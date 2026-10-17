"""Streaming SHA-256 computation with bounded memory usage."""

import hashlib
from pathlib import Path


def sha256_file(path: str | Path, *, chunk_size: int = 1024 * 1024) -> str:
    """Return the lower-case SHA-256 hex digest of a file.

    Reads in blocks rather than loading the entire file into memory.

    Raises:
        ValueError: if chunk_size is not positive.
        OSError: if the path cannot be read as a file.
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be a positive integer")

    digest = hashlib.sha256()
    with Path(path).open("rb") as source:
        while chunk := source.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()
