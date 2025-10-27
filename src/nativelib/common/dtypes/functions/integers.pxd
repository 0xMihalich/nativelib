cpdef Py_ssize_t read_int(
    object fileobj,
    int length,
    object precision,
    object scale,
    object tzinfo,
    object enumcase,
)
cpdef bytes write_int(
    object dtype_value,
    int length,
    object precision,
    object scale,
    object tzinfo,
    object enumcase,
)
cpdef Py_ssize_t read_uint(
    object fileobj,
    int length,
    object precision=*,
    object scale=*,
    object tzinfo=*,
    object enumcase=*,
)
cpdef bytes write_uint(
    object dtype_value,
    int length,
    object precision=*,
    object scale=*,
    object tzinfo=*,
    object enumcase=*,
)
cdef unsigned long long r_uint(object fileobj, unsigned char length)
cdef bytes w_uint(unsigned long long dtype_value, unsigned char length)
