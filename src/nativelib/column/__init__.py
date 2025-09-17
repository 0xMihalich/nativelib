"""Native column manipulate objects."""

from collections.abc import Iterator
from io import (
    BufferedReader,
    BufferedWriter,
)
from typing import Any

from pgcopylib import PGOid
from pgpack.structs import PGParam

from ..associate import (
    ArrayToOid,
    OidToDtype,
)

from ..dtype import (
    Array,
    DType,
    LowCardinality,

)
from .info import ColumnInfo


__all__ = (
    "Column",
    "ColumnInfo",
)


class Column:
    """Column object."""

    info: ColumnInfo
    dtype: Array | DType | LowCardinality
    data: tuple[Any] | None
    iter_data: Iterator | None

    def __init__(
        self,
        file: BufferedReader | BufferedWriter,
        total_rows: int,
        column: str,
        dtype: str,
    ) -> None:
        """Class initialization."""

        self.file = file
        self.total_rows = total_rows
        self.column = column
        self.dtype = dtype

        self.info = ColumnInfo.from_column_native(
            total_rows=self.total_rows,
            column=self.column,
            dtype=self.dtype,
        )
        self.dtype = self.info.make_dtype(file=self.file)
        self.data = None
        self.iter_data = None

    def __iter__(self) -> "Column":
        """Iterator method."""

        self.read()
        self.iter_data = iter(self.data)
        return self

    def __next__(self) -> Any:
        """Next method."""

        return next(self.iter_data)

    def skip(self) -> None:
        """Skip read native column."""

        self.dtype.skip()

    def read(self) -> tuple[Any]:
        """Read data from column."""

        if not self.data:
            self.data = tuple(self.dtype.read())

        return self.data

    def write(
        self,
        *data: Any,
    ) -> int:
        """Write data into column."""

        self.dtype.write(*data)
        return self.dtype.tell()

    def flush(self) -> int:
        """Write buffers into file."""

        self.file.write(self.info.header)
        return self.dtype.flush()

    @classmethod
    def from_pgpack_params(
        cls,
        file: BufferedWriter,
        column: str,
        pgtype: PGOid,
        pgparam: PGParam,
        not_null: bool = False,
    ) -> list:
        """Make column objects from pgpack_metadata."""

        oid = pgtype.value

        if pgparam.nested:
            oid = ArrayToOid[oid]

        if oid == 1042:
            args = f"({pgparam.length})"
        elif oid == 1184:
            args = "(3, 'UTC')"
        elif oid == 1700:
            args = f"({pgparam.length}, {pgparam.scale})"
        elif oid == 1266:
            args = "(3)"
        else:
            args = ""

        if not_null:
            dtype = OidToDtype[oid] + args
        else:
            dtype = f"Nullable({OidToDtype[oid]}{args})"

        for _ in range(pgparam.nested):
            dtype = f"Array({dtype})"

        return cls(
            file=file,
            total_rows=0,
            column=column,
            dtype=dtype,
        )
