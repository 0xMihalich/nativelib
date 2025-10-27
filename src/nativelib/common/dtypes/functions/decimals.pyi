"""All Decimals are read and written as Int8 - Int256.
Regardless of the specified aliases in the table,
this is written as Decimal(P, S).
To convert to Float, the following is required:
1. Determine the size of the signed integer:
P from [1: 9] - Int32
P from [10: 18] - Int64
P from [19: 38] - Int128
P from [39: 76] - Int256
2. Get the number from Native as a signed integer.
3. Number / pow(10, S)."""

from decimal import Decimal
from io import BufferedReader


def read_decimal(
    fileobj: BufferedReader,
    length: int | None,
    precision: int,
    scale: int,
    tzinfo: str | None,
    enumcase: dict[int, str] | None,
) -> Decimal:
    """Read Decimal(P, S) from Native Format."""

    ...


def write_decimal(
    dtype_value: Decimal,
    length: int | None,
    precision: int,
    scale: int,
    tzinfo: str | None,
    enumcase: dict[int, str] | None,
) -> bytes:
    """Write Decimal(P, S) into Native Format."""

    ...
