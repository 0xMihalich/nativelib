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


cdef dict PANDAS_TYPE = {
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


cpdef dict polars_schema(list column_list):
    """Make polars schema from columns."""

    cdef object column_obj
    cdef str name
    cdef object pytype
    cdef int _i
    cdef dict schema = {}

    for column_obj in column_list:
        name = column_obj.column
        pytype = column_obj.info.dtype.pytype

        if column_obj.info.is_array:
            for _i in range(column_obj.info.nested):
                pytype = list[pytype]

        schema[name] = pytype

    return schema


cpdef dict pandas_astype(list column_list):
    """Make pandas dtypes from columns."""

    cdef dict astype = polars_schema(column_list)

    for name, pytype in astype.items():
        astype[name] = PANDAS_TYPE.get(pytype, "O")

    return astype
