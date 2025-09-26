from nativelib.common.columns.info cimport ColumnInfo


cdef class Column:
    """Column object."""

    def __init__(
        self,
        str column,
        str dtype,
        object fileobj = None,
        unsigned long long total_rows = 0,
    ) -> None:
        """Class initialization."""

        self.column = column
        self.fileobj = fileobj
        self.info = ColumnInfo(
            total_rows=total_rows,
            column=self.column,
            dtype=dtype,
        )
        self.dtype = self.info.make_dtype(fileobj=self.fileobj)
        self.data = None
        self.iter_data = None
        self.pos = 0

    @property
    def total_rows(self):
        """Get total rows."""

        return self.dtype.total_rows

    def __iter__(self):
        """Iterator method."""

        self.read()
        self.iter_data = iter(self.data)
        return self

    def __next__(self):
        """Next method."""

        return next(self.iter_data)

    cpdef void skip(self):
        """Skip read native column."""

        self.dtype.skip()

    cpdef list read(self):
        """Read data from column."""

        if not self.data:
            self.data = self.dtype.read()

        return self.data

    cpdef unsigned long long write(self, object data):
        """Write data into column."""

        cdef unsigned long long pos = self.pos

        if not self.pos:
            self.pos = self.info.header_length

        self.pos += self.dtype.write(data)
        return self.pos - pos

    cpdef unsigned long long tell(self):
        """Return current size."""

        return self.info.header_length + self.dtype.tell()

    cpdef bytes clear(self):
        """Get column data and clean."""

        cdef list bytes_buffer = [self.info.header]
        bytes_buffer.append(self.dtype.clear())
        return b"".join(bytes_buffer)
