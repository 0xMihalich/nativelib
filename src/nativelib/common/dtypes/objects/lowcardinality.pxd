cdef class LowCardinality:

    cdef public object fileobj
    cdef public object dtype
    cdef public str name
    cdef public object is_nullable
    cdef public unsigned long long total_rows
    cdef public list dictionary
    cdef public list index_elements
    cdef public unsigned char index_size
    cdef public object defaul_value
    cdef public unsigned long long size

    cdef void __index_size(self)
    cdef void __update_index_size(self)
    cpdef void skip(self)
    cpdef list read(self)
    cpdef unsigned long long write(self, object dtype_value)
    cpdef unsigned long long tell(self)
    cpdef bytes clear(self)
    cdef void _cleanup(self)
