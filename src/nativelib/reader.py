from io import BufferedReader
from typing import (
    Any,
    Generator,
)

from pandas import DataFrame as PdFrame
from polars import DataFrame as PlFrame

from .common import (
    BlockReader,
    pandas_astype,
)


class NativeReader:
    """Class for read data from native format."""

    def __init__(
        self,
        fileobj: BufferedReader,
    ) -> None:
        """Class initialization."""

        self.fileobj = fileobj
        self.block_reader = BlockReader(self.fileobj)
        self.total_blocks = 0
        self.total_rows = 0

    def read_info(self) -> None:
        """Read info without reading data."""

        try:
            while 1:
                self.total_rows += self.block_reader.skip()
                self.total_blocks += 1
        except IndexError:
            """End of file."""

    def to_rows(self) -> Generator[Any, None, None]:
        """Convert to python rows."""

        try:
            while 1:
                for dtype_value in self.block_reader.read():
                    yield dtype_value
                    self.total_rows += 1
                self.total_blocks += 1
        except IndexError:
            """End of file."""

    def to_pandas(self) -> PdFrame:
        """Convert to pandas.DataFrame."""

        return PdFrame(
            self.to_rows(),
            columns=self.block_reader.columns,
        ).astype(pandas_astype(self.block_reader.column_list))

    def to_polars(self) -> PlFrame:
        """Convert to polars.DataFrame."""

        return PlFrame(
            self.to_rows(),
            schema=self.block_reader.columns,
            infer_schema_length=None,
        )

    def tell(self) -> int:
        """Return current position."""

        return self.fileobj.tell()

    def close(self) -> None:
        """Close file object."""

        self.fileobj.close()

    def __repr__(self) -> str:
        """String representation in interpreter."""

        return self.__str__()

    def __str__(self) -> str:
        """String representation of NativeReader."""

        def to_col(text: str) -> str:
            """Format string element."""

            text = text[:14] + "…" if len(text) > 15 else text
            return f" {text: <15} "

        if not self.block_reader.column_list:
            self.read_info()

        empty_line = (
            "├─────────────────┼─────────────────┤"
        )
        end_line = (
            "└─────────────────┴─────────────────┘"
        )
        _str = [
            "<Clickhouse Native dump reader>",
            "┌─────────────────┬─────────────────┐",
            "│ Column Name     │ Clickhouse Type │",
            "╞═════════════════╪═════════════════╡",
        ]

        for column in self.block_reader.column_list:
            _str.append(
                f"│{to_col(column.column)}│{to_col(column.dtype.name)}│",
            )
            _str.append(empty_line)

        _str[-1] = end_line
        return "\n".join(_str) + f"""
Total columns: {self.block_reader.total_columns}
Total blocks: {self.total_blocks}
Total rows: {self.total_rows}
"""
