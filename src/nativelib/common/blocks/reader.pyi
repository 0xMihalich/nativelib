from collections.abc import Generator
from io import BufferedReader
from typing import Any

from ..columns import Column


class BlockReader:
    """Read block from Native format."""

    def __init__(
        self,
        fileobj: BufferedReader,
    ) -> None:
        """Class initialization."""

        self.fileobj: BufferedReader
        self.total_columns: int
        self.total_rows: int
        self.column_list: list[Column]
        self.columns: list[str]
        ...

    def read_column(self) -> None:
        """Read single column."""

        ...

    def skip(self) -> int:
        """Skip block."""

        ...

    def read(self) -> Generator[tuple[Any], None, None]:
        """Read block into python rows."""

        ...
