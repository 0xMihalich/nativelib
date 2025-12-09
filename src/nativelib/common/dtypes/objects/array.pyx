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
        self.is_float = int("Float" in self.name)
        self.total_rows = total_rows
        self.row_elements = []
        self.writable_buffer = []
        self.pos = 0

    cpdef void skip(self):
        """Skip read native column."""

        self.fileobj.read(8 * (self.total_rows - 1))
        self.dtype.total_rows = r_uint(self.fileobj, 8)
        self.dtype.skip()

    cpdef list read(self):
        """Read array values from native column."""

        cdef int _i
        cdef unsigned long long row_element, from_element = 0
        cdef list array_elements = []

        for _i in range(self.total_rows):
            self.row_elements.append(r_uint(self.fileobj, 8))

        for row_element in self.row_elements:
            self.dtype.total_rows = row_element - from_element
            array_elements.append(self.dtype.read())
            from_element = row_element

        return array_elements

    cpdef unsigned long long write(self, object dtype_value):
        """Write array values into native column."""

        cdef object array_element, buffer_element
        cdef unsigned long long pos = self.pos

        for array_element in dtype_value:

            if self.is_float == 0 and array_element != array_element:
                array_element = None

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

        cdef bytes data_bytes = b"".join(self.writable_buffer)
        self.total_rows = 0
        self.row_elements.clear()
        self.writable_buffer.clear()
        return data_bytes + self.dtype.clear()
