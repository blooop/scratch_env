# scratch_env
A template repo for python projects that is set up using [pixi](https://pixi.sh). 

## Image → 3D-printable stamp

`python_template/stamp.py` turns a black-and-white image into an STL of a
physical stamp for applying paint. Dark regions of the image become the raised
relief that picks up paint; the design is mirrored left-to-right so the printed
impression reads the same as the source image. The output is a watertight,
support-free mesh (a flat base plate with vertical-walled relief).

```bash
image-to-stamp logo.png -o logo.stl --width 60 --relief 2.5 --base 3
```

Key options: `--width` (footprint mm), `--base` (backing plate mm),
`--relief` (how far the design rises), `--threshold` (0-255 dark/light cutoff),
`--invert` (use light pixels as the design), `--no-mirror`, `--max-pixels`
(downsample cap). From Python:

```python
from python_template.stamp import image_to_stamp_stl, StampConfig

image_to_stamp_stl("logo.png", "logo.stl", StampConfig(width_mm=60, relief_height=2.5))
```


This has basic setup for

* pylint
* ruff
* black
* pytest
* codecov
* git-lfs
* basic github actions ci
* pulling updates from this template


## Continuous Integration Status

[![Ci](https://github.com/blooop/python_template/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/blooop/python_template/actions/workflows/ci.yml?query=branch%3Amain)
[![Codecov](https://codecov.io/gh/blooop/python_template/branch/main/graph/badge.svg?token=Y212GW1PG6)](https://codecov.io/gh/blooop/python_template)
[![GitHub issues](https://img.shields.io/github/issues/blooop/python_template.svg)](https://GitHub.com/blooop/python_template/issues/)
[![GitHub pull-requests merged](https://badgen.net/github/merged-prs/blooop/python_template)](https://github.com/blooop/python_template/pulls?q=is%3Amerged)
[![GitHub release](https://img.shields.io/github/release/blooop/python_template.svg)](https://GitHub.com/blooop/python_template/releases/)
[![License](https://img.shields.io/pypi/l/bencher)](https://opensource.org/license/mit/)
[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11-blue)](https://www.python.org/downloads/)
[![Pixi Badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/prefix-dev/pixi/main/assets/badge/v0.json)](https://pixi.sh)


# Install

There are three methods of using this project.  

1. Use github to use this project as a template
2. Clone the project and run, scripts/update_from_template.sh and then scripts/rename_project.sh to rename the project.
3. In your existing git project run this command:

```

```
