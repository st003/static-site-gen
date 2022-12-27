"""
Unit tests for Layout class. Layout tests use files in examples directory.

Run with: python -m unittest tests.test_layout
"""

import unittest

from sitegen.components.layout import Layout
from sitegen.components.projectfile import ProjectFile
from sitegen.config import EX_LAYOUTS_PATH, EX_PROJECT_PATH


class TestLayout(unittest.TestCase):

    layout: Layout = Layout('base.html', path=EX_LAYOUTS_PATH)

    def test_init(self) -> None:
        """Check base was loaded correctly."""
        self.assertIsNotNone(self.layout)
        self.assertEqual(self.layout.file_name, 'base.html')
        self.assertIsNotNone(self.layout.lines)

    def test_compile(self) -> None:
        """Test compile() method."""
        pf: ProjectFile = ProjectFile('index.html', path=EX_PROJECT_PATH)
        pf.lines = self.layout.compile(pf)
        layout_tag_index: int = str(pf).find('{% layout')
        # str.find() returns -1 when match is not found
        self.assertEqual(layout_tag_index, -1)

    def test_get_all(self) -> None:
        """Test get_all() method."""
        self.assertGreater(len(self.layout.get_all(path=EX_LAYOUTS_PATH)), 0)
