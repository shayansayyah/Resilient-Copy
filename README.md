# Resilient Copy

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.x-3776AB)](https://www.python.org/)
[![Windows](https://img.shields.io/badge/Platform-Windows-0078D6)](#)

Resilient Copy is a lightweight Python utility that copies files and folders from a source path to a destination path while supporting wildcard patterns in the source path. It is built for Windows environments and uses `robocopy` under the hood for reliable directory replication.

## What the project does

This project helps when you want to back up or duplicate a set of folders without manually repeating copy commands. Instead of copying a single folder at a time, you can provide a source path containing wildcard segments such as `*`, `?`, or character classes, and the script will identify matching folders or files and replicate them into the destination.

Examples of supported pattern-based source paths:

- `C:/Users/*/Documents`
- `C:/Data/202[4-6]/*`
- `C:/Projects/[!Backup]*/`

If the source path does not contain wildcard characters, the script performs a standard recursive copy using `robocopy`.

## Why the project is useful

- Copy groups of matching folders without writing a long shell loop
- Preserve folder structure while syncing content to a target location
- Use native Windows file-copy behavior through `robocopy`
- Reduce manual errors when copying many similar directories
- Works well for backups, project transfers, and repeated sync scenarios

## Getting started

### Requirements

- Python 3.x
- Windows operating system
- `robocopy` installed and available in `PATH` (it is included with Windows)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/shayansayyah/Resilient-Copy.git
   cd Resilient-Copy
   ```

2. Run the script:

   ```bash
   python main.py
   ```

3. When prompted, enter:
   - the source path
   - the destination path

### Usage examples

#### Copy a single directory

```text
Source path: C:/Users/Alice/Documents
Destination path: D:/Backup/Documents
```

This performs a recursive copy of the source folder into the destination.

#### Copy all matching folders under a shared parent

```text
Source path: C:/Data/*/Reports
Destination path: D:/Archive
```

The script looks for folders matching the wildcard pattern and copies each matching `Reports` directory into the target destination.

#### Copy with literal bracket characters in the path

```text
Source path: C:/Users/[[]bob[]]/Projects
Destination path: D:/Backup
```

Use `[[]` and `[]]` to represent literal `[` and `]` characters in the path.

### Supported wildcard syntax

The script supports the same wildcard patterns commonly used by Windows file globbing:

- `*` — any number of characters
- `?` — exactly one character
- `[abc]` — any single character in the set
- `[a-z]` — any single character in a range
- `[!abc]` or `[^abc]` — any single character not in the set

> Wildcards are intended for the source path only. The destination path should be a concrete target directory.

## How it works

The script performs the following steps:

1. Reads the source and destination paths from the command line prompt.
2. Detects whether the source contains wildcard expressions.
3. Splits the source into fixed and floating path segments.
4. Resolves matching candidate paths.
5. Builds the destination structure based on the matched wildcard segments.
6. Executes `robocopy` to replicate the files and directories.

This keeps the project small and focused on reliable directory copying rather than building a larger file-management framework.

## Where to get help

- Review the code in [main.py](main.py)
- Read the licensing terms in [LICENSE](LICENSE)
- Open an issue in the repository for bug reports or feature requests
- If you are contributing code, share a clear description of the issue and the expected behavior

## Maintainers and contributions

This project is maintained by the repository owner and contributors working on the codebase in this workspace. Contributions are welcome through pull requests and issue discussions.

If you want to contribute:

1. Fork the repository or create a branch for your change.
2. Keep your change focused and well-scoped.
3. Test the updated behavior locally with Python and the platform-specific copy flow.
4. Submit a pull request with a concise summary of the problem and fix.

## License

This project is released under the [MIT License](LICENSE).
