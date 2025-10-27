from io import BufferedReader


def read_string(
    fileobj: BufferedReader,
    length: int | None = None,
    precision: int | None = None,
    scale: int | None = None,
    tzinfo: str | None = None,
    enumcase: dict[int, str] | None = None,
) -> str:
    """Read string from Native Format."""

    ...


def write_string(
    dtype_value: str,
    length: int | None = None,
    precision: int | None = None,
    scale: int | None = None,
    tzinfo: str | None = None,
    enumcase: dict[int, str] | None = None,
) -> bytes:
    """Write string into Native Format."""

    ...
