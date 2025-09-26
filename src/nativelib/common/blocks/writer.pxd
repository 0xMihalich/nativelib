cdef class BlockWriter:

    cdef public list column_list
    cdef public unsigned long long max_block_size
    cdef public unsigned long long total_columns
    cdef public unsigned long long total_rows
    cdef public unsigned long long block_size
    cdef public unsigned long long headers_size
    cdef public object data_iterator

    cdef void write_row(self)
    cdef bytes clear_block(self)
    cpdef void init_dataset(
        self,
        object dtype_values,
    )
