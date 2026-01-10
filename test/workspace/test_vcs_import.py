#!/usr/bin/env python3
"""Tests to verify vcstool repository import and installation."""

import os
import subprocess
from pathlib import Path

import pytest


class TestVcsImport:
    """Test cases for vcstool repository import."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up test environment."""
        self.workspace_root = Path(__file__).parent.parent.parent
        self.src_dir = self.workspace_root / "src"

    def test_src_directory_exists(self):
        """Test that the src directory exists."""
        assert self.src_dir.exists(), "src directory should exist"
        assert self.src_dir.is_dir(), "src should be a directory"

    def test_example_interfaces_repo_exists(self):
        """Test that example_interfaces repository was imported."""
        example_interfaces_dir = self.src_dir / "example_interfaces"
        assert (
            example_interfaces_dir.exists()
        ), "example_interfaces repository should exist in src/"

    def test_example_interfaces_package_xml_exists(self):
        """Test that example_interfaces has a package.xml."""
        package_xml = self.src_dir / "example_interfaces" / "package.xml"
        assert package_xml.exists(), "example_interfaces should have a package.xml"

    def test_example_interfaces_has_msg_definitions(self):
        """Test that example_interfaces contains message definitions."""
        msg_dir = self.src_dir / "example_interfaces" / "msg"
        if msg_dir.exists():
            msg_files = list(msg_dir.glob("*.msg"))
            assert len(msg_files) > 0, "example_interfaces should have .msg files"

    def test_example_interfaces_cmake_exists(self):
        """Test that example_interfaces has CMakeLists.txt."""
        cmake_file = self.src_dir / "example_interfaces" / "CMakeLists.txt"
        assert cmake_file.exists(), "example_interfaces should have CMakeLists.txt"

    def test_vcs_command_available(self):
        """Test that vcs tool is available."""
        result = subprocess.run(
            ["which", "vcs"], capture_output=True, text=True, check=False
        )
        assert result.returncode == 0, "vcs command should be available"

    def test_repos_file_exists(self):
        """Test that repos.repos file exists."""
        repos_file = self.workspace_root / "repos.repos"
        assert repos_file.exists(), "repos.repos file should exist"

    def test_repos_file_valid_yaml(self):
        """Test that repos.repos is valid YAML."""
        import yaml

        repos_file = self.workspace_root / "repos.repos"
        with open(repos_file) as f:
            data = yaml.safe_load(f)

        assert "repositories" in data, "repos.repos should have 'repositories' key"
        assert (
            "example_interfaces" in data["repositories"]
        ), "repos.repos should list example_interfaces"


class TestDevTools:
    """Test cases for development tools."""

    def test_fzf_available(self):
        """Test that fzf is available."""
        result = subprocess.run(
            ["which", "fzf"], capture_output=True, text=True, check=False
        )
        assert result.returncode == 0, "fzf should be available"

    def test_fd_available(self):
        """Test that fd-find is available."""
        # fd-find might be available as 'fd' or 'fdfind'
        result_fd = subprocess.run(
            ["which", "fd"], capture_output=True, text=True, check=False
        )
        result_fdfind = subprocess.run(
            ["which", "fdfind"], capture_output=True, text=True, check=False
        )
        assert (
            result_fd.returncode == 0 or result_fdfind.returncode == 0
        ), "fd or fdfind should be available"

    def test_ripgrep_available(self):
        """Test that ripgrep is available."""
        result = subprocess.run(
            ["which", "rg"], capture_output=True, text=True, check=False
        )
        assert result.returncode == 0, "rg (ripgrep) should be available"

    def test_vim_available(self):
        """Test that vim is available."""
        result = subprocess.run(
            ["which", "vim"], capture_output=True, text=True, check=False
        )
        assert result.returncode == 0, "vim should be available"

    def test_git_available(self):
        """Test that git is available."""
        result = subprocess.run(
            ["which", "git"], capture_output=True, text=True, check=False
        )
        assert result.returncode == 0, "git should be available"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
