# carina

[![License](https://img.shields.io/pypi/l/carina.svg?color=green)](https://github.com/tlambert03/carina/raw/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/carina.svg?color=green)](https://pypi.org/project/carina)
[![Python Version](https://img.shields.io/pypi/pyversions/carina.svg?color=green)](https://python.org)
[![CI](https://github.com/tlambert03/carina/actions/workflows/ci.yml/badge.svg)](https://github.com/tlambert03/carina/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/tlambert03/carina/branch/main/graph/badge.svg)](https://codecov.io/gh/tlambert03/carina)

Stylesheet free theming for Qt applications

## Development

The easiest way to get started is to use the [github cli](https://cli.github.com)
and [uv](https://docs.astral.sh/uv/getting-started/installation/):

```sh
gh repo fork tlambert03/carina --clone
# or just
# gh repo clone tlambert03/carina
cd carina
uv sync
```

Run tests:

```sh
uv run pytest
```

Lint files:

```sh
uv run pre-commit run --all-files
```
