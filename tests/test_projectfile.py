"""
Unit tests for ProjectFile class. ProjectFile tests use files in examples
directory.

Run with: python -m unittest tests.test_projectfile
"""

import unittest

from sitegen.components.projectfile import ProjectFile
from sitegen.config import EX_PROJECT_PATH, TEST_PATH
from sitegen.exceptions import TagSyntaxError


class TestProjectFile(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Load index file from examples/source."""
        cls.pf = ProjectFile('index.html', path=EX_PROJECT_PATH)
        cls.block = cls.pf.blocks[0]

    def test_init(self):
        """Check base was loaded correctly."""
        self.assertIsNotNone(self.pf)
        self.assertEqual(self.pf.file_name, 'index.html')
        self.assertIsNotNone(self.pf.lines)
        self.assertIsNotNone(self.pf.layout_name)
        self.assertGreater(len(self.pf.blocks), 0)

    def test_extends_layout(self):
        """Test extends_layout() method."""
        self.assertTrue(self.pf.extends_layout())

    # TODO - how to test update_relative_paths() for completeness?

    def test_path_syntax_check(self):
        """Test path tag syntax checking logic."""
        syntax_error_file = ProjectFile('path_tag_error.html', path=TEST_PATH)
        with self.assertRaises(TagSyntaxError):
            syntax_error_file.update_relative_paths()

    def test_load_project_files(self):
        """Test load_project_files() method."""
        files = ProjectFile.load_project_files(base_path=EX_PROJECT_PATH)
        self.assertGreater(len(files), 0)

    def test_block_tag_name(self):
        """Test ProjectFile.Block tag_name() method."""
        self.assertEqual(self.block.tag_name(), '{% block title %}')
