cdef class Array:

    cdef public object fileobj
    cdef public object dtype
    cdef public str name
    cdef public unsigned long long total_rows
    cdef public list row_elements
    cdef public object writable_buffer

    cpdef void skip(self)
    cpdef list read(self)
    cpdef unsigned long long write(self, object dtype_value)
    cpdef unsigned long long tell(self)
    cpdef bytes clear(self)
