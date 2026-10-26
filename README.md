# scratch_env
A template repo for python projects that is set up using [pixi](https://pixi.sh). 

This has basic setup for

* ruff (formatting and linting)
* pytest
* codecov
* git-lfs
* basic github actions ci
* pulling updates from this template


## One ruff version

Ruff is pinned once, as `ruff==X.Y.Z` in `pyproject.toml`. Everything else runs that ruff from the pixi environment:

* `pixi run lint` and `pixi run ci` run `ruff check .` and `ruff format --check .`
* the prek hooks in `.pre-commit-config.yaml` are `repo: local` hooks that run `pixi run --locked ruff ...`, so they carry no version of their own
* CI (`ci.yml` and `prek.yaml`) installs the pixi environment with `setup-pixi` and `locked: true`, so CI fails when `pixi.lock` does not match `pyproject.toml`. It does not run a stale ruff.

To change the ruff version, edit the pin in `pyproject.toml` and run `pixi lock`. Dependabot changes only `pyproject.toml`, so run `pixi lock` on its PR before you merge it. Do not add a `rev:` for ruff to `.pre-commit-config.yaml` or a `version:` to a ruff GitHub action.

## Continuous Integration Status

[![Ci](https://github.com/blooop/python_template/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/blooop/python_template/actions/workflows/ci.yml?query=branch%3Amain)
[![Codecov](https://codecov.io/gh/blooop/python_template/branch/main/graph/badge.svg?token=Y212GW1PG6)](https://codecov.io/gh/blooop/python_template)
[![GitHub issues](https://img.shields.io/github/issues/blooop/python_template.svg)](https://GitHub.com/blooop/python_template/issues/)
[![GitHub pull-requests merged](https://badgen.net/github/merged-prs/blooop/python_template)](https://github.com/blooop/python_template/pulls?q=is%3Amerged)
[![GitHub release](https://img.shields.io/github/release/blooop/python_template.svg)](https://GitHub.com/blooop/python_template/releases/)
[![License](https://img.shields.io/pypi/l/bencher)](https://opensource.org/license/mit/)
[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue)](https://www.python.org/downloads/)
[![Pixi Badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/prefix-dev/pixi/main/assets/badge/v0.json)](https://pixi.sh)


# Install

There are three methods of using this project.  

1. Use github to use this project as a template
2. Clone the project and run, scripts/update_from_template.sh and then scripts/rename_project.sh to rename the project.
3. In your existing git project run this command:

```

```
