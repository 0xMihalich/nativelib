cdef unsigned long long read_length(object fileobj):
    """Decoding length from ClickHouse Native Format
    (number of columns, number of rows, length of row)."""

    cdef int _i
    cdef unsigned char binary
    cdef unsigned long long length = 0
    cdef unsigned long long shift = 0

    for _i in range(10):
        binary = fileobj.read(1)[0]
        length |= (binary & 0x7f) << shift
        if binary & 0x80 == 0:
            return length
        shift += 7


cdef bytes write_length(unsigned long long length):
    """Encoding length into ClickHouse Native Format
    (number of columns, number of rows, length of row)."""

    cdef int _i
    cdef unsigned long long shift
    cdef list binary = []

    for _i in range(10):
        shift = length & 0x7F
        length >>= 7

        if length > 0:
            shift |= 0x80

        binary.append(shift)

        if length == 0:
            return bytes(binary)
