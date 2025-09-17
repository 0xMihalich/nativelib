from io import (
    BufferedReader,
    BufferedWriter,
)
from struct import (
    pack,
    unpack,
)
from types import NoneType


def read_bool(
    file: BufferedReader,
    length: int | None = None,
    precission: int | None = None,
    scale: int | None = None,
    tzinfo: str | None = None,
    enum: dict[int, str] | None = None,
) -> bool:
    """Read Bool from Native Format."""

    return unpack("<?", file.read(1))[0]


def write_bool(
    dtype_value: bool,
    file: BufferedWriter,
    length: int | None = None,
    precission: int | None = None,
    scale: int | None = None,
    tzinfo: str | None = None,
    enum: dict[int, str] | None = None,
) -> None:
    """Write Bool into Native Format."""

    file.write(pack("<?", bool(dtype_value)))


def read_nullable(
    file: BufferedReader,
    length: int | None = None,
    precission: int | None = None,
    scale: int | None = None,
    tzinfo: str | None = None,
    enum: dict[int, str] | None = None,
) -> bool:
    """Read Nullable from Native Format."""

    return read_bool(file)


def write_nullable(
    dtype_value: bool,
    file: BufferedWriter,
    length: int | None = None,
    precission: int | None = None,
    scale: int | None = None,
    tzinfo: str | None = None,
    enum: dict[int, str] | None = None,
) -> None:
    """Write Nullable into Native Format."""

    write_bool(dtype_value, file)


def read_nothing(
    file: BufferedReader,
    length: int | None = None,
    precission: int | None = None,
    scale: int | None = None,
    tzinfo: str | None = None,
    enum: dict[int, str] | None = None,
) -> None:
    """Read Nullable(Nothing) from Native Format."""

    file.read(1)


def write_nothing(
    dtype_value: NoneType,
    file: BufferedWriter,
    length: int | None = None,
    precission: int | None = None,
    scale: int | None = None,
    tzinfo: str | None = None,
    enum: dict[int, str] | None = None,
) -> None:
    """Write Nullable(Nothing) into Native Format."""

    file.write(b"0")
