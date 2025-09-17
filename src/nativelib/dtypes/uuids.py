from io import BufferedIOBase
from struct import (
    pack,
    unpack,
)
from uuid import UUID


def read_uuid(
    file: BufferedIOBase,
    length: int | None = None,
    precission: int | None = None,
    scale: int | None = None,
    tzinfo: str | None = None,
    enum: dict[int, str] | None = None,
) -> UUID:
    """Read UUID from Native Format."""

    return UUID(
        bytes=b"".join(
            unpack("<8s8s", file.read(16))[::-1]
        )[::-1]
    )


def write_uuid(
    dtype_value: UUID,
    file: BufferedIOBase,
    length: int | None = None,
    precission: int | None = None,
    scale: int | None = None,
    tzinfo: str | None = None,
    enum: dict[int, str] | None = None,
) -> None:
    """Write UUID into Native Format."""

    file.write(
        pack(
            "<8s8s",
            dtype_value.bytes[:8][::-1],
            dtype_value.bytes[8:][::-1]),
    )
