from io import BufferedReader
from ipaddress import (
    IPv4Address,
    IPv6Address,
)


def read_ipv4(
    fileobj: BufferedReader,
    length: int | None,
    precision: int | None,
    scale: int | None,
    tzinfo: str | None,
    enumcase: dict[int, str] | None,
) -> IPv4Address:
    """Read IPv4 from Native Format."""

    ...


def write_ipv4(
    dtype_value: IPv4Address,
    length: int | None,
    precision: int | None,
    scale: int | None,
    tzinfo: str | None,
    enumcase: dict[int, str] | None,
) -> bytes:
    """Write IPv4 into Native Format."""

    ...


def read_ipv6(
    fileobj: BufferedReader,
    length: int | None,
    precision: int | None,
    scale: int | None,
    tzinfo: str | None,
    enumcase: dict[int, str] | None,
) -> IPv6Address:
    """Read IPv6 from Native Format."""

    ...


def write_ipv6(
    dtype_value: IPv6Address,
    length: int | None,
    precision: int | None,
    scale: int | None,
    tzinfo: str | None,
    enumcase: dict[int, str] | None,
) -> bytes:
    """Write IPv6 into Native Format."""

    ...
