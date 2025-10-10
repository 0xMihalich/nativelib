"""Reading data from LowCardinality block:

0. Supported data types: String, FixedString, Date, DateTime,
   and numbers excepting Decimal.
1. The number of rows in the header is ignored when working with this format.
2. Skip the 16-byte block; it will not participate in the parser.
3. Read the total number of unique elements in the block as UInt64 (8 bytes).
4. Based on the number obtained in point 3, determine the size of the index:
   UInt8 (1 byte) [0 : 254]
   UInt16 (2 bytes) [255 : 65534]
   UInt32 (4 bytes) [65535 : 4294967294]
   UInt64 (8 bytes) [4294967295 : 18446744073709551615]
5. Read all elements as a dictionary:
   key = index starting from 0, value = element.
   The first element always writes the default
   value for the specified data type.
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

from io import BufferedReader
from typing import Any

from .dtype import DType


class LowCardinality:
    """Class for unpacking data from
    the LowCardinality block into a regular
    Data Type (String, FixedString, Date, DateTime,
    and numbers excepting Decimal)."""

    def __init__(
        self,
        fileobj: BufferedReader,
        dtype: DType,
        is_nullable: bool,
        total_rows: int = 0,
    ):
        """Class initialization."""

        self.fileobj: BufferedReader
        self.dtype: DType
        self.name: str
        self.is_nullable: bool
        self.total_rows: int
        self.dictionary: list[Any]
        self.index_elements: list[Any]
        self.index_size: int
        self.defaul_value: object
        self.size: int
        ...

    def __index_size(self) -> None:
        """Get index_size."""

        ...

    def __update_index_size(self) -> None:
        """Update index_size."""

        ...

    def skip(self) -> None:
        """Skip read native column."""

        ...

    def read(self) -> list[Any]:
        """Read lowcardinality values from native column."""

        ...

    def write(self, dtype_value: Any) -> int:
        """Write lowcardinality values into native column."""

        ...

    def tell(self) -> int:
        """Return size of write values."""

        ...

    def clear(self) -> bytes:
        """Get column data and clean buffers."""

        ...
