"""
Unit tests for minifiers using files.

Run with: python -m unittest tests.test_minify_on_file
"""

import unittest

from sitegen.minifiers.html_minifier import minify_html

class TestMinifiersOnFile(unittest.TestCase):

    def test_html_only(self):
        """A complex html file."""

        with open('tests/html_minify_source.html') as html_file:
            html = html_file.read()

        with open('tests/html_minify_expected.html') as html_file:
            expected = html_file.read()

        minified_text = []
        for char in minify_html(html):
            minified_text.append(char)

        minified_str = ''.join(minified_text)

        self.assertEqual(minified_str, expected)
