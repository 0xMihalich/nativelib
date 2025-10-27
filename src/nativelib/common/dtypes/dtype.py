"""Enum with read and write functions
for simple types in native binary format."""

from datetime import (
    date,
    datetime as dt,
    timedelta,
)
from enum import Enum
from ipaddress import (
    IPv4Address,
    IPv6Address,
)
from types import (
    FunctionType,
    NoneType,
)
from typing import NamedTuple

from .functions import (
    read_bfloat16,
    read_bool,
    read_date,
    read_date32,
    read_datetime,
    read_datetime64,
    read_decimal,
    read_enum,
    read_float,
    read_int,
    read_ipv4,
    read_ipv6,
    read_nothing,
    read_string,
    read_time,
    read_time64,
    read_uint,
    read_uuid,
    write_bfloat16,
    write_bool,
    write_date,
    write_date32,
    write_datetime,
    write_datetime64,
    write_decimal,
    write_enum,
    write_float,
    write_int,
    write_ipv4,
    write_ipv6,
    write_nothing,
    write_string,
    write_time,
    write_time64,
    write_uint,
    write_uuid,
)


class DTypeFunc(NamedTuple):
    """Class for associate read and write functions."""

    name: str
    pytype: type
    read: FunctionType
    write: FunctionType


class ClickhouseDtype(DTypeFunc, Enum):
    """Associate read and write functions with clickhouse data type."""

    BFloat16 = DTypeFunc("BFloat16", float, read_bfloat16, write_bfloat16)
    Bool = DTypeFunc("Bool", bool, read_bool, write_bool)
    Date = DTypeFunc("Date", date, read_date, write_date)
    Date32 = DTypeFunc("Date32", date, read_date32, write_date32)
    DateTime = DTypeFunc("DateTime", dt, read_datetime, write_datetime)
    DateTime64 = DTypeFunc("DateTime64", dt, read_datetime64, write_datetime64)
    Decimal = DTypeFunc("Decimal", object, read_decimal, write_decimal)
    Enum8 = DTypeFunc("Enum8", str, read_enum, write_enum)
    Enum16 = DTypeFunc("Enum16", str, read_enum, write_enum)
    FixedString = DTypeFunc("FixedString", str, read_string, write_string)
    Float32 = DTypeFunc("Float32", float, read_float, write_float)
    Float64 = DTypeFunc("Float64", float, read_float, write_float)
    IPv4 = DTypeFunc("IPv4", IPv4Address, read_ipv4, write_ipv4)
    IPv6 = DTypeFunc("IPv6", IPv6Address, read_ipv6, write_ipv6)
    Int128 = DTypeFunc("Int128", int, read_int, write_int)
    Int16 = DTypeFunc("Int16", int, read_int, write_int)
    Int256 = DTypeFunc("Int256", int, read_int, write_int)
    Int32 = DTypeFunc("Int32", int, read_int, write_int)
    Int64 = DTypeFunc("Int64", int, read_int, write_int)
    Int8 = DTypeFunc("Int8", int, read_int, write_int)
    Nothing = DTypeFunc("Nothing", NoneType, read_nothing, write_nothing)
    Nullable = DTypeFunc("Nullable", bool, read_bool, write_bool)
    String = DTypeFunc("String", str, read_string, write_string)
    Time = DTypeFunc("Time", timedelta, read_time, write_time)
    Time64 = DTypeFunc("Time64", timedelta, read_time64, write_time64)
    UInt128 = DTypeFunc("UInt128", int, read_uint, write_uint)
    UInt16 = DTypeFunc("UInt16", int, read_uint, write_uint)
    UInt256 = DTypeFunc("UInt256", int, read_uint, write_uint)
    UInt32 = DTypeFunc("UInt32", int, read_uint, write_uint)
    UInt64 = DTypeFunc("UInt64", int, read_uint, write_uint)
    UInt8 = DTypeFunc("UInt8", int, read_uint, write_uint)
    UUID = DTypeFunc("UUID", object, read_uuid, write_uuid)
