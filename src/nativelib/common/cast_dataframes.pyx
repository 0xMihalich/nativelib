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
    NoneType: "nan",
    bool: "?",
    date: "datetime64[ns]",
    datetime: "datetime64[ns, UTC]",
    float: "float64",
    int: "int64",
    str: "string",
}


cpdef dict pandas_astype(list column_list):
    """Make pandas dtypes from columns."""

    cdef object column_obj
    cdef str name
    cdef object pytype
    cdef int _i
    cdef dict astype = {}

    for column_obj in column_list:
        name = column_obj.column
        pytype = column_obj.info.dtype.pytype

        if column_obj.info.is_array:
            for _i in range(column_obj.info.nested):
                pytype = list[pytype]

        astype[name] = PANDAS_TYPE.get(pytype)

    return astype
