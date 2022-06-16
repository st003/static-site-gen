"""
Unit tests for Snippet class

Run with: python -m unittest tests.test_snippet
"""

import unittest

from sitegen.components.snippet import Snippet


class TestSnippet(unittest.TestCase):
    """Snippet tests use files in example directory."""

    @classmethod
    def setUpClass(cls):
        """Load base layout from examples."""
        cls.snippet = Snippet('hello.html')

    def test_init(self):
        """Check hello was loaded correctly."""
        self.assertIsNotNone(self.snippet)
        self.assertEqual(self.snippet.file_name, 'hello.html')
        self.assertGreater(len(self.snippet.lines), 0)

    def test_tag_name(self):
        """Test tag_name() method."""
        self.assertEqual(self.snippet.tag_name(), '{{ hello }}')

    def test_to_string(self):
        """Test to_string() method."""
        self.assertTrue(isinstance(self.snippet.to_string(), str))

    # TODO - integration test for insert()

    def test_get_all(self):
        """Test get_all() method."""
        self.assertGreater(len(Snippet.get_all()), 0)