from io import BufferedReader

from ..dtypes.dtype import ClickhouseDtype
from ..dtypes.objects import (
    Array,
    DType,
    LowCardinality,
)


class ColumnInfo:
    """Column information."""

    def __cinit__(
        self,
        total_rows: int,
        column: str,
        dtype: str,
    ):
        """Initialize from native data."""

        self.header: bytes
        self.header_length: int
        self.total_rows: int
        self.column: str
        self.dtype: ClickhouseDtype
        self.is_array: bool
        self.is_lowcardinality: bool
        self.is_nullable: bool
        self.length: int | None
        self.precision: int | None
        self.scale: int | None
        self.tzinfo: str | None
        self.enumcase: dict[int, str] | None
        self.nested: int
        ...

    def make_dtype(
        self,
        fileobj: BufferedReader,
    ) -> Array | DType | LowCardinality:
        """Make dtype object."""

        ...
