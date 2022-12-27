"""
Unit tests for Component class. Component tests use files in examples directory.

Run with: python -m unittest tests.test_component
"""

import unittest

from sitegen.components.component import Component
from sitegen.config import EX_PROJECT_PATH


class TestLayout(unittest.TestCase):

    c: Component = Component('index.html', path=EX_PROJECT_PATH)

    @classmethod
    def setUpClass(cls) -> None:
        """Load index file from examples/source."""
        cls.c.load_file()

    def test_init(self) -> None:
        """Check file was loaded correctly."""
        self.assertIsNotNone(self.c)
        self.assertEqual(self.c.file_name, 'index.html')

    def test_dir_level(self) -> None:
        """Test dir_level() method."""
        sub_page: Component = Component('subpage/index.html', path=EX_PROJECT_PATH)
        sub_sub_page: Component = Component('subpage/subsubpage/index.html', path=EX_PROJECT_PATH)

        self.assertEqual(self.c.dir_level(), 0)
        self.assertEqual(sub_page.dir_level(), 1)
        self.assertEqual(sub_sub_page.dir_level(), 2)

    def test_get_extention(self) -> None:
        """Test get_extention() method."""
        self.assertEqual(self.c.get_extention(), 'html')
    
    def test_get_name(self) -> None:
        """Test get_name() method."""
        self.assertEqual(self.c.get_name(), 'index')

    def test_in_sub_dir(self) -> None:
        """Test in_sub_dir() method."""
        self.assertFalse(self.c.in_sub_dir())
    
    def test_is_html(self) -> None:
        """Test is_html() method."""
        self.assertTrue(self.c.is_html())

    def test__str__(self) -> None:
        """Test to_string() method."""
        self.assertTrue(isinstance(str(self.c), str))

