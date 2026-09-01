# DNS Lookup Tool

A lightweight, dependency-free Python utility for performing **forward DNS lookups** through the operating system's resolver.

It resolves a hostname to its unique IPv4 and/or IPv6 addresses and supports machine-readable JSON output.

## Features

- IPv4 and IPv6 resolution
- Automatic address-family detection
- Unique, normalized results
- Deterministic output ordering
- JSON output
- Input validation
- Clear resolver errors
- Standard-library-only
- Unit tests
- GitHub Actions CI
- Python 3.10–3.14 testing

## Requirements

- Python 3.10+
- Network/resolver access as provided by the host operating system

No third-party Python dependencies are required.

## Usage

Resolve both IPv4 and IPv6 addresses:

```bash
python3 dns_lookup.py --host example.com
```

IPv4 only:

```bash
python3 dns_lookup.py \
  --host example.com \
  --family ipv4
```

IPv6 only:

```bash
python3 dns_lookup.py \
  --host example.com \
  --family ipv6
```

JSON output:

```bash
python3 dns_lookup.py \
  --host example.com \
  --format json
```

## Example output

Text:

```text
93.184.216.34
2606:2800:220:1:248:1893:25c8:1946
```

JSON:

```json
{
  "hostname": "example.com",
  "addresses": [
    "93.184.216.34",
    "2606:2800:220:1:248:1893:25c8:1946"
  ]
}
```

## How it works

The tool uses Python's standard-library `socket.getaddrinfo()` rather than implementing its own DNS protocol client.

This means the actual resolution behavior depends on the operating system and configured resolver stack, which may include:

- local resolver configuration
- DNS caching
- enterprise DNS
- VPN DNS
- `/etc/hosts` or equivalent local mappings
- OS-specific name-resolution mechanisms

It is therefore best described as an **OS resolver lookup**, not a direct authoritative DNS query.

## Limitations

This tool performs a forward hostname-to-address lookup only.

It does not:

- enumerate DNS records
- perform DNS zone transfers
- scan ports
- discover subdomains
- query authoritative nameservers directly
- perform reverse DNS lookups
- validate DNSSEC
- bypass local resolver configuration

If you need a specific DNS record type such as MX, TXT, NS, CNAME, or DNSSEC data, a dedicated DNS client/library is more appropriate.

## Security

The tool performs a normal local name-resolution operation and does not modify the target system.

Use network utilities only against systems and infrastructure you are authorized to assess.

## Exit codes

| Code | Meaning |
|---:|---|
| `0` | Lookup completed successfully |
| `1` | Resolver/lookup failure |
| `2` | Invalid command-line input |

## Development

Run tests:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

## License

MIT. See [LICENSE](LICENSE).
