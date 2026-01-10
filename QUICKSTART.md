# Quick Start Guide

This guide will help you get started with the ROS2 Pixi workspace.

## Prerequisites

- Docker and VS Code with Remote-Containers extension (for devcontainer)
- OR pixi installed locally: `curl -fsSL https://pixi.sh/install.sh | bash`

## Setup

### Option 1: Using Devcontainer (Recommended)

1. Open this folder in VS Code
2. Click "Reopen in Container" when prompted
3. Wait for container setup to complete
4. The environment will automatically:
   - Install all dependencies via pixi
   - Import third-party repositories from `repos.repos`
   - Source the ROS2 environment

### Option 2: Using Pixi Locally

```bash
# Install the environment
pixi install

# Import third-party repositories
pixi run import-repos

# Enter the pixi shell (ROS2 environment auto-sourced)
pixi shell
```

## Verify Installation

Run the workspace tests to verify everything is set up correctly:

```bash
pixi run test-workspace
```

This will verify:
- All dev tools are available (fzf, fd, ripgrep, vim)
- Third-party repositories were imported correctly
- The example_interfaces package is present

## Available Dev Tools

The following development tools are pre-installed:

- **fzf**: Fuzzy finder for files and text
- **fd**: Fast alternative to `find`
- **ripgrep (rg)**: Fast text search
- **vim**: Text editor
- **git**: Version control
- **curl/wget**: Download tools

## Build and Test

```bash
# Build the workspace
pixi run build

# Run all tests (workspace + package tests)
pixi run test

# Run linting
pixi run lint

# Run complete CI pipeline
pixi run ci
```

## Using colcon-runner

Short commands via `cr`:

```bash
pixi shell

# Build all packages
cr b

# Build and test
cr bt

# Test only
cr t
```

## Third-Party Repositories

The workspace includes `example_interfaces` as a demonstration. To add your own:

1. Edit `repos.repos`:
   ```yaml
   repositories:
     my_package:
       type: git
       url: https://github.com/user/repo.git
       version: humble
   ```

2. Import the repository:
   ```bash
   pixi run import-repos
   ```

3. Install dependencies:
   ```bash
   pixi run install-deps
   ```

4. Build:
   ```bash
   pixi run build
   ```

## ROS2 Environment

The ROS2 environment is automatically sourced when you enter the pixi shell or devcontainer. You can verify with:

```bash
echo $ROS_DISTRO  # Should output: humble
```

## Example Nodes

Run the example Python nodes:
```bash
# Terminal 1
ros2 run example_py_node publisher

# Terminal 2
ros2 run example_py_node subscriber
```

Run the example C++ nodes:
```bash
# Terminal 1
ros2 run example_cpp_node publisher

# Terminal 2
ros2 run example_cpp_node subscriber
```

## Next Steps

- Explore the example packages in `src/`
- Add your own packages
- Import additional repositories via `repos.repos`
- Customize the environment in `pyproject.toml`

For more details, see `ROS2_WORKSPACE_README.md`.
