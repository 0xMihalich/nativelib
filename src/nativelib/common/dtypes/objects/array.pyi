from io import BufferedReader
from typing import Any

from .dtype import DType


class Array:
    """Clickhouse column array type manipulate."""

    def __init__(
        self,
        fileobj: BufferedReader,
        dtype: DType | "Array",
        total_rows: int = 0,
    ):
        """Class initialization."""

        self.fileobj: BufferedReader
        self.dtype: DType | Array
        self.name: str
        self.total_rows: int
        self.row_elements: list
        self.writable_buffer: list
        self.pos: int
        ...

    def skip(self) -> None:
        """Skip read native column."""

        ...

    def read(self) -> list[Any]:
        """Read array values from native column."""

        ...

    def write(self, dtype_value: list[Any]) -> int:
        """Write array values into native column."""

        ...

    def tell(self) -> int:
        """Return size of write buffers."""

        ...

    def clear(self) -> bytes:
        """Get column data and clean buffers."""

        ...
