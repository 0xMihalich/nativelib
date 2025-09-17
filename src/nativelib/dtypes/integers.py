from io import (
    BufferedReader,
    BufferedWriter,
)


def read_int(
    file: BufferedReader,
    length: int,
    precission: int | None = None,
    scale: int | None = None,
    tzinfo: str | None = None,
    enum: dict[int, str] | None = None,
) -> int:
    """Read signed integer from Native Format."""

    return int.from_bytes(file.read(length), "little", signed=True)


def write_int(
    dtype_value: int,
    file: BufferedWriter,
    length: int,
    precission: int | None = None,
    scale: int | None = None,
    tzinfo: str | None = None,
    enum: dict[int, str] | None = None,
) -> None:
    """Write signed integer into Native Format."""

    file.write(dtype_value.to_bytes(length, "little", signed=True))


def read_uint(
    file: BufferedReader,
    length: int,
    precission: int | None = None,
    scale: int | None = None,
    tzinfo: str | None = None,
    enum: dict[int, str] | None = None,
) -> int:
    """Read unsigned integer from Native Format."""

    return int.from_bytes(file.read(length), "little", signed=False)


def write_uint(
    dtype_value: int,
    file: BufferedWriter,
    length: int,
    precission: int | None = None,
    scale: int | None = None,
    tzinfo: str | None = None,
    enum: dict[int, str] | None = None,
) -> None:
    """Write unsigned integer into Native Format."""

    file.write(dtype_value.to_bytes(length, "little", signed=False))
