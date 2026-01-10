# ROS2 Pixi Workspace

A complete ROS2 workspace setup using pixi for package management, with devcontainer support, vcstool integration, and colcon-runner for efficient development workflows.

## Features

- **Pixi-based package management**: Cross-platform, reproducible ROS2 environment
- **Auto-sourced ROS2 environment**: ROS2 setup automatically sourced on shell activation
- **Devcontainer support**: VS Code development container configuration
- **vcstool integration**: Manage third-party repositories easily (includes example_interfaces)
- **colcon-runner**: Streamlined build, test, and clean commands
- **Dev tools included**: fzf, fd-find, ripgrep, vim, git, curl, wget
- **Example packages**:
  - Custom message definitions
  - Python publisher/subscriber nodes
  - C++ publisher/subscriber nodes
  - Comprehensive tests
- **Workspace validation tests**: Verify repository imports and tool availability

## Prerequisites

- Docker (for devcontainer support)
- VS Code with Remote-Containers extension (optional)
- Or pixi installed locally: `curl -fsSL https://pixi.sh/install.sh | bash`

## Quick Start

### Using Devcontainer (Recommended)

1. Open this folder in VS Code
2. When prompted, click "Reopen in Container"
3. Wait for the container to build and initialize
4. The pixi environment will be automatically set up

### Using Pixi Locally

1. Install pixi if you haven't already
2. Install the environment:
   ```bash
   pixi install
   ```
3. Enter the pixi shell:
   ```bash
   pixi shell
   ```

## Workspace Structure

```
.
├── src/
│   ├── example_msgs/          # Custom message definitions
│   ├── example_py_node/       # Python publisher/subscriber
│   └── example_cpp_node/      # C++ publisher/subscriber
├── pyproject.toml             # Pixi configuration
├── defaults.yaml              # Colcon defaults for colcon-runner
├── repos.repos                # vcstool repository list
└── .devcontainer/             # VS Code devcontainer config
```

## Available Pixi Tasks

### Build Tasks
- `pixi run clean` - Remove build, install, and log directories
- `pixi run build` - Build all packages with colcon
- `pixi run build-cr` - Build using colcon-runner (cr b)

### Test Tasks
- `pixi run test` - Run all tests with colcon
- `pixi run test-cr` - Run tests using colcon-runner (cr t)
- `pixi run test-results` - Display test results verbosely

### Lint Tasks
- `pixi run lint` - Run all linters (Python and C++)
- `pixi run lint-python` - Run ruff linter on Python code
- `pixi run lint-python-format` - Format Python code with ruff
- `pixi run lint-cpp` - Format C++ code with clang-format

### CI Task
- `pixi run ci` - Run complete CI pipeline (clean, build, lint, test)

### Utility Tasks
- `pixi run import-repos` - Import repositories from repos.repos using vcstool
- `pixi run install-deps` - Install dependencies using rosdep

## Using colcon-runner

Colcon-runner provides short, mnemonic commands:

```bash
# Build all packages
cr b

# Build and test
cr bt

# Build only a specific package
cr boto package_name

# Test all packages
cr t

# Clean workspace
cr c
```

## Example Packages

### example_msgs
Custom ROS2 message package with an `ExampleMessage` type containing:
- `string name`
- `int32 value`
- `float64 timestamp`
- `bool is_active`

### example_py_node
Python package with:
- **publisher_node.py**: Publishes ExampleMessage at 1 Hz
- **subscriber_node.py**: Subscribes to ExampleMessage
- **Tests**: Unit tests for both nodes

Run the Python nodes:
```bash
pixi run build
source install/setup.bash
ros2 run example_py_node publisher
# In another terminal:
ros2 run example_py_node subscriber
```

### example_cpp_node
C++ package with:
- **publisher_node.cpp**: Publishes ExampleMessage at 1 Hz
- **subscriber_node.cpp**: Subscribes to ExampleMessage
- **Tests**: GTest-based unit tests

Run the C++ nodes:
```bash
pixi run build
source install/setup.bash
ros2 run example_cpp_node publisher
# In another terminal:
ros2 run example_cpp_node subscriber
```

## Adding Third-Party Repositories

1. Edit `repos.repos` to add your repository:
   ```yaml
   repositories:
     my_package:
       type: git
       url: https://github.com/user/repo.git
       version: humble
   ```

2. Import the repositories:
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

## Development Workflow

1. **Start development**:
   ```bash
   pixi shell
   ```

2. **Make changes** to your code

3. **Build and test**:
   ```bash
   pixi run ci
   ```

4. **Run your nodes**:
   ```bash
   source install/setup.bash
   ros2 run <package_name> <executable>
   ```

## CI/CD Integration

The `pixi run ci` task runs the complete CI pipeline:
1. Clean previous builds
2. Build all packages
3. Lint Python and C++ code
4. Run all tests

This can be integrated into your CI/CD pipeline (GitHub Actions, GitLab CI, etc.):

```yaml
# Example GitHub Actions step
- name: Run CI
  run: |
    pixi install
    pixi run ci
```

## Troubleshooting

### Build failures
- Ensure all dependencies are installed: `pixi install`
- Clean and rebuild: `pixi run clean && pixi run build`

### Import errors
- Make sure you source the setup file: `source install/setup.bash`
- Verify the package was built: `ls install/`

### vcstool issues
- Check your repos.repos syntax
- Ensure git is accessible and you have network connectivity

## Additional Resources

- [Pixi Documentation](https://prefix.dev/docs/pixi)
- [ROS2 Documentation](https://docs.ros.org)
- [colcon-runner](https://github.com/blooop/colcon-runner)
- [vcstool](https://github.com/dirk-thomas/vcstool)

## License

MIT
