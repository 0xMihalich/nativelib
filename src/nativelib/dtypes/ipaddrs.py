from ipaddress import (
    ip_address,
    IPv4Address,
    IPv6Address,
)
from io import (
    BufferedReader,
    BufferedWriter,
)


def read_ipv4(
    file: BufferedReader,
    length: int | None = None,
    precission: int | None = None,
    scale: int | None = None,
    tzinfo: str | None = None,
    enum: dict[int, str] | None = None,
) -> IPv4Address:
    """Read IPv4 from Native Format."""

    return ip_address(file.read(4)[::-1])


def write_ipv4(
    dtype_value: IPv4Address,
    file: BufferedWriter,
    length: int | None = None,
    precission: int | None = None,
    scale: int | None = None,
    tzinfo: str | None = None,
    enum: dict[int, str] | None = None,
) -> None:
    """Write IPv4 into Native Format."""

    file.write(dtype_value.packed[::-1])


def read_ipv6(
    file: BufferedReader,
    length: int | None = None,
    precission: int | None = None,
    scale: int | None = None,
    tzinfo: str | None = None,
    enum: dict[int, str] | None = None,
) -> IPv6Address:
    """Read IPv6 from Native Format."""

    return ip_address(file.read(16))


def write_ipv6(
    dtype_value: IPv6Address,
    file: BufferedWriter,
    length: int | None = None,
    precission: int | None = None,
    scale: int | None = None,
    tzinfo: str | None = None,
    enum: dict[int, str] | None = None,
) -> None:
    """Write IPv6 into Native Format."""

    file.write(dtype_value.packed)
