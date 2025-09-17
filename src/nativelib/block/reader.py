from io import BufferedReader
from typing import (
    Any,
    Generator,
)

from pandas import DataFrame as PdFrame
from polars import DataFrame as PlFrame

from ..column import Column
from ..dtypes.strings import read_string
from ..length import read_length
from .frame_type import (
    pandas_dtype,
    polars_dtype,
)


class BlockReader:
    """Read block from Native format."""

    def __init__(
        self,
        file: BufferedReader,
    ) -> None:
        """Class initialization."""

        self.file = file
        self.total_columns: int = 0
        self.total_rows: int = 0
        self.column_list: list[Column] = []
        self.columns: list[str] = []
        self.pandas_dtypes: dict[str, str] = {}
        self.polars_schema: dict[str, object] = {}

    def read_column(self) -> None:
        """Read column."""

        column = read_string(self.file)
        dtype = read_string(self.file)
        column_obj = Column(
            file=self.file,
            total_rows=self.total_rows,
            column=column,
            dtype=dtype,
        )
        column_obj.read()
        self.column_list.append(column_obj)

        if len(self.columns) + 1 <= self.total_columns:
            pytype = column_obj.info.dtype.pytype
            self.columns.append(column_obj.column)
            self.pandas_dtypes[column_obj.column] = pandas_dtype[pytype]
            self.polars_schema[column_obj.column] = polars_dtype[pytype]

    def skip_block(self) -> int:
        """Skip block."""

        self.total_columns = read_length(self.file)
        self.total_rows = read_length(self.file)
        self.column_list = []

        for _ in range(self.total_columns):
            column = read_string(self.file)
            dtype = read_string(self.file)
            column_obj = Column(
                file=self.file,
                total_rows=self.total_rows,
                column=column,
                dtype=dtype,
            )
            column_obj.skip()
            self.column_list.append(column_obj)

        return self.total_rows

    def read_block(self) -> None:
        """Read block."""

        self.total_columns = read_length(self.file)
        self.total_rows = read_length(self.file)
        self.column_list = []

        for _ in range(self.total_columns):
            self.read_column()

    def to_rows(self) -> Generator[tuple[Any], None, None]:
        """Convert to python rows."""

        return zip(*self.column_list)

    def to_pandas(self) -> PdFrame:
        """Convert to pandas.DataFrame."""

        return PdFrame(
            self.to_rows(),
            columns=self.columns,
        ).astype(self.pandas_dtypes)

    def to_polars(self) -> PlFrame:
        """Convert to polars.DataFrame."""

        return PlFrame(
            self.to_rows(),
            schema=self.polars_schema,
        )
