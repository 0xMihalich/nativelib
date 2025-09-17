from io import BufferedWriter
from typing import Any

from pgpack import PGPackReader
from pandas import DataFrame as PdFrame
from polars import DataFrame as PlFrame

from .block import (
    BlockWriter,
    DEFAULT_BLOCK_SIZE,
)
from .column import Column


class NativeWriter:
    """Class for write data into native format."""

    def __init__(
        self,
        fileobj: BufferedWriter,
        column_list: list[Column] = [],
        block_size: int = DEFAULT_BLOCK_SIZE,
    ) -> None:
        """Class initialization."""

        self.fileobj = fileobj
        self.column_list = column_list
        self.block_size = block_size
        self.block: BlockWriter | None = None
        self.total_blocks = 0
        self.total_rows = 0

        if self.column_list:
            self.block = BlockWriter(
                file=self.fileobj,
                column_list=self.column_list,
                max_block_size=self.block_size,
            )

    def block_from_describe(
        self,
        describe_response: str,
    ) -> None:
        """Init block writer from describe table response."""

        self.block = BlockWriter.from_describe(
            file=self.fileobj,
            describe_response=describe_response,
            max_block_size=self.block_size,
        )
        self.column_list = self.block.column_list

    def block_from_metadata(
        self,
        metadata: bytes,
    ) -> None:
        """Init block writer from metadata."""

        self.block = BlockWriter.from_metadata(
            file=self.fileobj,
            metadata=metadata,
            max_block_size=self.block_size,
        )
        self.column_list = self.block.column_list

    def block_from_pgpack(
        self,
        pgpack: PGPackReader,
        not_null: bool = False,
    ) -> None:
        """Init block writer from pgpack object."""

        self.block = BlockWriter.from_pgpack(
            file=self.fileobj,
            pgpack=pgpack,
            max_block_size=self.block_size,
            not_null=not_null,
        )
        self.column_list = self.block.column_list

    def from_pgpack(
        self,
        pgpack: PGPackReader,
        not_null: bool = False,
    ) -> None:
        """Convert pgpack to native format."""

        self.block_from_pgpack(pgpack, not_null)
        self.from_rows(pgpack.pgcopy.read_raws())

    def from_rows(
        self,
        *dtype_data: list[Any],
    ) -> None:
        """Convert python rows to native format."""

        if not self.block:
            raise ModuleNotFoundError("Native block not defined.")

        for is_full in self.block.write_rows(*dtype_data):
            self.total_rows += 1
            if is_full:
                self.block.finalize()
                self.total_blocks += 1

        if self.block.total_rows > 0:
            self.block.finalize()
            self.total_blocks += 1

    def from_pandas(
        self,
        data_frame: PdFrame,
    ) -> None:
        """Convert pandas.DataFrame to native format."""

        self.from_rows(*data_frame.values)

    def from_polars(
        self,
        data_frame: PlFrame,
    ) -> None:
        """Convert polars.DataFrame to native format."""

        self.from_rows(data_frame.iter_rows())

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
            "│-----------------+-----------------│"
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
