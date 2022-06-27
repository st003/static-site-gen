"""
Unit tests for Snippet class. Snippet tests use files in example directory.

Run with: python -m unittest tests.test_snippet
"""

import unittest

from sitegen.components.snippet import Snippet
from sitegen.config import EX_SNIPPETS_PATH


class TestSnippet(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Load base layout from examples."""
        cls.snippet = Snippet('ipsum.html', path=EX_SNIPPETS_PATH)

    def test_init(self):
        """Check hello was loaded correctly."""
        self.assertIsNotNone(self.snippet)
        self.assertEqual(self.snippet.file_name, 'ipsum.html')
        self.assertGreater(len(self.snippet.lines), 0)

    def test_tag_name(self):
        """Test tag_name() method."""
        self.assertEqual(self.snippet.tag_name(), '{{ ipsum }}')

    # TODO - integration test for insert()

    def test_get_all(self):
        """Test get_all() method."""
        self.assertGreater(len(Snippet.get_all(path=EX_SNIPPETS_PATH)), 0)