"""Functional command-line tests using a real Python subprocess."""

import hashlib
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class CliTests(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.path = Path(folder.name) / "file.txt"
        self.path.write_bytes(b"hello world")
        self.digest = hashlib.sha256(b"hello world").hexdigest()

    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, "-m", "file_integrity", *map(str, args)],
            check=False, capture_output=True, text=True,
        )

    def test_hash_command(self):
        result = self.run_cli("hash", self.path)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), self.digest)

    def test_verify_success(self):
        result = self.run_cli("verify", self.path, self.digest)
        self.assertEqual(result.returncode, 0)
        self.assertIn("OK", result.stdout)

    def test_verify_mismatch_is_exit_1(self):
        result = self.run_cli("verify", self.path, "f" * 64)
        self.assertEqual(result.returncode, 1)
        self.assertIn("MISMATCH", result.stderr)

    def test_invalid_digest_is_exit_2(self):
        result = self.run_cli("verify", self.path, "bad")
        self.assertEqual(result.returncode, 2)
        self.assertIn("ERROR", result.stderr)

    def test_missing_file_is_exit_2(self):
        result = self.run_cli("hash", self.path.parent / "missing")
        self.assertEqual(result.returncode, 2)
        self.assertIn("ERROR", result.stderr)

    def test_missing_arguments_is_exit_2(self):
        result = self.run_cli()
        self.assertEqual(result.returncode, 2)
        self.assertIn("usage", result.stderr.lower())


if __name__ == "__main__":
    unittest.main()
