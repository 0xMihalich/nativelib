from ipaddress import ip_address


cpdef object read_ipv4(
    object fileobj,
    object length,
    object precision,
    object scale,
    object tzinfo,
    object enumcase,
):
    """Read IPv4 from Native Format."""

    cdef bytes packed = fileobj.read(4)
    return ip_address(packed[::-1])


cpdef bytes write_ipv4(
    object dtype_value,
    object length,
    object precision,
    object scale,
    object tzinfo,
    object enumcase,
):
    """Write IPv4 into Native Format."""

    if dtype_value is None:
        return bytes(4)

    cdef bytes packed = dtype_value.packed
    return packed[::-1]


cpdef object read_ipv6(
    object fileobj,
    object length,
    object precision,
    object scale,
    object tzinfo,
    object enumcase,
):
    """Read IPv6 from Native Format."""

    cdef bytes packed = fileobj.read(16)
    return ip_address(packed)


cpdef bytes write_ipv6(
    object dtype_value,
    object length,
    object precision,
    object scale,
    object tzinfo,
    object enumcase,
):
    """Write IPv6 into Native Format."""

    if dtype_value is None:
        return bytes(16)

    return dtype_value.packed
