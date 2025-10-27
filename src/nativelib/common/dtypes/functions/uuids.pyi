from io import BufferedReader
from uuid import UUID


def read_uuid(
    fileobj: BufferedReader,
    length: int | None,
    precision: int | None,
    scale: int | None,
    tzinfo: str | None,
    enumcase: dict[int, str] | None,
) -> UUID:
    """Read UUID from Native Format."""

    ...


def write_uuid(
    dtype_value: UUID,
    length: int | None,
    precision: int | None,
    scale: int | None,
    tzinfo: str | None,
    enumcase: dict[int, str] | None,
) -> bytes:
    """Write UUID into Native Format."""

    ...
