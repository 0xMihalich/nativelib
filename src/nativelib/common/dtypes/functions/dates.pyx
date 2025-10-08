from libc.math cimport pow
from datetime import (
    date,
    datetime,
    timedelta,
    timezone,
)
from struct import (
    pack,
    unpack,
)

try:
    from zoneinfo import ZoneInfo
except ImportError:
    from backports.zoneinfo import ZoneInfo

from pandas import Timestamp


cdef object DEFAULTDATE = datetime(1970, 1, 1, tzinfo=timezone.utc)
cdef object DEFAULTDATE_NAIVE = datetime(1970, 1, 1)


cdef object unpack_date(long days):
    """Unpack date."""

    cdef object current_datetime = DEFAULTDATE + timedelta(days=days)
    return current_datetime.date()


cdef long pack_date(object dateobj):
    """Pack date into integer."""

    if dateobj.__class__ in (
        datetime,
        Timestamp,
    ):
        dateobj = dateobj.date()

    cdef object current_date = dateobj - DEFAULTDATE.date()
    return current_date.days


cdef object unpack_datetime(object seconds):
    """Unpack timestamp."""

    return DEFAULTDATE + timedelta(seconds=seconds)


cdef object pack_datetime(object datetimeobj):
    """Pack datetime into count seconds or ticks."""

    if datetimeobj.__class__ is Timestamp:
        datetimeobj = datetimeobj.to_pydatetime()
    elif datetimeobj.__class__ is date:
        datetimeobj = datetime.combine(datetimeobj, datetime.min.time())

    cdef object current_datetime

    if datetimeobj.tzinfo is None:
        current_datetime = datetimeobj - DEFAULTDATE_NAIVE
    else:
        current_datetime = datetimeobj.astimezone(timezone.utc) - DEFAULTDATE

    return current_datetime.total_seconds()


cpdef object read_date(
    object fileobj,
    object length,
    object precission,
    object scale,
    object tzinfo,
    object enumcase,
):
    """Read Date from Native Format."""

    cdef bytes date_bytes = fileobj.read(2)
    cdef long days = unpack("<H", date_bytes)[0]
    return unpack_date(days)


cpdef bytes write_date(
    object dtype_value,
    object length,
    object precission,
    object scale,
    object tzinfo,
    object enumcase,
):
    """Write Date into Native Format."""

    if dtype_value is None:
        return bytes(2)

    cdef long days = pack_date(dtype_value)

    if days < 0:
        return bytes(2)
    if days > 0xffff:
        return b"\xff\xff"
    return pack("<H", days)


cpdef object read_date32(
    object fileobj,
    object length,
    object precission,
    object scale,
    object tzinfo,
    object enumcase,
):
    """Read Date32 from Native Format."""

    cdef bytes date_bytes = fileobj.read(4)
    cdef long days = unpack("<l", date_bytes)[0]
    return unpack_date(days)


cpdef bytes write_date32(
    object dtype_value,
    object length,
    object precission,
    object scale,
    object tzinfo,
    object enumcase,
):
    """Write Date32 into Native Format."""

    if dtype_value is None:
        return bytes(4)

    cdef long days = pack_date(dtype_value)
    return pack("<l", days)


cpdef object read_datetime(
    object fileobj,
    object length,
    object precission,
    object scale,
    object tzinfo,
    object enumcase,
):
    """Read DateTime from Native Format."""

    cdef bytes seconds_bytes = fileobj.read(4)
    cdef long seconds = unpack("<l", seconds_bytes)[0]
    cdef object time_zone, datetimeobj = unpack_datetime(seconds)

    if tzinfo:
        time_zone = ZoneInfo(tzinfo)
        return datetimeobj.astimezone(time_zone)
    return datetimeobj


cpdef bytes write_datetime(
    object dtype_value,
    object length,
    object precission,
    object scale,
    object tzinfo,
    object enumcase,
):
    """Write DateTime into Native Format."""

    if dtype_value is None:
        return bytes(4)

    cdef object seconds = pack_datetime(dtype_value)

    if seconds < 0:
        return bytes(4)
    if seconds > 0xffffffff:
        return b"\xff\xff\xff\xff"
    return pack("<l", int(seconds))


cpdef object read_datetime64(
    object fileobj,
    object length,
    unsigned char precission,
    object scale,
    object tzinfo,
    object enumcase,
):
    """Read DateTime64 from Native Format."""

    if not 0 <= precission <= 9:
        raise ValueError("precission must be in [0:9] range!")

    cdef bytes seconds_bytes = fileobj.read(8)
    cdef long long seconds = unpack("<q", seconds_bytes)[0]
    cdef double divider = pow(10, -precission)
    cdef double total_seconds = seconds * divider
    cdef object time_zone, datetime64 = unpack_datetime(total_seconds)

    if tzinfo:
        time_zone = ZoneInfo(tzinfo)
        return datetime64.astimezone(time_zone)
    return datetime64


cpdef bytes write_datetime64(
    object dtype_value,
    object length,
    unsigned char precission,
    object scale,
    object tzinfo,
    object enumcase,
):
    """Write DateTime64 into Native Format."""

    if dtype_value is None:
        return bytes(8)

    if not 0 <= precission <= 9:
        raise ValueError("precission must be in [0:9] range!")

    cdef double seconds = pack_datetime(dtype_value)
    cdef double divider = pow(10, -precission)
    cdef long long total_seconds = <long long>(seconds // divider)

    if total_seconds < 0:
        return bytes(8)
    if total_seconds > 0xffffffffffffffff:
        return b"\xff\xff\xff\xff\xff\xff\xff\xff"
    return pack("<q", total_seconds)
