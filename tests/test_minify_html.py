"""
Unit tests for HTML minifier.

Run with: python -m unittest tests.test_minify_html
"""

import unittest

from sitegen.minifiers.html_minifier import minify_html

class TestHTMLMinifier(unittest.TestCase):

    def test_tabs(self) -> None:
        """String with tabs."""

        tabs: str = '<h1>pre\tpost</h1>\t'
        minifed_text: list[str] = []

        for char in minify_html(tabs):
            minifed_text.append(char)

        minified_str: str = ''.join(minifed_text)
        self.assertEqual(minified_str, '<h1>prepost</h1>')

    def test_newlines(self) -> None:
        """String with newlines."""

        newlines: str = '<h1>pre\npost</h1>\n'
        minifed_text: list[str] = []

        for char in minify_html(newlines):
            minifed_text.append(char)

        minified_str: str = ''.join(minifed_text)
        self.assertEqual(minified_str, '<h1>prepost</h1>')

    def test_carriage_returns(self) -> None:
        """String with carriage returns."""

        carriage_return: str = '<h1>abc</h1>\r'
        minifed_text: list[str] = []

        for char in minify_html(carriage_return):
            minifed_text.append(char)

        minified_str: str = ''.join(minifed_text)
        self.assertEqual(minified_str, '<h1>abc</h1>')

    def test_neighboring_spaces(self) -> None:
        """String with neighboring spaces."""

        neighboring_spaces: str = '<h1>Hello,     World!</h1>'
        minifed_text: list[str] = []

        for char in minify_html(neighboring_spaces):
            minifed_text.append(char)

        minified_str: str = ''.join(minifed_text)
        self.assertEqual(minified_str, '<h1>Hello, World!</h1>')

    def test_leading_whitespace(self) -> None:
        """String with leading whitespace."""

        leading_whitespace: str = ' \t\n\r\f\v<!DOCTYPE html>'
        minifed_text: list[str] = []

        for char in minify_html(leading_whitespace):
            minifed_text.append(char)

        minified_str: str = ''.join(minifed_text)
        self.assertEqual(minified_str, '<!DOCTYPE html>')

    def test_spaces_between_tags(self) -> None:
        """Spaces between tags."""

        spaces: str = '<div>   <p></p></div>'
        minifed_text: list[str] = []

        for char in minify_html(spaces):
            minifed_text.append(char)

        minified_str: str = ''.join(minifed_text)
        self.assertEqual(minified_str, '<div><p></p></div>')

    def test_html_tags_with_valid_spaces(self) -> None:
        """Inline spaces nested within html tags."""

        inline_spaces: str = '<div> <p>Here is a <a>link</a> to click</p></div>'
        minifed_text: list[str] = []

        for char in minify_html(inline_spaces):
            minifed_text.append(char)

        minified_str: str = ''.join(minifed_text)
        self.assertEqual(minified_str, '<div><p>Here is a <a>link</a> to click</p></div>')

    def test_attributes(self) -> None:
        """Test html attributes."""

        attributes: str = '<html lang="en"></html>'
        minifed_text: list[str] = []

        for char in minify_html(attributes):
            minifed_text.append(char)

        minified_str: str = ''.join(minifed_text)
        self.assertEqual(minified_str, '<html lang="en"></html>')

    def test_comment(self) -> None:
        """String with only comments."""

        comment: str = '<!-- test comment -->'
        minifed_text: list[str] = []

        for char in minify_html(comment):
            minifed_text.append(char)

        minified_str: str = ''.join(minifed_text)
        self.assertEqual(len(minified_str), 0)

    def test_inline_comment(self) -> None:
        """String with mix of comments and non-comments."""

        comment: str = '<body>\n    <!-- comment -->\n    <h1>Hello, World!</h1>'
        minifed_text: list[str] = []

        for char in minify_html(comment):
            minifed_text.append(char)

        minified_str: str = ''.join(minifed_text)
        self.assertEqual(minified_str, '<body><h1>Hello, World!</h1>')

    def test_html_only(self) -> None:
        """A complex html file."""

        with open('tests/html_minify_source.html') as html_file:
            html: str = html_file.read()

        with open('tests/html_minify_expected.html') as html_file:
            expected: str = html_file.read()

        minified_text: list[str] = []
        for char in minify_html(html):
            minified_text.append(char)

        minified_str: str = ''.join(minified_text)

        self.assertEqual(minified_str, expected)
