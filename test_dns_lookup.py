import socket
import unittest
from unittest.mock import patch

from dns_lookup import resolve_host


class TestDNSLookup(unittest.TestCase):
    @patch("dns_lookup.socket.getaddrinfo")
    def test_resolve_unique_addresses(self, mock_getaddrinfo):
        mock_getaddrinfo.return_value = [
            (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("192.0.2.10", 0)),
            (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("192.0.2.10", 0)),
            (socket.AF_INET6, socket.SOCK_STREAM, 6, "", ("2001:db8::10", 0, 0, 0)),
        ]

        result = resolve_host("example.test")

        self.assertEqual(
            result.addresses,
            ("192.0.2.10", "2001:db8::10"),
        )
        mock_getaddrinfo.assert_called_once_with(
            "example.test",
            None,
            family=socket.AF_UNSPEC,
            type=socket.SOCK_STREAM,
        )

    def test_empty_hostname(self):
        with self.assertRaises(ValueError):
            resolve_host("   ")

    @patch("dns_lookup.socket.getaddrinfo")
    def test_resolver_error(self, mock_getaddrinfo):
        mock_getaddrinfo.side_effect = socket.gaierror("name not known")

        with self.assertRaises(RuntimeError):
            resolve_host("missing.example")

    @patch("dns_lookup.socket.getaddrinfo")
    def test_no_addresses(self, mock_getaddrinfo):
        mock_getaddrinfo.return_value = []

        with self.assertRaises(RuntimeError):
            resolve_host("empty.example")


if __name__ == "__main__":
    unittest.main()
