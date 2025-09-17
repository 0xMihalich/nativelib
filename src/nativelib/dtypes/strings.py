from io import (
    BufferedReader,
    BufferedWriter,
)

from ..length import (
    read_length,
    write_length,
)


def read_string(
    file: BufferedReader,
    length: int | None = None,
    precission: int | None = None,
    scale: int | None = None,
    tzinfo: str | None = None,
    enum: dict[int, str] | None = None,
) -> str:
    """Read string from Native Format."""

    if length is None:
        length = read_length(file)

    if length == 0:
        return ""

    return file.read(length).decode("utf-8")


def write_string(
    dtype_value: str,
    file: BufferedWriter,
    length: int | None = None,
    precission: int | None = None,
    scale: int | None = None,
    tzinfo: str | None = None,
    enum: dict[int, str] | None = None,
) -> None:
    """Write string into Native Format."""

    length = length or 0

    if length > 0:
        dtype_value = (
            "{dtype_value:<" + str(length) + "}"
        ).format(dtype_value=dtype_value)[:length]

    string_data = dtype_value.encode("utf-8")

    if not length:
        length = len(string_data)
        write_length(length, file)

    if length > 0:
        file.write(string_data)
