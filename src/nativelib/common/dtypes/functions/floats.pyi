from io import BufferedReader


def read_bfloat16(
    fileobj: BufferedReader,
    length: int,
    precision: int | None,
    scale: int | None,
    tzinfo: str | None,
    enumcase: dict[int, str] | None,
) -> float:
    """Read BFloat16 from Native Format."""

    ...


def write_bfloat16(
    dtype_value: float,
    length: int,
    precision: int | None,
    scale: int | None,
    tzinfo: str | None,
    enumcase: dict[int, str] | None,
) -> bytes:
    """Write BFloat16 into Native Format."""

    ...


def read_float(
    fileobj: BufferedReader,
    length: int,
    precision: int | None,
    scale: int | None,
    tzinfo: str | None,
    enumcase: dict[int, str] | None,
) -> float:
    """Read Float32/Float64 from Native Format."""

    ...


def write_float(
    dtype_value: float,
    length: int,
    precision: int | None,
    scale: int | None,
    tzinfo: str | None,
    enumcase: dict[int, str] | None,
) -> bytes:
    """Write Float32/Float64 into Native Format."""

    ...
