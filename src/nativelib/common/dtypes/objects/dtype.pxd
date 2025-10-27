cdef class DType:

    cdef public object fileobj
    cdef public object dtype
    cdef public str name
    cdef public object is_nullable
    cdef public object length
    cdef public object precision
    cdef public object scale
    cdef public object tzinfo
    cdef public object enumcase
    cdef public unsigned long long total_rows
    cdef public list nullable_map
    cdef public list nullable_buffer
    cdef public list writable_buffer
    cdef public unsigned long long pos

    cdef object read_dtype(self, int row)
    cdef void write_dtype(self, object dtype_value)
    cpdef void skip(self)
    cpdef list read(self)
    cpdef unsigned long long write(self, object dtype_values)
    cpdef unsigned long long tell(self)
    cpdef bytes clear(self)
