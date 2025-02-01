This directory has a collection of scripts in bash and Python.

The README has a directory of the scripts and their usage, and should be kept up to date with changes to the scripts.

The Python scripts use the `uv` package and specifies their dependencies inline. They don't use a Justfile or pyproject.toml file.

Python scripts should start with `#!/usr/bin/env -S uv --quiet run --script`.
They should follow this with the following syntax to specify their dependencies:

```
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "click",
#     "rich",
# ]
# ///
```

Whenever it makes sense, scripts should support a dry run option.

Bash scripts should have a description of the script before the usage information.

Git scripts should have the name git-* so that they be invoked as subcommnands of the `git` command.