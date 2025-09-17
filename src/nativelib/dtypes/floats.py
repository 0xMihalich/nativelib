from io import (
    BufferedReader,
    BufferedWriter,
)
from struct import (
    pack,
    unpack,
)


FloatStructValue: dict[int, str] = {
    4: "<f",
    8: "<d",
}


def unpack_bfloat16(bfloat16: bytes) -> float:
    """Unpack float from BFloat16 value."""

    bits = bin(
        int.from_bytes(bfloat16, byteorder="little")
    )[2:].zfill(16)
    sign = 1 if bits[0] == "0" else -1
    mantissa = int(bits[9:], 2)
    mant_mult = 1
    exponent: int = pow(2, int(bits[1:9], 2) - 127)

    for b in range(6, -1, -1):
        if mantissa & pow(2, b):
            mant_mult += 1 / pow(2, 7 - b)

    return sign * exponent * mant_mult


def pack_bfloat16(num_float: float) -> bytes:
    """Pack float into BFloat16 value."""

    float32: int = unpack("I", pack("f", num_float))[0]
    return float32.to_bytes(4, "little")[-2:]


def read_bfloat16(
    file: BufferedReader,
    length: int | None = None,
    precission: int | None = None,
    scale: int | None = None,
    tzinfo: str | None = None,
    enum: dict[int, str] | None = None,
) -> float:
    """Read BFloat16 from Native Format."""

    return unpack_bfloat16(file.read(2))


def write_bfloat16(
    dtype_value: float,
    file: BufferedWriter,
    length: int | None = None,
    precission: int | None = None,
    scale: int | None = None,
    tzinfo: str | None = None,
    enum: dict[int, str] | None = None,
) -> None:
    """Write BFloat16 into Native Format."""

    file.write(pack_bfloat16(dtype_value))


def read_float(
    file: BufferedReader,
    length: int,
    precission: int | None = None,
    scale: int | None = None,
    tzinfo: str | None = None,
    enum: dict[int, str] | None = None,
) -> float:
    """Read Float32/Float64 from Native Format."""

    return unpack(FloatStructValue[length], file.read(length))[0]


def write_float(
    dtype_value: float,
    file: BufferedWriter,
    length: int,
    precission: int | None = None,
    scale: int | None = None,
    tzinfo: str | None = None,
    enum: dict[int, str] | None = None,
) -> None:
    """Write Float32/Float64 into Native Format."""

    file.write(pack(FloatStructValue[length], dtype_value))
