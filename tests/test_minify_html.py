"""
Unit tests for HTML minifier.

Run with: python -m unittest tests.test_minify_html
"""

import unittest

from sitegen.minifiers.html_minifier import minify_html

class TestHTMLMinifier(unittest.TestCase):

    def test_comment(self):
        """String with only comments."""

        comment = '<!-- test comment -->'
        minifed_text = []

        for char in minify_html(comment):
            minifed_text.append(char)

        minified_str = ''.join(minifed_text)
        self.assertEqual(len(minified_str), 0)

    def test_comment_with_text(self):
        """String with mix of comments and non-comments."""

        comment = 'pre <!-- comment --> post'
        minifed_text = []

        for char in minify_html(comment):
            minifed_text.append(char)

        minified_str = ''.join(minifed_text)
        self.assertEqual(minified_str, 'prepost')

    def test_space(self):
        """String with spaces only."""

        comment = '     '
        minifed_text = []

        for char in minify_html(comment):
            minifed_text.append(char)

        minified_str = ''.join(minifed_text)
        self.assertEqual(len(minified_str), 0)

    def test_space_with_text(self):
        """String with spaces only."""

        comment = 'a b c'
        minifed_text = []

        for char in minify_html(comment):
            minifed_text.append(char)

        minified_str = ''.join(minifed_text)
        self.assertEqual(minified_str, 'abc')

    def test_tabs(self):
        """String with tabs."""

        comment = 'pre\tpost\t'
        minifed_text = []

        for char in minify_html(comment):
            minifed_text.append(char)

        minified_str = ''.join(minifed_text)
        self.assertEqual(minified_str, 'prepost')

    def test_newlines(self):
        """String with newlines."""

        comment = 'pre\npost\n'
        minifed_text = []

        for char in minify_html(comment):
            minifed_text.append(char)

        minified_str = ''.join(minifed_text)
        self.assertEqual(minified_str, 'prepost')

    def test_carriage_returns(self):
        """String with carriage returns."""

        comment = 'abc\r'
        minifed_text = []

        for char in minify_html(comment):
            minifed_text.append(char)

        minified_str = ''.join(minifed_text)
        self.assertEqual(minified_str, 'abc')
