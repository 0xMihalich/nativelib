from io import (
    BytesIO,
    BufferedReader,
    BufferedWriter,
)
from types import MethodType
from typing import (
    Any,
    Generator,
)

from ..associate import NillValues
from ..dtypes import ClickhouseDtype
from ..length import read_length


class DType:
    """Clickhouse column data type manipulate."""

    def __init__(
        self,
        file: BufferedReader | BufferedWriter,
        dtype: ClickhouseDtype,
        is_nullable: bool,
        length: int,
        precission: int,
        scale: int,
        tzinfo: str,
        enum: dict[int, str],
        total_rows: int = 0,
    ) -> None:
        """Class initialization."""

        self.file = file
        self.dtype = dtype
        self.name = dtype.name
        self.is_nullable = is_nullable
        self.length = length
        self.precission = precission
        self.scale = scale
        self.tzinfo = tzinfo
        self.enum = enum
        self.total_rows = total_rows
        self.nullable_map: dict[int, bool] = {}
        self.nullable_buffer = BytesIO()
        self.writable_buffer = BytesIO()

    @staticmethod
    def read_nullable(reader: MethodType):
        """Nullable read decorator."""

        def wrapper(self: "DType", raw: int):

            if self.is_nullable and not self.nullable_map:
                self.nullable_map = {
                    row: ClickhouseDtype.Nullable.read(self.file)
                    for row in range(self.total_rows)
                }

            dtype_value = reader(self, raw)

            if self.is_nullable and self.nullable_map[raw]:
                return

            return dtype_value

        return wrapper

    @staticmethod
    def write_nullable(writer: MethodType):
        """Nullable write decorator."""

        def wrapper(self: "DType", dtype_value: Any):

            if self.is_nullable:
                ClickhouseDtype.Nullable.write(
                    dtype_value is None,
                    self.nullable_buffer,
                )

            writer(
                self,
                NillValues.get(self.dtype.pytype)
                if dtype_value is None
                else dtype_value
            )
            self.total_rows += 1

        return wrapper

    @read_nullable
    def read_dtype(self, row: int) -> Any:
        """Read dtype value from native column."""

        _ = row

        return self.dtype.read(
            self.file,
            self.length,
            self.precission,
            self.scale,
            self.tzinfo,
            self.enum,
        )

    @write_nullable
    def write_dtype(self, dtype_value: Any) -> None:
        """Write dtype value into native column."""

        self.dtype.write(
            dtype_value,
            self.writable_buffer,
            self.length,
            self.precission,
            self.scale,
            self.tzinfo,
            self.enum,
        )

    def skip(self) -> None:
        """Skip read native column."""

        if self.is_nullable:
            self.file.seek(self.file.tell() + self.total_rows)

        if self.length is not None:
            self.file.seek(
                self.file.tell() + (self.length * self.total_rows)
            )
            return

        for _ in range(self.total_rows):
            length = read_length(self.file)
            self.file.seek(self.file.tell() + length)

    def read(self) -> Generator[Any, None, None]:
        """Read dtype values from native column."""

        for row in range(self.total_rows):
            yield self.read_dtype(row)

    def write(self, *dtype_values: Any) -> None:
        """Write dtype values into native column."""

        for dtype_value in dtype_values:
            self.write_dtype(dtype_value)

    def tell(self) -> int:
        """Return size of write buffers."""

        return (
            self.nullable_buffer.tell() +
            self.writable_buffer.tell()
        )

    def flush(self) -> int:
        """Write buffers into file."""

        size = 0

        for buffer in (
            self.nullable_buffer,
            self.writable_buffer,
        ):
            size += self.file.write(buffer.getvalue())
            buffer.seek(0)
            buffer.truncate()

        return size
