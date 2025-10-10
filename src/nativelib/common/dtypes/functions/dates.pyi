from datetime import (
    date,
    datetime,
)
from io import BufferedReader

from pandas import Timestamp


def read_date(
    fileobj: BufferedReader,
    length: int | None,
    precission: int | None,
    scale: int | None,
    tzinfo: str | None,
    enumcase: dict[int, str] | None,
) -> date:
    """Read Date from Native Format."""

    ...


def write_date(
    dtype_value: date | datetime | Timestamp,
    length: int | None,
    precission: int | None,
    scale: int | None,
    tzinfo: str | None,
    enumcase: dict[int, str] | None,
) -> bytes:
    """Write Date into Native Format."""

    ...


def read_date32(
    fileobj: BufferedReader,
    length: int | None,
    precission: int | None,
    scale: int | None,
    tzinfo: str | None,
    enumcase: dict[int, str] | None,
) -> date:
    """Read Date32 from Native Format."""

    ...


def write_date32(
    dtype_value: date | datetime | Timestamp,
    length: int | None,
    precission: int | None,
    scale: int | None,
    tzinfo: str | None,
    enumcase: dict[int, str] | None,
) -> bytes:
    """Write Date32 into Native Format."""

    ...


def read_datetime(
    fileobj: BufferedReader,
    length: int | None,
    precission: int | None,
    scale: int | None,
    tzinfo: str | None,
    enumcase: dict[int, str] | None,
) -> datetime:
    """Read DateTime from Native Format."""

    ...


def write_datetime(
    dtype_value: date | datetime | Timestamp,
    length: int | None,
    precission: int | None,
    scale: int | None,
    tzinfo: str | None,
    enumcase: dict[int, str] | None,
) -> bytes:
    """Write DateTime into Native Format."""

    ...


def read_datetime64(
    fileobj: BufferedReader,
    length: int | None,
    precission: int,
    scale: int | None,
    tzinfo: str | None,
    enumcase: dict[int, str] | None,
) -> datetime:
    """Read DateTime64 from Native Format."""

    ...


def write_datetime64(
    dtype_value: date | datetime | Timestamp,
    length: int | None,
    precission: int,
    scale: int | None,
    tzinfo: str | None,
    enumcase: dict[int, str] | None,
) -> bytes:
    """Write DateTime64 into Native Format."""

    ...
