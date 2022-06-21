"""
Unit tests for ProjectFile class. ProjectFile tests use files in example
directory.

Run with: python -m unittest tests.test_projectfile
"""

import unittest

from sitegen.components.projectfile import ProjectFile
from sitegen.config import EX_PROJECT_PATH


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

    def test_get_extention(self):
        """Test get_extention() method."""
        self.assertEqual(self.pf.get_extention(), 'html')

    def test__str__(self):
        """Test to_string() method."""
        self.assertTrue(isinstance(str(self.pf), str))

    def test_extends_layout(self):
        """Test extends_layout() method."""
        self.assertTrue(self.pf.extends_layout())

    def test_dir_level(self):
        """Test dir_level() method."""
        sub_page = ProjectFile('subpage/index.html', path=EX_PROJECT_PATH)
        sub_sub_page = ProjectFile('subpage/subsubpage/index.html', path=EX_PROJECT_PATH)

        self.assertEqual(self.pf.dir_level(), 0)
        self.assertEqual(sub_page.dir_level(), 1)
        self.assertEqual(sub_sub_page.dir_level(), 2)

    def test_in_sub_dir(self):
        """Test in_sub_dir() method."""
        self.assertFalse(self.pf.in_sub_dir())

    # TODO - how to test update_relative_paths()

    def test_load_project_files(self):
        """Test load_project_files() method."""
        files = ProjectFile.load_project_files(base_path=EX_PROJECT_PATH)
        self.assertGreater(len(files), 0)

    def test_block_tag_name(self):
        """Test ProjectFile.Block tag_name() method."""
        self.assertEqual(self.block.tag_name(), '{% block title %}')
