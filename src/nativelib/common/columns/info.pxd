cdef class ColumnInfo:

    cdef public bytes header
    cdef public unsigned short header_length
    cdef public unsigned long long total_rows
    cdef public str column
    cdef public object dtype
    cdef public object is_array
    cdef public object is_lowcardinality
    cdef public object is_nullable
    cdef public object length
    cdef public object precision
    cdef public object scale
    cdef public object tzinfo
    cdef public object enumcase
    cdef public unsigned short nested

    cpdef object make_dtype(self, object fileobj)
