from io import (
    BufferedReader,
    BufferedWriter,
)
from json import dumps
from typing import (
    Any,
    Generator,
)
from struct import error as EOFError

from pandas import DataFrame as PdFrame
from polars import DataFrame as PlFrame
from pgcopylib import (
    PGOid,
    PGCopyWriter,
)

from .associate import (
    DTypeToOid,
    OidLength,
    OidToArray,
)
from .block import BlockReader


class NativeReader:
    """Class for read data from native format."""

    def __init__(
        self,
        fileobj: BufferedReader,
    ) -> None:
        """Class initialization."""

        self.fileobj = fileobj
        self.block = BlockReader(self.fileobj)
        self.pgtypes: list[PGOid] = []
        self.total_blocks = 0
        self.total_rows = 0

    def read_info(self) -> None:
        """Read info without reading data."""

        try:
            while 1:
                self.total_rows += self.block.skip_block()
                self.total_blocks += 1
        except EOFError:
            return

    def init_first_block(self) -> None:
        """Read first block to make pgtypes."""

        self.fileobj.seek(0)
        self.block.read_block()
        self.pgtypes = [
            PGOid(OidToArray[DTypeToOid[column.info.dtype.name]])
            if column.info.is_array
            else PGOid(DTypeToOid[column.info.dtype.name])
            for column in self.block.column_list
        ]
        self.total_blocks = 1
        self.total_rows = 0

    def to_rows(self) -> Generator[Any, None, None]:
        """Convert to python rows."""

        try:
            if not self.pgtypes:
                self.init_first_block()
            while 1:
                for dtype_value in self.block.to_rows():
                    yield dtype_value
                    self.total_rows += 1
                self.block.read_block()
                self.total_blocks += 1
        except EOFError:
            return

    def to_pandas(self) -> PdFrame:
        """Convert to pandas.DataFrame."""

        self.init_first_block()

        return PdFrame(
            self.to_rows(),
            columns=self.block.columns,
        ).astype(self.block.pandas_dtypes)

    def to_polars(self) -> PlFrame:
        """Convert to polars.DataFrame."""

        if not self.block.column_list:
            self.init_first_block()

        return PlFrame(
            self.to_rows(),
            schema=self.block.polars_schema,
        )

    def to_pgcopy(
        self,
        fileobj: BufferedWriter,
    ) -> int:
        """Save as pgcopy bynary dump."""

        self.init_first_block()

        writer = PGCopyWriter(
            file=fileobj,
            pgtypes=self.pgtypes,
        )
        writer.write(self.to_rows())
        writer.finalize()
        return writer.tell()

    @property
    def pgpack_metadata(self) -> bytes:
        """Make metadata object for pgpack."""

        if not self.block.column_list:
            self.init_first_block()

        metadata: list[int, list[str, int]] = []

        for number, column in enumerate(self.block.column_list, 1):
            name = column.column
            oid = DTypeToOid[column.info.dtype.name]

            if column.info.is_array:
                oid = OidToArray[oid]

            lengths = OidLength.get(oid) or -1
            scale = column.info.scale or 0
            nested = column.info.nested or 0

            if oid == 1700:
                lengths = column.info.precission
            elif oid == 1042:
                lengths = column.info.length

            metadata.append([
                number, [name, oid, lengths, scale, nested]
            ])

        return dumps(metadata, ensure_ascii=False).encode("utf-8")

    def __repr__(self) -> str:
        """String representation in interpreter."""

        return self.__str__()

    def __str__(self) -> str:
        """String representation of NativeWriter."""

        def to_col(text: str) -> str:
            """Format string element."""

            text = text[:14] + "…" if len(text) > 15 else text
            return f" {text: <15} "

        if not self.block.column_list:
            self.read_info()

        empty_line = (
            "│-----------------+-----------------│"
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

        for column in self.block.column_list:
            _str.append(
                f"│{to_col(column.column)}│{to_col(column.dtype.name)}│",
            )
            _str.append(empty_line)

        _str[-1] = end_line
        return "\n".join(_str) + f"""
Total columns: {len(self.block.column_list)}
Total blocks: {self.total_blocks}
Total rows: {self.total_rows}
"""
