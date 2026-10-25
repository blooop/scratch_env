#!/bin/sh
# Runs on the HOST before the container is created. docker refuses a bind
# mount whose source does not exist, so every bind source in devcontainer.json
# must be created here. mkdir -p never clobbers an existing directory.

mkdir -p "$HOME/.claude" "$HOME/.config/gh"
