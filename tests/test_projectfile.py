"""
Unit tests for ProjectFile class. ProjectFile tests use files in examples
directory.

Run with: python -m unittest tests.test_projectfile
"""

import unittest
from typing import Optional

from sitegen.components.projectfile import ProjectFile
from sitegen.config import EX_PROJECT_PATH, TEST_PATH
from sitegen.exceptions import TagSyntaxError


class TestProjectFile(unittest.TestCase):

    pf: ProjectFile = ProjectFile('index.html', path=EX_PROJECT_PATH)
    block: Optional[ProjectFile.Block] = pf.blocks.get('title')

    def test_init(self) -> None:
        """Check base was loaded correctly."""
        self.assertIsNotNone(self.pf)
        self.assertEqual(self.pf.file_name, 'index.html')
        self.assertIsNotNone(self.pf.lines)
        self.assertIsNotNone(self.pf.layout_name)
        self.assertGreater(len(self.pf.blocks), 0)

    def test_extends_layout(self) -> None:
        """Test extends_layout() method."""
        self.assertTrue(self.pf.extends_layout())

    def test_update_relative_paths(self) -> None:
        """Test update_relative_paths() method."""
        sb: ProjectFile = ProjectFile('/subpage/subsubpage/index.html', path=EX_PROJECT_PATH)
        sb.update_relative_paths()
        rel_path_location: int = str(sb).find('../../subpage/index.html')
        # str.find() returns -1 if a match is not located
        self.assertNotEqual(rel_path_location, -1)

    def test_path_syntax_check(self) -> None:
        """Test path tag syntax checking logic."""
        syntax_error_file: ProjectFile = ProjectFile('path_tag_error.html', path=TEST_PATH)
        with self.assertRaises(TagSyntaxError):
            syntax_error_file.update_relative_paths()

    def test_load_project_files(self) -> None:
        """Test load_project_files() method."""
        files: list[ProjectFile] = ProjectFile.load_project_files(base_path=EX_PROJECT_PATH)
        self.assertGreater(len(files), 0)

    def test_block_tag_name(self) -> None:
        """Test ProjectFile.Block tag_name() method."""
        if self.block is not None:
            self.assertEqual(self.block.tag_name(), '{% block title %}')
        else:
            self.fail('self.block is None')
