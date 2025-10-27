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

from libc.math cimport pow
from decimal import Decimal


cdef unsigned char find_length(unsigned char precision):
    """Find Decimal lens."""

    if precision not in range(1, 77):
        raise ValueError("precision must be in [1:76] range!")
    if precision <= 9:
        return 4
    if precision <= 18:
        return 8
    if precision <= 38:
        return 16
    return 32


cpdef object read_decimal(
    object fileobj,
    object length,
    unsigned char precision,
    unsigned char scale,
    object tzinfo,
    object enumcase,
):
    """Read Decimal(P, S) from Native Format."""

    cdef unsigned char decimal_length = find_length(precision)
    cdef bytes decimal_bytes = fileobj.read(decimal_length)
    cdef object decimal_value = int.from_bytes(decimal_bytes, "little", signed=True)
    cdef long long divider = <long long>pow(10, scale)
    cdef object quantize = Decimal(10) ** -scale
    cdef object decimal = Decimal(decimal_value / divider)
    return decimal.quantize(quantize)


cpdef bytes write_decimal(
    object dtype_value,
    object length,
    unsigned char precision,
    unsigned char scale,
    object tzinfo,
    object enumcase,
):
    """Write Decimal(P, S) into Native Format."""

    cdef unsigned char decimal_length = find_length(precision)

    if dtype_value is None:
        return bytes(decimal_length)

    cdef long long divider = <long long>pow(10, scale)
    cdef object decimal_value = int(dtype_value * divider)
    return decimal_value.to_bytes(decimal_length, "little", signed=True)
