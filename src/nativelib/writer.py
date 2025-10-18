from collections.abc import Generator
from typing import Any, Iterable

from pandas import DataFrame as PdFrame
from polars import DataFrame as PlFrame

from .common import (
    BlockWriter,
    Column,
    DEFAULT_BLOCK_SIZE,
)


class NativeWriter:
    """Class for write data into native format."""

    def __init__(
        self,
        column_list: list[Column],
        block_size: int = DEFAULT_BLOCK_SIZE,
    ) -> None:
        """Class initialization."""

        self.column_list = column_list
        self.block_size = block_size
        self.block_writer = BlockWriter(column_list, block_size)
        self.total_blocks = 0
        self.total_rows = 0

    def from_rows(
        self,
        dtype_data: Iterable[Any],
    ) -> Generator[bytes, None, None]:
        """Convert python rows to native format."""

        self.block_writer.init_dataset(dtype_data)

        for block, total_rows in self.block_writer.write():
            self.total_rows += total_rows
            self.total_blocks += 1
            yield block

    def from_pandas(
        self,
        data_frame: PdFrame,
    ) -> Generator[bytes, None, None]:
        """Convert pandas.DataFrame to native format."""

        return self.from_rows(iter(data_frame.values))

    def from_polars(
        self,
        data_frame: PlFrame,
    ) -> Generator[bytes, None, None]:
        """Convert polars.DataFrame to native format."""

        return self.from_rows(data_frame.iter_rows())

    def __repr__(self) -> str:
        """String representation in interpreter."""

        return self.__str__()

    def __str__(self) -> str:
        """String representation of NativeWriter."""

        def to_col(text: str) -> str:
            """Format string element."""

            text = text[:14] + "…" if len(text) > 15 else text
            return f" {text: <15} "

        empty_line = (
            "├─────────────────┼─────────────────┤"
        )
        end_line = (
            "└─────────────────┴─────────────────┘"
        )
        _str = [
            "<Clickhouse Native dump writer>",
            "┌─────────────────┬─────────────────┐",
            "│ Column Name     │ Clickhouse Type │",
            "╞═════════════════╪═════════════════╡",
        ]

        for column in self.column_list:
            _str.append(
                f"│{to_col(column.column)}│{to_col(column.dtype.name)}│",
            )
            _str.append(empty_line)

        _str[-1] = end_line
        return "\n".join(_str) + f"""
Total columns: {len(self.column_list)}
Total blocks: {self.total_blocks}
Total rows: {self.total_rows}
"""
