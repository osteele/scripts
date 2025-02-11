# Contributing

This directory has a collection of scripts in bash and Python.

The README has a directory of the scripts and their usage, and should be kept up to date with changes to the scripts.

## Getting Started

Clone the repository:

```bash
git clone https://github.com/osteele/scripts.git
cd scripts
```

## Development Guidelines

### General Guidelines

Whenever it makes sense, scripts should support a dry run option.

### Shell Scripts

All shell scripts in this repository should:

1. Start with a proper shebang:
   ```bash
   #!/bin/bash
   ```

2. Set safe shell options:
   ```bash
   set -euo pipefail
   ```

3. Pass shellcheck validation with no warnings. Install shellcheck:
   ```bash
   # macOS
   brew install shellcheck

   # Ubuntu/Debian
   apt-get install shellcheck
   ```
and installed the git hooks:
   ```bash
   bash ./.githooks/install-git-hooks
   ```

4. Use modern shell constructs:
   - Use `$(command)` instead of backticks
   - Quote variables unless they need word splitting
   - Use `[[` for pattern matching
   - Use `printf` instead of `echo` for formatting

### Python Scripts

The Python scripts use the `uv` package and specifies their dependencies inline. They don't use a `Justfile` or `pyproject.toml` file.

Python scripts should start with `#!/usr/bin/env -S uv --quiet run --script`.
They should follow this with the following syntax to specify their dependencies:

```python
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "click",
#     "rich",
# ]
# ///
```

### Directory Structure

- Shell scripts go in topic-specific directories (e.g., `git/`, `dev/`, `media/`)
- Each script should:
  - Have a descriptive name
  - Include a comment header describing its purpose
  - Document its usage in the script and in README.md
- Git scripts should start with `git-*` so that they be invoked as subcommnands
  of the `git` command.

### Testing

Before submitting changes:
1. Run shellcheck on modified scripts
2. Test the scripts with sample data
3. Update documentation if behavior changes
4. Verify git hooks still work

## Pull Request Process

1. Create a feature branch
2. Make your changes
3. Ensure all scripts pass shellcheck
4. Update documentation
5. Submit a pull request

## Code Style

- Use 4 spaces for indentation
- Keep lines under 100 characters
- Add comments for complex logic
- Use meaningful variable names
- Document dependencies
