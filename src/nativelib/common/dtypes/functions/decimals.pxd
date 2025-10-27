cpdef object read_decimal(
    object fileobj,
    object length,
    unsigned char precision,
    unsigned char scale,
    object tzinfo,
    object enumcase,
)
cpdef bytes write_decimal(
    object dtype_value,
    object length,
    unsigned char precision,
    unsigned char scale,
    object tzinfo,
    object enumcase,
)
