from decimal import Decimal
from io import (
    BufferedReader,
    BufferedWriter,
)

from .integers import (
    read_int,
    write_int,
)


__doc__ = """
All Decimals are read and written as Int8 - Int256.
Regardless of the specified aliases in the table,
this is written as Decimal(P, S).
To convert to Float, the following is required:
1. Determine the size of the signed integer:
P from [1: 9] - Int32
P from [10: 18] - Int64
P from [19: 38] - Int128
P from [39: 76] - Int256
2. Get the number from Native as a signed integer.
3. Number / pow(10, S)
"""


def read_decimal(
    file: BufferedReader,
    length: int,
    precission: int = 10,
    scale: int = 0,
    tzinfo: str | None = None,
    enum: dict[int, str] | None = None,
) -> Decimal:
    """Read Decimal(P, S) from Native Format."""

    dtype_value: int = read_int(file=file, precission=length)

    return Decimal(
        dtype_value / pow(10, scale)
    ).quantize(Decimal(10) ** -scale)


def write_decimal(
    dtype_value: Decimal,
    file: BufferedWriter,
    length: int,
    precission: int = 10,
    scale: int = 0,
    tzinfo: str | None = None,
    enum: dict[int, str] | None = None,
) -> None:
    """Write Decimal(P, S) into Native Format."""

    write_int(
        dtype_value=int(float(dtype_value) * pow(10, scale)),
        file=file,
        precission=length,
    )
