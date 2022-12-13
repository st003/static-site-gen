"""
Unit tests for HTML minifier.

Run with: python -m unittest tests.test_minify_html
"""

import unittest

from sitegen.minifiers.html_minifier import minify_html

class TestHTMLMinifier(unittest.TestCase):

    def test_tabs(self):
        """String with tabs."""

        tabs = '<h1>pre\tpost</h1>\t'
        minifed_text = []

        for char in minify_html(tabs):
            minifed_text.append(char)

        minified_str = ''.join(minifed_text)
        self.assertEqual(minified_str, '<h1>prepost</h1>')

    def test_newlines(self):
        """String with newlines."""

        newlines = '<h1>pre\npost</h1>\n'
        minifed_text = []

        for char in minify_html(newlines):
            minifed_text.append(char)

        minified_str = ''.join(minifed_text)
        self.assertEqual(minified_str, '<h1>prepost</h1>')

    def test_carriage_returns(self):
        """String with carriage returns."""

        carriage_return = '<h1>abc</h1>\r'
        minifed_text = []

        for char in minify_html(carriage_return):
            minifed_text.append(char)

        minified_str = ''.join(minifed_text)
        self.assertEqual(minified_str, '<h1>abc</h1>')

    def test_neighboring_spaces(self):
        """String with neighboring spaces."""

        neighboring_spaces = '<h1>Hello,     World!</h1>'
        minifed_text = []

        for char in minify_html(neighboring_spaces):
            minifed_text.append(char)

        minified_str = ''.join(minifed_text)
        self.assertEqual(minified_str, '<h1>Hello, World!</h1>')

    def test_leading_whitespace(self):
        """String with leading whitespace."""

        leading_whitespace = ' \t\n\r\f\v<!DOCTYPE html>'
        minifed_text = []

        for char in minify_html(leading_whitespace):
            minifed_text.append(char)

        minified_str = ''.join(minifed_text)
        self.assertEqual(minified_str, '<!DOCTYPE html>')

    def test_spaces_between_tags(self):
        """Spaces between tags."""

        spaces = '<div>   <p></p></div>'
        minifed_text = []

        for char in minify_html(spaces):
            minifed_text.append(char)

        minified_str = ''.join(minifed_text)
        self.assertEqual(minified_str, '<div><p></p></div>')

    def test_html_tags_with_valid_spaces(self):
        """Inline spaces nested within html tags."""

        inline_spaces = '<div> <p>Here is a <a>link</a> to click</p></div>'
        minifed_text = []

        for char in minify_html(inline_spaces):
            minifed_text.append(char)

        minified_str = ''.join(minifed_text)
        self.assertEqual(minified_str, '<div><p>Here is a <a>link</a> to click</p></div>')

    def test_attributes(self):
        """Test html attributes."""

        attributes = '<html lang="en"></html>'
        minifed_text = []

        for char in minify_html(attributes):
            minifed_text.append(char)

        minified_str = ''.join(minifed_text)
        self.assertEqual(minified_str, '<html lang="en"></html>')

    def test_comment(self):
        """String with only comments."""

        comment = '<!-- test comment -->'
        minifed_text = []

        for char in minify_html(comment):
            minifed_text.append(char)

        minified_str = ''.join(minifed_text)
        self.assertEqual(len(minified_str), 0)

    def test_inline_comment(self):
        """String with mix of comments and non-comments."""

        comment = '<p>paragraph <!-- comment--> with a comment inside</p>'
        minifed_text = []

        for char in minify_html(comment):
            minifed_text.append(char)

        minified_str = ''.join(minifed_text)
        self.assertEqual(minified_str, '<p>paragraph with a comment inside</p>')

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
