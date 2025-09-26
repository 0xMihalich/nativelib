cdef class Column:

    cdef public str column
    cdef public object fileobj
    cdef public object info
    cdef public object dtype
    cdef public object data
    cdef public object iter_data
    cdef public unsigned long long pos

    cpdef void skip(self)
    cpdef list read(self)
    cpdef unsigned long long write(self, object data)
    cpdef unsigned long long tell(self)
    cpdef bytes clear(self)
