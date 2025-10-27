from enum import Enum
from struct import (
    pack,
    unpack,
)


cdef dict EnumStructValue = {
    1: "<b",
    2: "<h",
}


cpdef str read_enum(
    object fileobj,
    int length,
    object precision,
    object scale,
    object tzinfo,
    dict enumcase,
):
    """Read Enum8/Enum16 from Native Format."""

    cdef bytes dtype_value = fileobj.read(length)
    cdef str struct_string = EnumStructValue[length]
    cdef short enum_key = unpack(struct_string, dtype_value)[0]
    return enumcase[enum_key]


cpdef bytes write_enum(
    object dtype_value,
    int length,
    object precision,
    object scale,
    object tzinfo,
    dict enumcase,
):
    """Write Enum8/Enum16 into Native Format."""

    if dtype_value is None:
        return bytes(length)

    cdef str struct_string = EnumStructValue[length]
    cdef short enum_key

    if dtype_value.__class__ == Enum:
        enum_key = dtype_value.value
    elif dtype_value.__class__ == str:
        for key, value in enumcase.items():
            if value == dtype_value:
                enum_key = key
                break
        else:
            raise ValueError(f"Enum don't have {dtype_value} value!")
    elif dtype_value.__class__ == int:
        enum_key = dtype_value
    else:
        raise ValueError(f"Enum must be in type int, str or Enum not {dtype_value.__class__}!")

    return pack(struct_string, enum_key)
