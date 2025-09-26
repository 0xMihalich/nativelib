cpdef int read_int(
    object fileobj,
    int length,
    object precission,
    object scale,
    object tzinfo,
    object enumcase,
)
cpdef bytes write_int(
    int dtype_value,
    int length,
    object precission,
    object scale,
    object tzinfo,
    object enumcase,
)
cpdef int read_uint(
    object fileobj,
    int length,
    object precission=*,
    object scale=*,
    object tzinfo=*,
    object enumcase=*,
)
cpdef bytes write_uint(
    unsigned int dtype_value,
    int length,
    object precission=*,
    object scale=*,
    object tzinfo=*,
    object enumcase=*,
)
cdef unsigned long long r_uint(object fileobj, unsigned char length)
cdef bytes w_uint(unsigned long long dtype_value, unsigned char length)
