"""
Unit tests for Layout class. Layout tests use files in examples directory.

Run with: python -m unittest tests.test_layout
"""

import unittest
from typing import Optional

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

    def test_get_block_name_from_line(self) -> None:
        """Test get_block_name_from_line() method."""
        line: str = 'asdfg{% block name %}sdfsdfd'
        name: Optional[str] = Layout.get_block_name_from_line(line)
        self.assertEqual(name, 'name')

    def test_get_block_name_from_line_with_no_block_tag(self) -> None:
        """Test get_block_name_from_line() method when the line has no block tag."""
        line: str = 'asdfgsdfsdfd'
        name: Optional[str] = Layout.get_block_name_from_line(line)
        self.assertEqual(name, None)

    def test_get_all(self) -> None:
        """Test get_all() method."""
        self.assertGreater(len(self.layout.get_all(path=EX_LAYOUTS_PATH)), 0)
