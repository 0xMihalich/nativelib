"""Reading data from LowCardinality block:

0. Supported data types: String, FixedString, Date, DateTime,
   and numbers excepting Decimal.
1. The number of rows in the header is ignored when working with this format.
2. Skip the 16-byte block; it will not participate in the parser.
3. Read the total number of unique elements in the block as UInt64 (8 bytes).
4. Based on the number obtained in point 3, determine the size of the index:
   UInt8 (1 byte) [0 : 254]
   UInt16 (2 bytes) [255 : 65534]
   UInt32 (4 bytes) [65535 : 4294967294]
   UInt64 (8 bytes) [4294967295 : 18446744073709551615]
5. Read all elements as a dictionary: key = index starting from 0, value = element.
   The first element always writes the default value for the specified data type.
   If Nullable is additionally specified
   [for example, LowCardinality(Nullable(String))],
   the first two values will be default,
   but the element with index 0 corresponds to None,
   and the element with index 1 corresponds to the default
   value for this data type (an empty string).
6. Read the total number of elements in the block as UInt64 (8 bytes).
   This parameter corresponds to the number of rows in the header.
7. Read the index of each element according to the size obtained in point 4
   and relate it to the value in the dictionary.
"""

from datetime import (
    date,
    datetime,
)

from nativelib.common.dtypes.functions.integers cimport (
    r_uint,
    w_uint,
)


cdef str FIXEDSTRING = "FixedString"
cdef object NON_STR = ""
cdef object NON_INT = 0
cdef object NON_FLOAT = 0.0
cdef dict DEFAULT_VALUE = {
    "String": NON_STR,
    "Date": date(1970, 1, 1),
    "DateTime": datetime(1970, 1, 1),
    "FixedString": NON_STR,
    "Float32": NON_FLOAT,
    "Float64": NON_FLOAT,
    "Int128": NON_INT,
    "Int16": NON_INT,
    "Int256": NON_INT,
    "Int32": NON_INT,
    "Int64": NON_INT,
    "Int8": NON_INT,
    "UInt128": NON_INT,
    "UInt16": NON_INT,
    "UInt256": NON_INT,
    "UInt32": NON_INT,
    "UInt64": NON_INT,
    "UInt8": NON_INT,
}
cdef dict INDEX_SIZE = {
    0: 1,  # UInt8
    1: 2,  # UInt16
    2: 4,  # UInt32
    3: 8,  # UInt64
}


cdef unsigned char find_index_size(unsigned long long total_rows):
    """Detect index size."""

    if total_rows < 0:
        raise ValueError("Non uint value!")
    if total_rows <= 0xff:
        return 1
    if total_rows <= 0xffff:
        return 2
    if total_rows <= 0xffffffff:
        return 4
    return 8


cdef unsigned char size_from_header(object fileobj):
    """Get index size from header."""

    cdef bytes bynary = fileobj.read(16)
    cdef unsigned char index = bynary[8]
    return INDEX_SIZE[index]


cdef bytes generate_header(unsigned char index_size):
    """Generate LowCardinality header from count elements."""

    cdef unsigned char key, value
    cdef list header = [1, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0]

    for key, value in INDEX_SIZE.items():
        if index_size == value:
            header[8] = key
            return bytes(header)

    raise ValueError(f"Unknown index size {index_size}")


