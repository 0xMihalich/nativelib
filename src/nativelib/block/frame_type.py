from datetime import (
    date,
    datetime,
)
from decimal import Decimal
from enum import Enum
from ipaddress import (
    IPv4Address,
    IPv6Address,
)
from types import NoneType
from uuid import UUID

from polars import (
    Decimal as PlDecimal,
    Enum as PlEnum,
    Object,
    Null,
    Boolean,
    Date,
    Datetime,
    Float64,
    Int64,
    String,
)


pandas_dtype = {
    Decimal: "O",
    Enum: "O",
    IPv4Address: "O",
    IPv6Address: "O",
    NoneType: "nan",
    UUID: "O",
    bool: "?",
    date: "datetime64[ns]",
    datetime: "datetime64[ns]",
    float: "float64",
    int: "int64",
    str: "str",
}
polars_dtype = {
    Decimal: PlDecimal,
    Enum: PlEnum,
    IPv4Address: Object,
    IPv6Address: Object,
    NoneType: Null,
    UUID: Object,
    bool: Boolean,
    date: Date,
    datetime: Datetime,
    float: Float64,
    int: Int64,
    str: String,
}
