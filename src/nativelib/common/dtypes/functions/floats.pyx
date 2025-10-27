from libc.math cimport pow
from libc.stdint cimport (
    uint16_t,
    uint32_t,
)
from struct import (
    pack,
    unpack,
)


cdef dict FloatStructValue = {
    4: "<f",
    8: "<d",
}


cpdef float read_bfloat16(
    object fileobj,
    object length,
    object precision,
    object scale,
    object tzinfo,
    object enumcase,
):
    """Read BFloat16 from Native Format."""

    cdef bytes bfloat16
    cdef unsigned short bits_int
    cdef int sign, exponent_int, mantissa
    cdef float exponent, mant_mult

    bfloat16 = fileobj.read(2)
    bits_int = (<unsigned char>bfloat16[1] << 8) | <unsigned char>bfloat16[0]
    sign = 1 if (bits_int & 0x8000) == 0 else -1
    exponent_int = (bits_int >> 7) & 0xff
    mantissa = bits_int & 0x7f

    if exponent_int == 0:
        if mantissa == 0:
            return 0.0
        return sign * (mantissa / 128.0) * pow(2, -126)
    if exponent_int == 0xff:
        if mantissa == 0:
            return sign * float('inf')
        return float('nan')

    exponent = <float>(1 << (exponent_int - 127)) if exponent_int >= 127 else 1.0 / <float>(1 << (127 - exponent_int))
    mant_mult = 1.0 + (mantissa / 128.0)
    return sign * exponent * mant_mult


cpdef bytes write_bfloat16(
    object dtype_value,
    object length,
    object precision,
    object scale,
    object tzinfo,
    object enumcase,
):
    """Write BFloat16 into Native Format."""

    if dtype_value is None:
        return bytes(2)

    cdef bytes float_bytes
    cdef uint32_t float_bits
    cdef uint16_t bfloat16_bits

    float_bytes = pack('f', <float>dtype_value)
    float_bits = (<unsigned char>float_bytes[3] << 24) | \
                 (<unsigned char>float_bytes[2] << 16) | \
                 (<unsigned char>float_bytes[1] << 8) | \
                 <unsigned char>float_bytes[0]
    bfloat16_bits = (float_bits >> 16) & 0xffff

    if (bfloat16_bits & 0x7fff) == 0x7F80:
        if bfloat16_bits & 0x8000:
            return b'\xFF\xFF'
        return b'\x7F\x80'
    if (bfloat16_bits & 0x7fff) > 0x7F80:
        return b'\x7F\xFF'

    return bfloat16_bits.to_bytes(2, 'little')


cpdef double read_float(
    object fileobj,
    int length,
    object precision,
    object scale,
    object tzinfo,
    object enumcase,
):
    """Read Float32/Float64 from Native Format."""

    cdef bytes float_bytes = fileobj.read(length)
    cdef str struct_string = FloatStructValue[length]
    return unpack(struct_string, float_bytes)[0]


cpdef bytes write_float(
    object dtype_value,
    int length,
    object precision,
    object scale,
    object tzinfo,
    object enumcase,
):
    """Write Float32/Float64 into Native Format."""

    if dtype_value is None:
        return bytes(length)

    cdef str struct_string = FloatStructValue[length]
    return pack(struct_string, <double>dtype_value)
