from io import BufferedReader
from types import NoneType


def read_bool(
    fileobj: BufferedReader,
    length: int | None = None,
    precision: int | None = None,
    scale: int | None = None,
    tzinfo: str | None = None,
    enumcase: dict[int, str] | None = None,
) -> bool:
    """Read Bool/Nullable from Native Format."""

    ...


def write_bool(
    dtype_value: bool,
    length: int | None = None,
    precision: int | None = None,
    scale: int | None = None,
    tzinfo: str | None = None,
    enumcase: dict[int, str] | None = None,
) -> bytes:
    """Write Bool/Nullable into Native Format."""

    ...


def read_nothing(
    fileobj: BufferedReader,
    length: int | None = None,
    precision: int | None = None,
    scale: int | None = None,
    tzinfo: str | None = None,
    enumcase: dict[int, str] | None = None,
) -> None:
    """Read Nullable(Nothing) from Native Format."""

    ...


def write_nothing(
    dtype_value: NoneType,
    length: int | None = None,
    precision: int | None = None,
    scale: int | None = None,
    tzinfo: str | None = None,
    enumcase: dict[int, str] | None = None,
) -> bytes:
    """Write Nullable(Nothing) into Native Format."""

    ...
