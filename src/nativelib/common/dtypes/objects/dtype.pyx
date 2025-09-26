from io import BytesIO

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
        object precission,
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
        self.precission = precission
        self.scale = scale
        self.tzinfo = tzinfo
        self.enumcase = enumcase
        self.total_rows = total_rows
        self.nullable_map = []
        self.nullable_buffer = BytesIO()
        self.writable_buffer = BytesIO()
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
            self.precission,
            self.scale,
            self.tzinfo,
            self.enumcase,
        )

        if self.is_nullable and self.nullable_map[row]:
            return
        return dtype_value

    cdef void write_dtype(self, object dtype_value):
        """Write dtype value into native column."""

        if self.is_nullable:
            self.pos += self.nullable_buffer.write(
                write_bool(dtype_value is None)
            )
        self.pos += self.writable_buffer.write(
            self.dtype.write(
            dtype_value,
            self.length,
            self.precission,
            self.scale,
            self.tzinfo,
            self.enumcase,
        ))
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

        cdef object _buffer
        cdef list data_bytes = []

        for _buffer in (
            self.nullable_buffer,
            self.writable_buffer,
        ):
            data_bytes.append(_buffer.getvalue())
            _buffer.seek(0)
            _buffer.truncate()

        self.total_rows = 0
        self.pos = 0
        return b"".join(data_bytes)
