"""
Unit tests for Snippet class. Snippet tests use files in example directory.

Run with: python -m unittest tests.test_snippet
"""

import unittest

from sitegen.components.snippet import Snippet
from sitegen.components.projectfile import ProjectFile
from sitegen.config import EX_SNIPPETS_PATH, EX_PROJECT_PATH


class TestSnippet(unittest.TestCase):

    snippet: Snippet = Snippet('ipsum.html', path=EX_SNIPPETS_PATH)

    def test_init(self) -> None:
        """Check hello was loaded correctly."""
        self.assertIsNotNone(self.snippet)
        self.assertEqual(self.snippet.file_name, 'ipsum.html')
        self.assertGreater(len(self.snippet.lines), 0)

    def test_tag_name(self) -> None:
        """Test tag_name() method."""
        self.assertEqual(self.snippet.tag_name(), '{{ ipsum }}')

    def test_insert(self) -> None:
        """Test insert() method."""
        pf: ProjectFile = ProjectFile('index.html', path=EX_PROJECT_PATH)
        pf.lines = Snippet.insert(pf, [self.snippet])
        text_location: int = str(pf).find('<p>Lorem ipsum')
        # str.find() returns -1 when match is not found
        self.assertNotEqual(text_location, -1)

    def test_get_all(self) -> None:
        """Test get_all() method."""
        self.assertGreater(len(Snippet.get_all(path=EX_SNIPPETS_PATH)), 0)
