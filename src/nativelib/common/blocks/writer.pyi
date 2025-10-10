from collections.abc import Generator
from typing import (
    Any,
    Iterable,
    Iterator,
)

from ..columns import Column
from ..defines import DEFAULT_BLOCK_SIZE


class BlockWriter:
    """Write block into Native format."""

    def __init__(
        self,
        column_list: list[Column],
        max_block_size: int = DEFAULT_BLOCK_SIZE,
    ) -> None:
        """Class initialization."""

        self.column_list: list[Column]
        self.max_block_size: int
        self.total_columns: int
        self.total_rows: int
        self.block_size: int
        self.headers_size: int
        self.data_iterator: Iterator[Any] | None
        ...

    def write_row(self) -> None:
        """Write single row."""

        ...

    def clear_block(self) -> bytes:
        """Return block bytes and clear buffers."""

        ...

    def init_dataset(
        self,
        dtype_values: Iterable[Any],
    ) -> None:
        """Init dataset."""

        ...

    def write(self) -> Generator[bytes, None, None]:
        """Write from rows."""

        ...
