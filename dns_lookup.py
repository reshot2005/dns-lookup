#!/usr/bin/env python3
"""Resolve a hostname to its IPv4 and/or IPv6 addresses.

This is a defensive network utility using the operating system's resolver.
It performs a normal forward DNS resolution and does not perform scanning.
"""

from __future__ import annotations

import argparse
import ipaddress
import json
import socket
import sys
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class DNSResult:
    hostname: str
    addresses: tuple[str, ...]


def resolve_host(
    host: str,
    *,
    family: int = socket.AF_UNSPEC,
) -> DNSResult:
    """Resolve a hostname and return unique, normalized IP addresses."""
    hostname = host.strip()

    if not hostname:
        raise ValueError("hostname must not be empty")

    try:
        infos = socket.getaddrinfo(
            hostname,
            None,
            family=family,
            type=socket.SOCK_STREAM,
        )
    except socket.gaierror as exc:
        raise RuntimeError(f"DNS lookup failed: {exc}") from exc

    addresses: set[str] = set()

    for info in infos:
        sockaddr = info[4]
        if not sockaddr:
            continue

        address = sockaddr[0]

        try:
            addresses.add(str(ipaddress.ip_address(address)))
        except ValueError:
            # Ignore unexpected resolver output rather than emitting
            # malformed addresses.
            continue

    if not addresses:
        raise RuntimeError("resolver returned no IP addresses")

    return DNSResult(
        hostname=hostname,
        addresses=tuple(
            sorted(
                addresses,
                key=lambda value: (
                    ipaddress.ip_address(value).version,
                    ipaddress.ip_address(value),
                ),
            )
        ),
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Resolve a hostname to IPv4 and/or IPv6 addresses."
    )
    parser.add_argument(
        "--host",
        required=True,
        help="hostname to resolve, for example example.com",
    )
    parser.add_argument(
        "--family",
        choices=("any", "ipv4", "ipv6"),
        default="any",
        help="address family to return (default: any)",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        dest="output_format",
        help="output format (default: text)",
    )
    return parser


def family_from_argument(value: str) -> int:
    return {
        "any": socket.AF_UNSPEC,
        "ipv4": socket.AF_INET,
        "ipv6": socket.AF_INET6,
    }[value]


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        result = resolve_host(
            args.host,
            family=family_from_argument(args.family),
        )
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if args.output_format == "json":
        print(json.dumps(asdict(result), indent=2))
    else:
        for address in result.addresses:
            print(address)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
