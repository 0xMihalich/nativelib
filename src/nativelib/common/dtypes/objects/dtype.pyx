from nativelib.common.dtypes.functions.booleans cimport (
    read_bool,
    write_bool,
)
from nativelib.common.length cimport read_length


cdef class DType:
    """Clickhouse column data type manipulate."""

    def __init__(
        self,
        object fileobj,
        object dtype,
        object is_nullable,
        object length,
        object precision,
        object scale,
        object tzinfo,
        object enumcase,
        unsigned long long total_rows = 0,
    ):
        """Class initialization."""

        self.fileobj = fileobj
        self.dtype = dtype
        self.name = dtype.name
        self.is_nullable = is_nullable
        self.length = length
        self.precision = precision
        self.scale = scale
        self.tzinfo = tzinfo
        self.enumcase = enumcase
        self.total_rows = total_rows
        self.nullable_map = []
        self.nullable_buffer = []
        self.writable_buffer = []
        self.pos = 0

    cdef object read_dtype(self, int row):
        """Read dtype value from native column."""

        cdef int _
        cdef object dtype_value

        if self.is_nullable and not self.nullable_map:
            for _ in range(self.total_rows):
                self.nullable_map.append(
                    read_bool(self.fileobj)
                )

        dtype_value = self.dtype.read(
            self.fileobj,
            self.length,
            self.precision,
            self.scale,
            self.tzinfo,
            self.enumcase,
        )

        if self.is_nullable and self.nullable_map[row]:
            return
        return dtype_value

    cdef void write_dtype(self, object dtype_value):
        """Write dtype value into native column."""

        cdef bytes obj_value

        if self.is_nullable:
            obj_value = write_bool(dtype_value is None)
            self.pos += len(obj_value)
            self.nullable_buffer.append(obj_value)

        obj_value = self.dtype.write(
            dtype_value,
            self.length,
            self.precision,
            self.scale,
            self.tzinfo,
            self.enumcase,
        )
        self.pos += len(obj_value)
        self.writable_buffer.append(obj_value)
        self.total_rows += 1

    cpdef void skip(self):
        """Skip read native column."""

        cdef int _, length, total_length

        if self.is_nullable:
            self.fileobj.read(self.total_rows)

        if self.length is None:
            for _ in range(self.total_rows):
                length = read_length(self.fileobj)
                self.fileobj.read(length)
        else:
            total_length = self.length * self.total_rows
            self.fileobj.read(total_length)

    cpdef list read(self):
        """Read dtype values from native column."""

        cdef int row
        cdef list dtype_values = []

        for row in range(self.total_rows):
            dtype_values.append(self.read_dtype(row))

        return dtype_values

    cpdef unsigned long long write(self, object dtype_value):
        """Write dtype values into native column."""

        cdef unsigned long long pos = self.pos
        self.write_dtype(dtype_value)
        return self.pos - pos

    cpdef unsigned long long tell(self):
        """Return size of write buffers."""

        return self.pos

    cpdef bytes clear(self):
        """Get column data and clean buffers."""

        cdef bytes data_bytes

        self.nullable_buffer.extend(self.writable_buffer)
        data_bytes = b"".join(self.nullable_buffer)
        self.nullable_buffer.clear()
        self.writable_buffer.clear()

        del self.nullable_map[:]
        self.total_rows = 0
        self.pos = 0

        return data_bytes

    def __dealloc__(self):
        """Destructor for clearing memory."""

        if self.nullable_map is not None:
            self.nullable_map.clear()

        if self.nullable_buffer is not None:
            self.nullable_buffer.clear()

        if self.writable_buffer is not None:
            self.writable_buffer.clear()
