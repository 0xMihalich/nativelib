from io import BufferedReader


def read_length(fileobj: BufferedReader) -> int:
    """Decoding length from ClickHouse Native Format
    (number of columns, number of rows, length of row)."""

    ...


def write_length(length: int) -> bytes:
    """Encoding length into ClickHouse Native Format
    (number of columns, number of rows, length of row)."""

    ...
