"""
Unit tests for Layout class. Layout tests use files in examples directory.

Run with: python -m unittest tests.test_layout
"""

import unittest

from sitegen.components.layout import Layout
from sitegen.config import EX_LAYOUTS_PATH


class TestLayout(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Load base layout from examples."""
        cls.layout = Layout('base.html', path=EX_LAYOUTS_PATH)

    def test_init(self):
        """Check base was loaded correctly."""
        self.assertIsNotNone(self.layout)
        self.assertEqual(self.layout.file_name, 'base.html')
        self.assertIsNotNone(self.layout.lines)

    # TODO - integration test for compile()

    def test_get_all(self):
        """Test get_all() method."""
        self.assertGreater(len(self.layout.get_all(path=EX_LAYOUTS_PATH)), 0)
