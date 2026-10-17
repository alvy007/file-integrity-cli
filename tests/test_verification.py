"""Unit tests for verifying SHA-256 digests."""

import hashlib
import tempfile
import unittest
from pathlib import Path

from file_integrity.verification import verify_file


class VerificationTests(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.file = Path(folder.name) / "payload.bin"
        self.file.write_bytes(b"a verified payload")
        self.expected = hashlib.sha256(self.file.read_bytes()).hexdigest()

    def test_matching_digest(self):
        self.assertTrue(verify_file(self.file, self.expected))

    def test_uppercase_digest(self):
        self.assertTrue(verify_file(self.file, self.expected.upper()))

    def test_mismatched_digest(self):
        self.assertFalse(verify_file(self.file, "0" * 64))

    def test_modified_contents_do_not_verify(self):
        self.file.write_bytes(b"a changed payload")
        self.assertFalse(verify_file(self.file, self.expected))

    def test_malformed_digest_rejected(self):
        for invalid in ("", "abc", "0" * 63, "g" * 64, "0" * 65, "0" * 64 + "\n"):
            with self.subTest(invalid=repr(invalid)):
                with self.assertRaises(ValueError):
                    verify_file(self.file, invalid)


if __name__ == "__main__":
    unittest.main()
