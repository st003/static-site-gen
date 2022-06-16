"""
Unit tests for Layout class

Run with: python -m unittest tests.test_layout
"""

import unittest

from sitegen.components.layout import Layout


class TestLayout(unittest.TestCase):
    """Layout tests use files in example directory."""

    @classmethod
    def setUpClass(cls):
        """Load base layout from examples."""
        cls.layout = Layout('base.html')

    def test_init(self):
        """Check base was loaded correctly."""
        self.assertIsNotNone(self.layout)
        self.assertEqual(self.layout.file_name, 'base.html')
        self.assertIsNotNone(self.layout.lines)

    def test_get_name(self):
        """Test get_name() method."""
        self.assertEqual(self.layout.get_name(), 'base')

    # TODO - integration test for compile()

    def test_get_all(self):
        """Test get_all() method."""
        self.assertGreater(len(self.layout.get_all()), 0)
