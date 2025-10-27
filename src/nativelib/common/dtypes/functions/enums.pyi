from enum import Enum
from io import BufferedReader


def read_enum(
    fileobj: BufferedReader,
    length: int,
    precision: int | None,
    scale: int | None,
    tzinfo: str | None,
    enumcase: dict[int, str] | None,
) -> str:
    """Read Enum8/Enum16 from Native Format."""

    ...


def write_enum(
    dtype_value: int | str | Enum,
    length: int,
    precision: int | None,
    scale: int | None,
    tzinfo: str | None,
    enumcase: dict[int, str] | None,
) -> bytes:
    """Write Enum8/Enum16 into Native Format."""

    ...
