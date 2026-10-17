"""Unit tests for streaming SHA-256 hashing."""

import hashlib
import tempfile
import unittest
from pathlib import Path

from file_integrity.hashing import sha256_file


class HashingTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.file = Path(self.folder.name) / "sample.bin"

    def test_known_sha256_of_abc(self):
        self.file.write_bytes(b"abc")
        self.assertEqual(
            sha256_file(self.file),
            "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",
        )

    def test_empty_file(self):
        self.file.write_bytes(b"")
        self.assertEqual(sha256_file(self.file), hashlib.sha256(b"").hexdigest())

    def test_large_binary_file_is_streamed_in_small_chunks(self):
        data = bytes(range(256)) * 8192
        self.file.write_bytes(data)
        self.assertEqual(sha256_file(self.file, chunk_size=17), hashlib.sha256(data).hexdigest())

    def test_invalid_chunk_size(self):
        self.file.write_bytes(b"x")
        with self.assertRaisesRegex(ValueError, "positive"):
            sha256_file(self.file, chunk_size=0)

    def test_missing_file(self):
        with self.assertRaises(FileNotFoundError):
            sha256_file(self.file)


if __name__ == "__main__":
    unittest.main()
