from io import (
    BytesIO,
    BufferedReader,
    BufferedWriter,
)
from typing import (
    Any,
    Generator,
    Union,
)

from .dtype import DType
from ..dtypes import (
    read_uint,
    write_uint,
)


class Array:
    """Clickhouse column array type manipulate."""

    def __init__(
        self,
        file: BufferedReader | BufferedWriter,
        dtype: Union[DType, "Array"],
        total_rows: int = 0,
    ) -> None:
        """Class initialization."""

        self.file = file
        self.dtype = dtype
        self.name = f"Array({dtype.name})"
        self.total_rows = total_rows
        self.row_elements: list[int] = []
        self.writable_buffer = BytesIO()

    def skip(self) -> None:
        """Skip read native column."""

        self.file.seek(self.file.tell() + (8 * (self.total_rows - 1)))
        self.dtype.total_rows = read_uint(self.file, 8)
        self.dtype.skip()

    def read(self) -> Generator[list[Any], None, None]:
        """Read array values from native column."""

        if not self.row_elements:
            self.row_elements = [
                read_uint(self.file, 8)
                for _ in range(self.total_rows)
            ]

        from_num = 0

        for num in self.row_elements:
            self.dtype.total_rows = num - from_num
            from_num += num
            yield list(self.dtype.read())

    def write(self, *dtype_values: list[Any]) -> None:
        """Write array values into native column."""

        num = self.dtype.total_rows

        for dtype_value in dtype_values:
            self.dtype.total_rows = len(dtype_value)
            num += self.dtype.total_rows
            write_uint(num, self.writable_buffer, 8)
            self.dtype.write(dtype_value)
            self.total_rows += 1

    def tell(self) -> int:
        """Return size of write buffers."""

        return (
            self.writable_buffer.tell() +
            self.dtype.tell()
        )

    def flush(self) -> int:
        """Write buffers into file."""

        size = self.file.write(self.writable_buffer.getvalue())
        self.writable_buffer.seek(0)
        self.writable_buffer.truncate()
        size += self.dtype.flush()

        return size
