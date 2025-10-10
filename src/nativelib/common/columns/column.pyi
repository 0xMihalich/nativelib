from io import BufferedReader
from typing import (
    Any,
    Iterator,
)

from ..dtypes.objects import (
    Array,
    DType,
    LowCardinality,
)
from .info import ColumnInfo


class Column:
    """Column object."""

    def __init__(
        self,
        column: str,
        dtype: str,
        fileobj: BufferedReader | None = None,
        total_rows: int = 0,
    ) -> None:
        """Class initialization."""

        self.column: str
        self.fileobj: BufferedReader | None
        self.info: ColumnInfo
        self.dtype: Array | DType | LowCardinality
        self.data: list[Any] | None
        self.iter_data: Iterator[Any] | None
        self.pos: int
        ...

    @property
    def total_rows(self) -> int:
        """Get total rows."""

        ...

    def __iter__(self) -> "Column":
        """Iterator method."""

        ...

    def __next__(self) -> Any:
        """Next method."""

        ...

    def skip(self) -> None:
        """Skip read native column."""

        ...

    def read(self) -> list[Any]:
        """Read data from column."""

        ...

    def write(self, data: Any) -> int:
        """Write data into column."""

        ...

    def tell(self) -> int:
        """Return current size."""

        ...

    def clear(self) -> bytes:
        """Get column data and clean."""

        ...
