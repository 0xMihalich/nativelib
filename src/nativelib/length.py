from io import BufferedReader
from struct import unpack


def read_length(file: BufferedReader) -> int:
    """Decoding length from ClickHouse Native Format
    (number of columns, number of rows, length of row)."""

    shift = 0
    length = 0

    for _ in range(10):
        binary = unpack("<b", file.read(1))[0]
        length |= (binary & 0x7F) << shift

        if binary & 0x80 == 0:
            return length

        shift += 7


def write_length(length: int) -> bytes:
    """Encoding length into ClickHouse Native Format
    (number of columns, number of rows, length of row)."""

    binary = b""

    for _ in range(10):
        shift = length & 0x7F
        length >>= 7

        if length > 0:
            shift |= 0x80

        binary += bytes([shift])

        if length == 0:
            return binary