cdef class LowCardinality:
    """Class for unpacking data from
    the LowCardinality block into a regular
    Data Type (String, FixedString, Date, DateTime,
    and numbers excepting Decimal)."""

    def __init__(
        self,
        object fileobj,
        object dtype,
        object is_nullable,
        unsigned long long total_rows = 0,
    ):
        """Class initialization."""

        self.fileobj = fileobj
        self.dtype = dtype
        self.name = f"LowCardinality({dtype.name})"
        self.is_float = int("Float" in dtype.name)
        self.is_nullable = is_nullable
        self.total_rows = total_rows
        self.dictionary = []
        self.index_elements = []
        self.index_size = 0
        self.defaul_value = DEFAULT_VALUE[self.dtype.name]
        self.dtype.is_nullable = False
        self.size = 0

    cdef void __index_size(self):
        """Get index_size."""

        if not self.index_size:
            self.index_size = size_from_header(self.fileobj)
            self.dtype.total_rows = r_uint(self.fileobj, 8)

    cdef void __update_index_size(self):
        """Update index_size."""

        self.index_size = find_index_size(self.total_rows)

    cpdef void skip(self):
        """Skip read native column."""

        self.__index_size()
        self.dtype.skip()
        self.total_rows = r_uint(self.fileobj, 8)
        self.fileobj.read(self.index_size * self.total_rows)

    cpdef list read(self):
        """Read lowcardinality values from native column."""

        cdef object dtype_value
        cdef list dtype_values = []
        cdef int _i
        cdef unsigned long long row_index

        self.__index_size()
        self.dictionary = self.dtype.read()

        if self.is_nullable:
            self.dictionary[0] = None

        self.total_rows = r_uint(self.fileobj, 8)

        for _i in range(self.total_rows):
            row_index = r_uint(self.fileobj, self.index_size)
            dtype_values.append(self.dictionary[row_index])

        return dtype_values

    cpdef unsigned long long write(self, object dtype_value):
        """Write lowcardinality values into native column."""

        cdef unsigned long long size

        if self.is_float == 0 and dtype_value != dtype_value:
            dtype_value = None

        if not self.total_rows:
            self.dictionary.clear()
            self.index_elements.clear()
            self.total_rows = 0
            self.dtype.total_rows = 0
            self.index_size = 1
            self.size = 32

            if self.is_nullable:
                self.size += self.dtype.write(None)
                self.dictionary.append(None)

            self.size += self.dtype.write(None)
            self.dictionary.append(self.defaul_value)
            size = 0
        else:
            size = self.index_size * self.total_rows + self.size

        if not self.is_nullable and dtype_value is None:
            dtype_value = self.defaul_value

        if self.dtype.name == FIXEDSTRING:
            dtype_value = dtype_value[:self.dtype.length]

        self.index_elements.append(dtype_value)
        self.total_rows += 1

        if dtype_value not in self.dictionary:
            self.dictionary.append(dtype_value)
            self.size += self.dtype.write(dtype_value)

        self.index_size = find_index_size(self.total_rows)
        return self.index_size * self.total_rows + self.size - size

    cpdef unsigned long long tell(self):
        """Return size of write values."""

        self.__update_index_size()
        return self.index_size * self.total_rows + self.dtype.pos + 32

    cpdef bytes clear(self):
        """Get column data and clean buffers."""

        cdef list buffer_bytes = []
        cdef bytes buffer_element
        cdef object dict_element, index_element

        self.__update_index_size()

        buffer_element = generate_header(self.index_size)
        buffer_bytes.append(buffer_element)

        self.dtype.clear()
        self.dictionary = [self.dictionary[0], *sorted(self.dictionary[1:])]

        buffer_element = w_uint(len(self.dictionary), 8)
        buffer_bytes.append(buffer_element)

        for dict_element in self.dictionary:
            self.dtype.write(dict_element)

        buffer_element = self.dtype.clear()
        buffer_bytes.append(buffer_element)

        buffer_element = w_uint(self.total_rows, 8)
        buffer_bytes.append(buffer_element)

        for index_element in self.index_elements:
            buffer_element = w_uint(
                self.dictionary.index(index_element),
                self.index_size,
            )
            buffer_bytes.append(buffer_element)

        self.dictionary.clear()
        self.index_elements.clear()
        self.total_rows = 0
        self.dtype.total_rows = 0
        self.index_size = 1
        self.size = 0
        return b"".join(buffer_bytes)
