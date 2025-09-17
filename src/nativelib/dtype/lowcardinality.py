from io import (
    BufferedReader,
    BufferedWriter,
)
from typing import (
    Any,
    Generator,
    NoReturn,
)

from ..dtypes import read_uint
from .dtype import DType


__doc__ = """
Reading data from LowCardinality block:
0. Supported data types: String, FixedString, Date, DateTime,
and numbers excepting Decimal.
1. The number of rows in the header is ignored when working with this format.
2. Skip the 16-byte block; it will not participate in the parser.
3. Read the total number of unique elements in the block as UInt64 (8 bytes).
4. Based on the number obtained in point 3, determine the size of the index:
UInt8 (1 byte)
[0 : 254]
UInt16 (2 bytes)
[255 : 65534]
UInt32 (4 bytes)
[65535 : 4294967294]
UInt64 (8 bytes)
[4294967295 : 18446744073709551615]
5. Read all elements as a dictionary: key = index starting from 0,
value = element.
The first element always writes the default value for the specified data type.
If Nullable is additionally specified
[for example, LowCardinality(Nullable(String))],
the first two values will be default,
but the element with index 0 corresponds to None,
and the element with index 1 corresponds to the default
value for this data type (an empty string).
6. Read the total number of elements in the block as UInt64 (8 bytes).
This parameter corresponds to the number of rows in the header.
7. Read the index of each element according to the size obtained in point 4
and relate it to the value in the dictionary.
"""

def index_size(total_elements: int) -> int:
    """Detect index size."""

    if total_elements < 0:
        raise ValueError("Non uint value!")
    if total_elements <= 0xff:
        return 1
    if total_elements <= 0xffff:
        return 2
    if total_elements <= 0xffffffff:
        return 4
    return 8


def size_from_header(file: BufferedReader) -> int:
    """Get index size from header."""

    file.read(8)  # hex 0100000000000000
    item = read_uint(file, 1)  # index_size key
    file.read(7) # hex 06000000000000

    return {
        0: 1,  # UInt8
        1: 2,  # UInt16
        2: 4,  # UInt32
        3: 8,  # UInt64
    }[item]


class LowCardinality:
    """Class for unpacking data from
    the LowCardinality block into a regular
    Data Type (String, FixedString, Date, DateTime,
    and numbers excepting Decimal)."""

    def __init__(
        self,
        file: BufferedReader | BufferedWriter,
        dtype: DType,
        is_nullable: bool,
        total_rows: int = 0,
    ) -> None:
        """Class initialization."""

        self.file = file
        self.dtype = dtype
        self.name = f"LowCardinality({dtype.name})"
        self.is_nullable = is_nullable
        self.total_rows = total_rows
        self.dictionary: dict[int, Any] = {}
        self.index_size = 0

    def __index_size(self) -> None:
        """Get index_size."""

        if not self.index_size:
            self.file.seek(self.file.tell() + 16)  # skip header
            self.dtype.is_nullable = False
            self.dtype.total_rows = read_uint(self.file, 8)
            self.index_size = index_size(self.dtype.total_rows)

    def skip(self) -> None:
        """Skip read native column."""

        self.__index_size()
        self.dtype.skip()
        self.total_rows = read_uint(self.file, 8)
        self.file.seek(self.file.tell() + (self.index_size * self.total_rows))

    def read(self) -> Generator[Any, None, None]:
        """Read lowcardinality values from native column."""

        self.__index_size()

        if not self.dictionary:
            self.dictionary = {
                index: None
                if self.is_nullable and index == 0 else dtype_value
                for index, dtype_value in enumerate(self.dtype.read())
            }

        self.total_rows = read_uint(self.file, 8)

        for _ in range(self.total_rows):
            yield self.dictionary[read_uint(self.file, self.index_size)]

    def write(self, *dtype_values: list[Any]) -> NoReturn:
        """Write lowcardinality values into native column."""

        _ = dtype_values

        raise NotImplementedError("write method don't support now.")

    def tell(self) -> NoReturn:
        """Return size of write buffers."""

        raise NotImplementedError("tell method don't support now.")

    def flush(self) -> NoReturn:
        """Write buffers into file."""

        raise NotImplementedError("flush method don't support now.")
