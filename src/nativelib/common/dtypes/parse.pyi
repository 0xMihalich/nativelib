from .dtype import ClickhouseDtype


def from_dtype(
    dtype: str,
    is_array: bool = False,
    is_lowcardinality: bool = False,
    is_nullable: bool = False,
    length: int | None = None,
    precision: int | None = None,
    scale: int | None = None,
    tzinfo: str | None = None,
    enumcase: dict[int, str] | None = None,
    nested: int = 0,
) -> tuple[
    ClickhouseDtype,
    bool,
    bool,
    bool,
    int | None,
    int | None,
    int | None,
    str | None,
    dict[int, str] | None,
    int,
]:
    """Parse info from dtype."""

    ...
