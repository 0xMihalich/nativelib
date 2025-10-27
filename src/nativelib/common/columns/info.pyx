from nativelib.common.dtypes.objects.array cimport Array
from nativelib.common.dtypes.objects.dtype cimport DType
from nativelib.common.dtypes.objects.lowcardinality cimport LowCardinality
from nativelib.common.dtypes.parse cimport from_dtype
from nativelib.common.length cimport write_length


cdef class ColumnInfo:
    """Column information."""

    def __cinit__(
        self,
        unsigned long long total_rows,
        str column,
        str dtype,
    ):
        """Initialize from native data."""

        cdef bytes bytestring, header = b""
        cdef str string

        for string in (column, dtype):
            bytestring = string.encode("utf-8")
            header += write_length(len(bytestring))
            header += bytestring

        self.header = header
        self.header_length = len(header)
        self.total_rows = total_rows
        self.column = column
        (
        self.dtype,
        self.is_array,
        self.is_lowcardinality,
        self.is_nullable,
        self.length,
        self.precision,
        self.scale,
        self.tzinfo,
        self.enumcase,
        self.nested,
        ) = from_dtype(dtype)

    cpdef object make_dtype(self, object fileobj):
        """Make dtype object."""

        cdef int _i
        cdef object dtype = DType(
            fileobj=fileobj,
            dtype=self.dtype,
            is_nullable=self.is_nullable,
            length=self.length,
            precision=self.precision,
            scale=self.scale,
            tzinfo=self.tzinfo,
            enumcase=self.enumcase,
            total_rows=self.total_rows,
        )

        if self.is_lowcardinality:
            dtype.is_nullable = False
            return LowCardinality(
                fileobj=fileobj,
                dtype=dtype,
                is_nullable=self.is_nullable,
                total_rows=self.total_rows,
            )

        if self.is_array:
            for _i in range(self.nested):
                dtype = Array(
                    fileobj=fileobj,
                    dtype=dtype,
                    total_rows=self.total_rows,
                )

        return dtype
