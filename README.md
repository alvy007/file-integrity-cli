# File Integrity CLI

A lightweight, dependency-free Python command-line tool for **SHA-256 file integrity checks**. It streams file contents in chunks, so it works with large files without loading them entirely into memory.

## Requirements

- Python 3.10 or later
- No third-party dependencies

## Generate a hash

```bash
python -m file_integrity hash path/to/file.zip
```

Prints the file's 64-character SHA-256 digest. Compare this with a digest from a trusted source.

## Verify a hash

```bash
python -m file_integrity verify path/to/file.zip 0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef
```

Replace the example digest with a **trusted SHA-256 digest**. Verification accepts uppercase or lowercase hex.

Exit codes:

| Code | Meaning |
|---|---|
| 0 | File hashed successfully or digest matches |
| 1 | Digest mismatch |
| 2 | Invalid input or file read error |

## Command-line help

To discover available commands and arguments, run:

```bash
python -m file_integrity --help
python -m file_integrity hash --help
python -m file_integrity verify --help
```

These commands display usage information without computing or checking file hashes.

## Running the tests

```bash
python -m unittest discover -s tests -v
```

CI runs the suite automatically on pushes and pull requests.

## Security considerations

An attacker who controls both a file and its published digest can replace both. **SHA-256 hashing alone is not an authenticity check**. Obtain the reference checksum through a trusted channel or use signed releases when authentication is required.

The utility reads files but does not modify them.

## License

[MIT](LICENSE).
