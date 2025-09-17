from dataclasses import dataclass
from io import (
    BufferedReader,
    BufferedWriter,
)

from ..dtype import (
    Array,
    DType,
    LowCardinality,
)
from ..dtypes import ClickhouseDtype
from ..length import write_length
from .parse import from_dtype


@dataclass
class ColumnInfo:
    """Column information."""

    header: bytes
    header_length: int
    total_rows: int
    column: str
    dtype: ClickhouseDtype
    is_array: bool
    is_lowcardinality: bool
    is_nullable: bool
    length: int | None
    precission: int | None
    scale: int | None
    tzinfo: str | None
    enum: dict[int, str] | None
    nested: int

    @classmethod
    def from_column_native(
        cls,
        total_rows: int,
        column: str,
        dtype: str,
    ) -> "ColumnInfo":
        """Initialize from native data."""

        header = b""

        for string in (column, dtype):
            bytestring = string.encode("utf-8")
            header += write_length(len(bytestring))
            header += bytestring

        return cls(
            header,
            len(header),
            total_rows,
            column,
            *from_dtype(dtype),
        )

    def make_dtype(
        self,
        file: BufferedReader | BufferedWriter,
    ) -> Array | DType | LowCardinality:
        """Make dtype object."""

        dtype = DType(
            file=file,
            dtype=self.dtype,
            is_nullable=self.is_nullable,
            length=self.length,
            precission=self.precission,
            scale=self.scale,
            tzinfo=self.tzinfo,
            enum=self.enum,
            total_rows=self.total_rows,
        )

        if self.is_lowcardinality:
            return LowCardinality(
                file=file,
                dtype=dtype,
                is_nullable=self.is_nullable,
                total_rows=self.total_rows,
            )

        if self.is_array:
            for _ in range(self.nested):
                dtype = Array(
                    file=file,
                    dtype=dtype,
                    total_rows=self.total_rows,
                )

        return dtype
