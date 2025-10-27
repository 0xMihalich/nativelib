from libc.math cimport pow
from datetime import (
    date,
    datetime,
    time,
    timedelta,
    timezone,
)
from decimal import Decimal
from struct import (
    pack,
    unpack,
)

try:
    from zoneinfo import ZoneInfo
except ImportError:
    from backports.zoneinfo import ZoneInfo

from pandas import Timestamp

from nativelib.common.dtypes.functions.decimals cimport (
    read_decimal,
    write_decimal,
)


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
    object precision,
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
    object precision,
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
    object precision,
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
    object precision,
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
    object precision,
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
    object precision,
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
    unsigned char precision,
    object scale,
    object tzinfo,
    object enumcase,
):
    """Read DateTime64 from Native Format."""

    if not 0 <= precision <= 9:
        raise ValueError("precision must be in [0:9] range!")

    cdef bytes seconds_bytes = fileobj.read(8)
    cdef long long seconds = unpack("<q", seconds_bytes)[0]
    cdef double divider = pow(10, -precision)
    cdef double total_seconds = seconds * divider
    cdef object time_zone, datetime64 = unpack_datetime(total_seconds)

    if tzinfo:
        time_zone = ZoneInfo(tzinfo)
        return datetime64.astimezone(time_zone)
    return datetime64


cpdef bytes write_datetime64(
    object dtype_value,
    object length,
    unsigned char precision,
    object scale,
    object tzinfo,
    object enumcase,
):
    """Write DateTime64 into Native Format."""

    if dtype_value is None:
        return bytes(8)

    if not 0 <= precision <= 9:
        raise ValueError("precision must be in [0:9] range!")

    cdef double seconds = pack_datetime(dtype_value)
    cdef double divider = pow(10, -precision)
    cdef long long total_seconds = <long long>(seconds // divider)

    if total_seconds < 0:
        return bytes(8)
    if total_seconds > 0xffffffffffffffff:
        return b"\xff\xff\xff\xff\xff\xff\xff\xff"
    return pack("<q", total_seconds)


cpdef object read_time(
    object fileobj,
    object length,
    object precision,
    object scale,
    object tzinfo,
    object enumcase,
):
    """Read Time from Native Format."""

    cdef bytes seconds_bytes = fileobj.read(4)
    cdef long total_seconds = unpack("<i", seconds_bytes)[0]

    if total_seconds > 3599999:
        total_seconds = 3599999
    elif total_seconds < -3599999:
        total_seconds = -3599999

    return timedelta(seconds=total_seconds)


cpdef bytes write_time(
    object dtype_value,
    object length,
    object precision,
    object scale,
    object tzinfo,
    object enumcase,
):
    """Write Time into Native Format."""

    if dtype_value is None:
        return bytes(4)

    cdef long total_seconds

    if dtype_value.__class__ is timedelta:
        total_seconds = int(dtype_value.total_seconds())
    elif dtype_value.__class__ is time:
        total_seconds = (
            dtype_value.hour * 3600 +
            dtype_value.minute * 60 +
            dtype_value.second
        )
    else:
        raise ValueError(
            "dtype_value must be datetime.time or datetime.timedelta"
        )

    if total_seconds > 3599999:
        total_seconds = 3599999
    elif total_seconds < -3599999:
        total_seconds = -3599999
    
    return pack("<i", total_seconds)


cpdef object read_time64(
    object fileobj,
    object length,
    object precision,
    object scale,
    object tzinfo,
    object enumcase,
):
    """Read Time64 from Native Format."""

    cdef object decimal_value = read_decimal(
        fileobj,
        length,
        18,
        precision,
        tzinfo,
        enumcase,
    )
    cdef double total_seconds_fractional

    if decimal_value is None:
        return None

    total_seconds_fractional = float(decimal_value)

    if total_seconds_fractional > 3599999.999999999:
        total_seconds_fractional = 3599999.999999999
    elif total_seconds_fractional < -3599999.999999999:
        total_seconds_fractional = -3599999.999999999

    return timedelta(seconds=total_seconds_fractional)


cpdef bytes write_time64(
    object dtype_value,
    object length,
    object precision,
    object scale,
    object tzinfo,
    object enumcase,
):
    """Write Time64 into Native Format."""

    if dtype_value is None:
        return write_decimal(
            Decimal('0'),
            length,
            18,
            precision,
            tzinfo,
            enumcase,
        )

    cdef double total_seconds_fractional
    cdef object decimal_value

    if dtype_value.__class__ is timedelta:
        total_seconds_fractional = dtype_value.total_seconds()
    elif dtype_value.__class__ is time:
        total_seconds_fractional = (
            dtype_value.hour * 3600 +
            dtype_value.minute * 60 +
            dtype_value.second +
            dtype_value.microsecond / 1_000_000
        )
    else:
        raise ValueError(
            "dtype_value must be datetime.time or datetime.timedelta"
        )

    if total_seconds_fractional > 3599999.999999999:
        total_seconds_fractional = 3599999.999999999
    elif total_seconds_fractional < -3599999.999999999:
        total_seconds_fractional = -3599999.999999999

    decimal_value = Decimal(str(total_seconds_fractional)).quantize(
        Decimal('1.' + '0' * precision)
    )

    return write_decimal(
        decimal_value,
        length,
        18,
        precision,
        tzinfo,
        enumcase,
    )
