from datetime import (
    date,
    datetime,
    timedelta,
    timezone,
)
from io import (
    BufferedReader,
    BufferedWriter,
)
from struct import (
    pack,
    unpack,
)
from typing import Union

try:
    from zoneinfo import ZoneInfo
except ImportError:
    from backports.zoneinfo import ZoneInfo  # type: ignore


DefaultDate = datetime(1970, 1, 1, tzinfo=timezone.utc)


def unpack_date(days: int) -> date:
    """Unpack date."""

    return (DefaultDate + timedelta(days=days)).date()


def pack_date(dateobj: date) -> int:
    """Pack date into integer."""

    return (dateobj - DefaultDate.date()).days


def unpack_datetime(seconds: Union[int, float]) -> datetime:
    """Unpack timestamp."""

    return DefaultDate + timedelta(seconds=seconds)


def pack_datetime(datetimeobj: datetime) -> Union[int, float]:
    """Pack datetime into count seconds or ticks."""

    return (
        datetimeobj.astimezone(timezone.utc) - DefaultDate
    ).total_seconds()


def read_date(
    file: BufferedReader,
    length: int | None = None,
    precission: int | None = None,
    scale: int | None = None,
    tzinfo: str | None = None,
    enum: dict[int, str] | None = None,
) -> date:
    """Read Date from Native Format."""

    return unpack_date(unpack("<H", file.read(2))[0])


def write_date(
    dtype_value: date,
    file: BufferedWriter,
    length: int | None = None,
    precission: int | None = None,
    scale: int | None = None,
    tzinfo: str | None = None,
    enum: dict[int, str] | None = None,
) -> None:
    """Write Date into Native Format."""

    file.write(pack("<H", pack_date(dtype_value)))


def read_date32(
    file: BufferedReader,
    length: int | None = None,
    precission: int | None = None,
    scale: int | None = None,
    tzinfo: str | None = None,
    enum: dict[int, str] | None = None,
) -> date:
    """Read Date32 from Native Format."""

    return unpack_date(unpack("<l", file.read(4))[0])


def write_date32(
    dtype_value: date,
    file: BufferedWriter,
    length: int | None = None,
    precission: int | None = None,
    scale: int | None = None,
    tzinfo: str | None = None,
    enum: dict[int, str] | None = None,
) -> None:
    """Write Date32 into Native Format."""

    file.write(pack("<l", pack_date(dtype_value)))


def read_datetime(
    file: BufferedReader,
    length: int | None = None,
    precission: int | None = None,
    scale: int | None = None,
    tzinfo: str = "UTC",
    enum: dict[int, str] | None = None,
) -> datetime:
    """Read DateTime from Native Format."""

    dtype_value = unpack_datetime(unpack("<l", file.read(4))[0])

    if tzinfo:
        return dtype_value.astimezone(ZoneInfo(tzinfo))

    return dtype_value


def write_datetime(
    dtype_value: datetime,
    file: BufferedWriter,
    length: int | None = None,
    precission: int | None = None,
    scale: int | None = None,
    tzinfo: str | None = None,
    enum: dict[int, str] | None = None,
) -> None:
    """Write DateTime into Native Format."""

    seconds = int(pack_datetime(dtype_value))
    file.write(pack("<l", seconds))


def read_datetime64(
    file: BufferedReader,
    length: int | None = None,
    precission: int = 0,
    scale: int | None = None,
    tzinfo: str = "UTC",
    enum: dict[int, str] | None = None,
) -> datetime:
    """Read DateTime64 from Native Format."""

    if not 0 <= precission < 9:
        raise ValueError("precission must be in [0:9] range!")
    if not isinstance(precission, int):
        raise ValueError("precission must be an integer!")

    seconds: int = unpack("<q", file.read(8))[0]
    datetime64 = unpack_datetime(seconds * pow(10, -precission))

    if tzinfo:
        return datetime64.astimezone(ZoneInfo(tzinfo))

    return datetime64


def write_datetime64(
    dtype_value: datetime,
    file: BufferedWriter,
    length: int | None = None,
    precission: int = 0,
    scale: int | None = None,
    tzinfo: str | None = None,
    enum: dict[int, str] | None = None,
) -> None:
    """Write DateTime64 into Native Format."""

    seconds: int = int(pack_datetime(dtype_value)) // pow(10, -precission)
    file.write(pack("<q", seconds))
