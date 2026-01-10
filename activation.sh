#!/bin/bash
# Pixi activation script for ROS2 workspace
# This script is automatically sourced when entering the pixi environment

# Source ROS2 setup if it exists
if [ -f "$CONDA_PREFIX/setup.bash" ]; then
    source "$CONDA_PREFIX/setup.bash"
fi

# Source local workspace setup if it exists
if [ -f "install/setup.bash" ]; then
    source install/setup.bash
    echo "✓ ROS2 workspace environment sourced"
fi

# Set up useful aliases for development
alias ll='ls -lah'
alias gs='git status'
alias gd='git diff'
alias gc='git commit'
alias gp='git push'

# Inform user that dev tools are available
echo "✓ Dev tools available: fzf, fd, rg (ripgrep), vim"
echo "✓ ROS2 environment ready"
