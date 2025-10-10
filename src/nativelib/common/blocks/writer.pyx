from nativelib.common.defines import DEFAULT_BLOCK_SIZE
from nativelib.common.length cimport write_length


cdef class BlockWriter:
    """Write block into Native format."""

    def __init__(
        self,
        list column_list,
        unsigned long long max_block_size = DEFAULT_BLOCK_SIZE,
    ) -> None:
        """Class initialization."""

        cdef object column

        self.column_list = column_list
        self.max_block_size = max_block_size
        self.total_columns = len(self.column_list)
        self.total_rows = 0
        self.block_size = 0
        self.headers_size = len(write_length(self.total_columns))
        self.data_iterator = None

        for column in self.column_list:
            self.headers_size += column.info.header_length

    cdef void write_row(self):
        """Write single row."""

        if self.data_iterator is None:
            raise ValueError()

        cdef object column, dtype_value

        for column, dtype_value in zip(
            self.column_list,
            next(self.data_iterator),
        ):
            self.block_size += column.write(dtype_value)

        self.total_rows += 1

    cdef bytes clear_block(self):
        """Return block bytes and clear buffers."""

        cdef list block_bytes = []

        block_bytes.append(write_length(self.total_columns))
        block_bytes.append(write_length(self.total_rows))

        for column in self.column_list:
            block_bytes.append(column.clear())

        self.total_rows = 0
        self.block_size = 0
        return b"".join(block_bytes)

    cpdef void init_dataset(
        self,
        object dtype_values,
    ):
        """Init dataset."""

        self.data_iterator = iter(dtype_values)
        self.total_rows = 0
        self.block_size = 0

    def write(self):
        """Write from rows."""

        cdef unsigned long long total_rows

        try:
            while 1:
                if (
                    self.block_size +
                    self.headers_size +
                    len(write_length(self.total_rows))
                ) >= self.max_block_size:
                    total_rows = self.total_rows
                    yield self.clear_block(), total_rows
                self.write_row()
        except StopIteration:
            if self.total_rows:
                total_rows = self.total_rows
                yield self.clear_block(), total_rows
