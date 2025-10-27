from nativelib.common.length cimport (
    read_length,
    write_length,
)


cpdef str read_string(
    object fileobj,
    object length = None,
    object precision = None,
    object scale = None,
    object tzinfo = None,
    object enumcase = None,
):
    """Read string from Native Format."""

    cdef int string_length

    if length is None:
        string_length = read_length(fileobj)
    else:
        string_length = length

    if string_length == 0:
        return ""

    cdef bytes string = fileobj.read(string_length)
    return string.decode("utf-8", errors="replace")


cpdef bytes write_string(
    object dtype_value,
    object length = None,
    object precision = None,
    object scale = None,
    object tzinfo = None,
    object enumcase = None,
):
    """Write string into Native Format."""

    cdef bytes string
    cdef int string_length

    if dtype_value is None:
        string = b""
    else:
        string = str(dtype_value).encode("utf-8")

    if length is None:
        string_length = len(string)
        return write_length(string_length) + string

    string_length = length

    if string_length > len(string):
        string += bytes(string_length - len(string))
        return string

    return string[:string_length]
