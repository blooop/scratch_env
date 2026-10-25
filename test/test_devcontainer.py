import json
import os
import re
import subprocess
from pathlib import Path

DEVCONTAINER = Path(__file__).resolve().parent.parent / ".devcontainer"


def load_devcontainer_json():
    text = (DEVCONTAINER / "devcontainer.json").read_text(encoding="utf-8")
    return json.loads(re.sub(r"(?m)^\s*//.*$", "", text))


def test_init_host_creates_every_home_bind_source(tmp_path):
    """docker refuses a bind mount whose source is missing, so container
    creation fails on a host that lacks any of these directories."""
    config = load_devcontainer_json()
    subprocess.run(
        [str(DEVCONTAINER.parent / config["initializeCommand"])],
        env={**os.environ, "HOME": str(tmp_path)},
        check=True,
    )
    sources = [
        dict(kv.split("=", 1) for kv in mount.split(","))["source"]
        for mount in config["mounts"]
        if "type=bind" in mount
    ]
    assert sources
    for source in sources:
        path = Path(source.replace("${localEnv:HOME}", str(tmp_path)))
        assert path.is_dir(), f"{source} missing after initializeCommand"
