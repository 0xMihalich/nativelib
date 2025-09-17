from enum import Enum
from io import (
    BufferedReader,
    BufferedWriter,
)
from struct import (
    pack,
    unpack,
)


EnumStructValue: dict[int, str] = {
    1: "<b",
    2: "<h",
}


def read_enum(
    file: BufferedReader,
    length: int | None = None,
    precission: int | None = None,
    scale: int | None = None,
    tzinfo: str | None = None,
    enum: dict[int, str] = {},
) -> str:
    """Read Enum8/Enum16 from Native Format."""

    return enum[
        unpack(EnumStructValue[length], file.read(length),)[0]
    ]


def write_enum(
    dtype_value: int | Enum,
    file: BufferedWriter,
    length: int | None = None,
    precission: int | None = None,
    scale: int | None = None,
    tzinfo: str | None = None,
    enum: dict[int, str] | None = None,
) -> None:
    """Write Enum8/Enum16 into Native Format."""

    if isinstance(dtype_value, Enum):
        dtype_value: int = dtype_value.value

    file.write(
        pack(EnumStructValue[precission], dtype_value)
    )
