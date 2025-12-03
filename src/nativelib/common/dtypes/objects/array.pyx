from nativelib.common.dtypes.functions.integers cimport (
    r_uint,
    w_uint,
)


cdef class Array:
    """Clickhouse column array type manipulate."""

    def __init__(
        self,
        object fileobj,
        object dtype,
        unsigned long long total_rows = 0,
    ):
        """Class initialization."""

        self.fileobj = fileobj
        self.dtype = dtype
        self.name = f"Array({dtype.name})"
        self.total_rows = total_rows
        self.row_elements = []
        self.writable_buffer = []
        self.pos = 0

    cpdef void skip(self):
        """Skip read native column."""

        cdef unsigned long long i, elements_count

        for i in range(self.total_rows - 1):
            r_uint(self.fileobj, 8)

        elements_count = r_uint(self.fileobj, 8)
        self.dtype.total_rows = elements_count
        self.dtype.skip()

    cpdef list read(self):
        """Read array values from native column."""

        cdef int i
        cdef unsigned long long row_element, from_element = 0
        cdef list array_elements = []

        self.row_elements.clear()

        for i in range(self.total_rows):
            self.row_elements.append(r_uint(self.fileobj, 8))

        for row_element in self.row_elements:
            self.dtype.total_rows = row_element - from_element
            array_elements.append(self.dtype.read())
            from_element = row_element

        self.row_elements.clear()
        return array_elements

    cpdef unsigned long long write(self, object dtype_value):
        """Write array values into native column."""

        cdef object array_element
        cdef bytes buffer_element
        cdef unsigned long long pos = self.pos

        for array_element in dtype_value:
            self.pos += self.dtype.write(array_element)

        buffer_element = w_uint(self.dtype.total_rows, 8)
        self.pos += 8
        self.writable_buffer.append(buffer_element)
        self.total_rows += 1
        return self.pos - pos

    cpdef unsigned long long tell(self):
        """Return size of write buffers."""

        return self.pos

    cpdef bytes clear(self):
        """Get column data and clean buffers."""

        cdef bytes data_bytes, dtype_data

        data_bytes = b"".join(self.writable_buffer)
        self.writable_buffer.clear()
        self.row_elements.clear()
        dtype_data = self.dtype.clear()
        self.total_rows = 0
        self.pos = 0

        return data_bytes + dtype_data

    def __dealloc__(self):
        """Destructor for clearing memory."""

        if self.row_elements is not None:
            self.row_elements.clear()

        if self.writable_buffer is not None:
            self.writable_buffer.clear()
