cpdef Py_ssize_t read_int(
    object fileobj,
    int length,
    object precision,
    object scale,
    object tzinfo,
    object enumcase,
):
    """Read signed integer from Native Format."""

    cdef bytes int_value = fileobj.read(length)
    return int.from_bytes(int_value, "little", signed=True)


cpdef bytes write_int(
    object dtype_value,
    int length,
    object precision,
    object scale,
    object tzinfo,
    object enumcase,
):
    """Write signed integer into Native Format."""

    if dtype_value is None:
        return bytes(length)

    cdef Py_ssize_t int_value = <Py_ssize_t>dtype_value
    return int_value.to_bytes(length, "little", signed=True)


cpdef Py_ssize_t read_uint(
    object fileobj,
    int length,
    object precision = None,
    object scale = None,
    object tzinfo = None,
    object enumcase = None,
):
    """Read unsigned integer from Native Format."""

    cdef bytes int_value = fileobj.read(length)
    return int.from_bytes(int_value, "little", signed=False)


cpdef bytes write_uint(
    object dtype_value,
    int length,
    object precision = None,
    object scale = None,
    object tzinfo = None,
    object enumcase = None,
):
    """Write unsigned integer into Native Format."""

    if dtype_value is None:
        return bytes(length)

    cdef Py_ssize_t int_value = <Py_ssize_t>dtype_value
    return int_value.to_bytes(length, "little", signed=False)


cdef unsigned long long r_uint(object fileobj, unsigned char length):
    """Cython read uint function."""

    cdef bytes int_value = fileobj.read(length)
    return int.from_bytes(int_value, "little", signed=False)


cdef bytes w_uint(unsigned long long dtype_value, unsigned char length):
    """Cython write uint function."""

    return dtype_value.to_bytes(length, "little", signed=False)
