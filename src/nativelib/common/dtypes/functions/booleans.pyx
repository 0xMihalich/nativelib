from struct import (
    pack,
    unpack,
)


cpdef object read_bool(
    object fileobj,
    object length = None,
    object precision = None,
    object scale = None,
    object tzinfo = None,
    object enumcase = None,
):
    """Read Bool/Nullable from Native Format."""

    cdef bytes boolean_byte = fileobj.read(1)
    return unpack("<?", boolean_byte)[0]


cpdef bytes write_bool(
    object dtype_value,
    object length = None,
    object precision = None,
    object scale = None,
    object tzinfo = None,
    object enumcase = None,
):
    """Write Bool/Nullable into Native Format."""

    if dtype_value is None:
        return b"\x00"

    return pack("<?", bool(dtype_value))


cpdef object read_nothing(
    object fileobj,
    object length = None,
    object precision = None,
    object scale = None,
    object tzinfo = None,
    object enumcase = None,
):
    """Read Nullable(Nothing) from Native Format."""

    fileobj.read(1)


cpdef bytes write_nothing(
    object dtype_value = None,
    object length = None,
    object precision = None,
    object scale = None,
    object tzinfo = None,
    object enumcase = None,
):
    """Write Nullable(Nothing) into Native Format."""

    return b"0"
