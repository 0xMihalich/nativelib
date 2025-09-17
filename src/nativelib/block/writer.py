from io import BufferedWriter
from typing import (
    Any,
    Generator,
)

from pgpack import PGPackReader
from pgpack.metadata import metadata_reader

from ..column import Column
from ..length import write_length
from .defines import DEFAULT_BLOCK_SIZE


class BlockWriter:
    """Write block into Native format."""

    def __init__(
        self,
        file: BufferedWriter,
        column_list: list[Column],
        max_block_size: int = DEFAULT_BLOCK_SIZE,
    ) -> None:
        """Class initialization."""

        self.file = file
        self.column_list = column_list
        self.total_columns = len(self.column_list)
        self.total_rows = 0
        self.max_block_size = max_block_size
        self.block_size = 0
        self.headers_size = sum(
            column.info.header_length
            for column in self.column_list
        ) + len(write_length(self.total_columns))

    @classmethod
    def from_describe(
        cls,
        file: BufferedWriter,
        describe_response: str,
        max_block_size: int = DEFAULT_BLOCK_SIZE,
    ) -> "BlockWriter":
        """Make block writer from describe table response."""

        return cls(
            file=file,
            column_list=[
                Column(
                    file=file,
                    total_rows=0,
                    column=row.split("\t")[0],
                    dtype=row.split("\t")[1],
                )
                for row in describe_response.strip().split("\n")
            ],
            max_block_size=max_block_size,
        )

    @classmethod
    def from_metadata(
        cls,
        file: BufferedWriter,
        metadata: bytes,
        max_block_size: int = DEFAULT_BLOCK_SIZE,
        not_null: bool = False,
    ) -> "BlockWriter":
        """Make block writer from metadata."""

        return cls(
            file=file,
            column_list=[
                Column.from_pgpack_params(
                    file=file,
                    column=column,
                    pgtype=pgtype,
                    pgparam=pgparam,
                    not_null=not_null,
                )
                for column, pgtype, pgparam in zip(
                    *metadata_reader(metadata)
                )
            ],
            max_block_size=max_block_size,
        )

    @classmethod
    def from_pgpack(
        cls,
        file: BufferedWriter,
        pgpack: PGPackReader,
        max_block_size: int = DEFAULT_BLOCK_SIZE,
        not_null: bool = False,
    ) -> "BlockWriter":
        """Make block writer from pgpack object."""

        return cls(
            file=file,
            column_list=[
                Column.from_pgpack_params(
                    file=file,
                    column=column,
                    pgtype=pgtype,
                    pgparam=pgparam,
                    not_null=not_null,
                )
                for column, pgtype, pgparam in zip(
                    pgpack.columns,
                    pgpack.pgtypes,
                    pgpack.pgparam,
                )
            ],
            max_block_size=max_block_size,
        )

    def write_row(
        self,
        dtype_value: Any,
    ) -> None:
        """Write from row."""

        block_size = self.headers_size

        for num in range(self.total_columns):
            block_size += self.column_list[num].write(dtype_value[num])

        self.total_rows += 1
        self.block_size = block_size + len(write_length(self.total_rows))

    def write_rows(
        self,
        dtype_values: list[Any],
    ) -> Generator[bool, None, None]:
        """Write from rows."""

        for dtype_value in dtype_values:
            self.write_row(dtype_value)
            yield self.block_size >= self.max_block_size

    def finalize(self) -> None:
        """Finalize block and refresh values."""

        self.file.write(write_length(self.total_columns))
        self.file.write(write_length(self.total_rows))

        for column in self.column_list:
            column.flush()

        self.total_rows = 0
        self.block_size = 0
