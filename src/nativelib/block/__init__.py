"""Read and write block from native format."""

from .defines import DEFAULT_BLOCK_SIZE
from .reader import BlockReader
from .writer import BlockWriter


__all__ = (
    "DEFAULT_BLOCK_SIZE",
    "BlockReader",
    "BlockWriter",
)
