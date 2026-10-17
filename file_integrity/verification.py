"""SHA-256 digest validation and constant-time comparison."""

import hmac
import re
from pathlib import Path

from .hashing import sha256_file

_DIGEST_PATTERN = re.compile(r"[0-9a-fA-F]{64}\Z", flags=re.ASCII)


def verify_file(path: str | Path, expected_hash: str) -> bool:
    """Verify a file against a trusted 64-digit SHA-256 hex digest.

    Raises ValueError on malformed digests and OSError on unreadable files.
    """
    if not _DIGEST_PATTERN.fullmatch(expected_hash):
        raise ValueError("expected SHA-256 must contain exactly 64 hexadecimal characters")
    actual = sha256_file(path)
    return hmac.compare_digest(actual, expected_hash.lower())
