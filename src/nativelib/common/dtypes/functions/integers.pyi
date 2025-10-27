from io import BufferedReader


def read_int(
    fileobj: BufferedReader,
    length: int,
    precision: int | None,
    scale: int | None,
    tzinfo: str | None,
    enumcase: dict[int, str] | None,
) -> int:
    """Read signed integer from Native Format."""

    ...


def write_int(
    dtype_value: int,
    length: int,
    precision: int | None,
    scale: int | None,
    tzinfo: str | None,
    enumcase: dict[int, str] | None,
) -> bytes:
    """Write signed integer into Native Format."""

    ...


def read_uint(
    fileobj: BufferedReader,
    length: int,
    precision: int | None = None,
    scale: int | None = None,
    tzinfo: str | None = None,
    enumcase: dict[int, str] | None = None,
) -> int:
    """Read unsigned integer from Native Format."""

    ...


def write_uint(
    dtype_value: int,
    length: int,
    precision: int | None = None,
    scale: int | None = None,
    tzinfo: str | None = None,
    enumcase: dict[int, str] | None = None,
) -> bytes:
    """Write unsigned integer into Native Format."""

    ...


def r_uint(fileobj: BufferedReader, length: int) -> int:
    """Cython read uint function."""

    ...


def w_uint(dtype_value: int, length: int) -> bytes:
    """Cython write uint function."""

    ...
