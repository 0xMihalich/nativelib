from ast import literal_eval
from re import (
    findall,
    match,
)

from nativelib.common.dtypes.dtype import ClickhouseDtype


cdef str DTYPE_PATTERN = r"^(\w+)(?:\((.*)\))?$"
cdef str ENUM_PATTERN = r"'([^']+)'\s*=\s*(-*?\d+)"
cdef dict DTYPE_LENGTH = {
    "BFloat16": 2,
    "Bool": 1,
    "Date": 2,
    "Date32": 4,
    "DateTime": 4,
    "DateTime64": 8,
    "Enum16": 2,
    "Enum8": 1,
    "Float32": 4,
    "Float64": 8,
    "IPv4": 4,
    "IPv6": 16,
    "Int128": 16,
    "Int16": 2,
    "Int256": 32,
    "Int32": 4,
    "Int64": 8,
    "Int8": 1,
    "Point": 16,
    "Time": 4,
    "Time64": 8,
    "UInt128": 16,
    "UInt16": 2,
    "UInt256": 32,
    "UInt32": 4,
    "UInt64": 8,
    "UInt8": 1,
    "UUID": 16,
}


cdef unsigned char find_decimal_length(char precision):
    """Find Decimal lens."""

    if precision not in range(1, 77):
        raise ValueError("precision must be in [1:76] range!")
    if precision <= 9:
        return 4
    if precision <= 18:
        return 8
    if precision <= 38:
        return 16
    return 32


cdef object parse_args(str args):
    """Find args for Datetime64, Decimal and FixedString."""

    return literal_eval(args)


cdef object parse_dtype(str dtype):
    """Find datype and args from dtype string."""

    return match(DTYPE_PATTERN, dtype)


cdef dict parse_enum(str args):
    """Create Enum8/Enum16 dictionary from string."""

    cdef dict enumcase = {}
    cdef str string, number

    for string, number in findall(ENUM_PATTERN, args):
        enumcase[int(number)] = string

    return enumcase


cdef tuple from_dtype(
    str dtype,
    object is_array = False,
    object is_lowcardinality = False,
    object is_nullable = False,
    object length = None,
    object precision = None,
    object scale = None,
    object tzinfo = None,
    object enumcase = None,
    unsigned long nested = 0,
):
    """Parse info from dtype."""

    cdef object parse = parse_dtype(dtype)
    cdef str parent_dtype
    cdef object args_dtype

    if not parse:
        raise ValueError("Fail to parse dtype values!")

    parent_dtype = parse.group(1)
    args_dtype = parse.group(2)

    if parent_dtype in ("Array", "LowCardinality", "Nullable"):

        if parent_dtype == "Array":
            is_array = True
            nested += 1
        elif parent_dtype == "LowCardinality":
            is_lowcardinality = True
        elif parent_dtype == "Nullable":
            is_nullable = True

        return from_dtype(
            args_dtype,
            is_array,
            is_lowcardinality,
            is_nullable,
            length,
            precision,
            scale,
            tzinfo,
            enumcase,
            nested,
        )

    if parent_dtype == "FixedString":
        length = parse_args(args_dtype)
    elif parent_dtype == "Decimal":
        precision, scale = parse_args(args_dtype)
        length = find_decimal_length(precision)
    else:
        length = DTYPE_LENGTH.get(parent_dtype)

    if parent_dtype == "DateTime64":
        args = parse_args(args_dtype)

        if args.__class__ is tuple:
            precision, tzinfo = args
        else:
            precision = args

    elif parent_dtype == "Time64":
        precision = parse_args(args_dtype)
    elif parent_dtype in ("Enum8", "Enum16"):
        enumcase = parse_enum(args_dtype)

    return (
        ClickhouseDtype[parent_dtype],
        is_array,
        is_lowcardinality,
        is_nullable,
        length,
        precision,
        scale,
        tzinfo,
        enumcase,
        nested,
    )
