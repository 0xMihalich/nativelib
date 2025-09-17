from ast import literal_eval
from re import (
    findall,
    match,
    Match,
)
from typing import Any

from ..associate import DTypeLength
from ..dtypes import ClickhouseDtype


dtype_pattern = r"^(\w+)(?:\((.*)\))?$"
enum_pattern = r"'([^']+)'\s*=\s*(-*?\d+)"


def find_decimal_length(precission: int) -> int:
    """Find Decimal lens."""

    if precission not in range(1, 77):
        raise ValueError("precission must be in [1:76] range!")
    if precission <= 9:
        return 4
    if precission <= 18:
        return 8
    if precission <= 38:
        return 16
    return 32


def parse_args(args: str) -> tuple[int, int | str] | int:
    """Find args for Datetime64, Decimal and FixedString."""

    return literal_eval(args)


def parse_dtype(dtype: str) -> Match | None:
    """Find datype and args from dtype string."""

    return match(dtype_pattern, dtype)


def parse_enum(args: str) -> dict[int, str]:
    """Create Enum8/Enum16 dictionary from string."""

    return {
        int(num): strings
        for strings, num in findall(enum_pattern, args)
    }


def from_dtype(
    dtype: str,
    is_array: bool = False,
    is_lowcardinality: bool = False,
    is_nullable: bool = False,
    length: int | None = None,
    precission: int | None = None,
    scale: int | None = None,
    tzinfo: str | None = None,
    enum: dict[int, str] | None = None,
    nested: int = 0,
) -> tuple[Any, ...]:
    """Parse info from dtype."""

    parse: Match | None = parse_dtype(dtype)

    if not parse:
        raise ValueError("Fail to parse dtype values!")

    parent_dtype: str = parse.group(1)
    args_dtype: str | None = parse.group(2)

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
            precission,
            scale,
            tzinfo,
            enum,
            nested,
        )

    if parent_dtype == "FixedString":
        length = parse_args(args_dtype)
    elif parent_dtype == "Decimal":
        precission, scale = parse_args(args_dtype)
        length = find_decimal_length(precission)
    else:
        length = DTypeLength.get(parent_dtype)

    if parent_dtype == "DateTime64":
        args = parse_args(args_dtype)
        if isinstance(args, tuple):
            precission, tzinfo = args
        else:
            precission = args
            tzinfo = "UTC"
    elif parent_dtype == "Time64":
        precission = parse_args(args_dtype)
    elif parent_dtype in ("Enum8", "Enum16"):
        enum = parse_enum(args_dtype)

    return (
        ClickhouseDtype[parent_dtype],
        is_array,
        is_lowcardinality,
        is_nullable,
        length,
        precission,
        scale,
        tzinfo,
        enum,
        nested,
    )
