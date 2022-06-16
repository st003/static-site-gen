"""
Unit tests for ProjectFile class. ProjectFile tests use files in example
directory.

Run with: python -m unittest tests.test_projectfile
"""

import unittest

from sitegen.config import PROJECT_PATH
from sitegen.components.projectfile import ProjectFile


class TestProjectFile(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Load root src index file from examples."""
        cls.pf = ProjectFile(f'{PROJECT_PATH}/index.html')
        cls.block = cls.pf.blocks[0]

    def test_init(self):
        """Check base was loaded correctly."""
        self.assertIsNotNone(self.pf)
        self.assertEqual(self.pf.path, f'{PROJECT_PATH}/index.html')
        self.assertIsNotNone(self.pf.lines)
        self.assertIsNotNone(self.pf.layout_name)
        self.assertGreater(len(self.pf.blocks), 0)

    def test_relative_path(self):
        """Test relative_path() method."""
        self.assertEqual(self.pf.relative_path(), 'index.html')

    def test_get_extention(self):
        """Test get_extention() method."""
        self.assertEqual(self.pf.get_extention(), 'html')

    def test_to_string(self):
        """Test to_string() method."""
        self.assertTrue(isinstance(self.pf.to_string(), str))

    def test_extends_layout(self):
        """Test extends_layout() method."""
        self.assertTrue(self.pf.extends_layout())

    def test_dir_level(self):
        """Test dir_level() method."""
        self.assertEqual(self.pf.dir_level(), 0)

    def test_in_sub_dir(self):
        """Test in_sub_dir() method."""
        self.assertFalse(self.pf.in_sub_dir())

    # TODO - how to test update_relative_paths()

    def test_load_project_files(self):
        """Test load_project_files() method."""
        files = ProjectFile.load_project_files()
        self.assertGreater(len(files), 0)

    def test_block_tag_name(self):
        """Test ProjectFile.Block tag_name() method."""
        self.assertEqual(self.block.tag_name(), '{% block title %}')
