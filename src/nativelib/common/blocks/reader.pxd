cdef class BlockReader:

    cdef public object fileobj
    cdef public unsigned long long total_columns
    cdef public unsigned long long total_rows
    cdef public list column_list
    cdef public list columns

    cdef void read_column(self)
    cpdef unsigned long long skip(self)
    cpdef object read(self)
