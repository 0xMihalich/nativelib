from datetime import (
    date,
    datetime,
)
from types import NoneType


cdef dict PANDAS_TYPE = {
    NoneType: "nan",
    bool: "?",
    date: "datetime64[ns]",
    datetime: "datetime64[ns, UTC]",
    float: "float64",
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
