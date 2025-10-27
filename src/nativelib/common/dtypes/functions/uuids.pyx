from struct import (
    pack,
    unpack,
)
from uuid import UUID


cpdef object read_uuid(
    object fileobj,
    object length,
    object precision,
    object scale,
    object tzinfo,
    object enumcase,
):
    """Read UUID from Native Format."""

    cdef bytes data = fileobj.read(16)
    cdef tuple parts = unpack("<8s8s", data)
    cdef bytes reversed_bytes = b"".join(parts[::-1])

    return UUID(bytes=reversed_bytes[::-1])


cpdef bytes write_uuid(
    object dtype_value,
    object length,
    object precision,
    object scale,
    object tzinfo,
    object enumcase,
):
    """Write UUID into Native Format."""

    if dtype_value is None:
        return bytes(16)

    cdef bytes uuid_bytes = dtype_value.bytes
    cdef bytes first_part = uuid_bytes[:8][::-1]
    cdef bytes second_part = uuid_bytes[8:][::-1]

    return pack("<8s8s", first_part, second_part)
