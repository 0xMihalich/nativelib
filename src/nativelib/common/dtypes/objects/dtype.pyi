from io import BufferedReader
from typing import Any

from ..dtype import ClickhouseDtype


class DType:
    """Clickhouse column data type manipulate."""

    def __init__(
        self,
        fileobj: BufferedReader,
        dtype: ClickhouseDtype,
        is_nullable: bool,
        length: int | None,
        precision: int | None,
        scale: int | None,
        tzinfo: str | None,
        enumcase: dict[int, str] | None,
        total_rows: int = 0,
    ):
        """Class initialization."""

        self.fileobj: BufferedReader
        self.dtype: ClickhouseDtype
        self.name: str
        self.is_nullable: bool
        self.length: int | None
        self.precision: int | None
        self.scale: int | None
        self.tzinfo: str | None
        self.enumcase: dict[int, str] | None
        self.total_rows: int
        self.nullable_map: list[bool]
        self.nullable_buffer: list[bytes]
        self.writable_buffer: list[bytes]
        self.pos: int

    def read_dtype(self, row: int) -> Any:
        """Read dtype value from native column."""

        ...

    def write_dtype(self, dtype_value: Any) -> None:
        """Write dtype value into native column."""

        ...

    def skip(self) -> None:
        """Skip read native column."""

        ...

    def read(self) -> list[Any]:
        """Read dtype values from native column."""

        ...

    def write(self, dtype_value: Any) -> int:
        """Write dtype values into native column."""

        ...

    def tell(self) -> int:
        """Return size of write buffers."""

        ...

    def clear(self) -> bytes:
        """Get column data and clean buffers."""

        ...
