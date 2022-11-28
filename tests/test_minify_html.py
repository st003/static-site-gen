"""
Unit tests for HTML minifier.

Run with: python -m unittest tests.test_minify_html
"""

import unittest

from sitegen.minifiers.html_minifier import minify_html, reset_html_minifier_flags

class TestHTMLMinifier(unittest.TestCase):

    def setUp(self):
        reset_html_minifier_flags()

    def test_space(self):
        """String with only spaces."""

        spaces = '    '
        minifed_text = []

        for char in minify_html(spaces):
            minifed_text.append(char)

        minified_str = ''.join(minifed_text)
        self.assertEqual(len(minified_str), 0)

    def test_space_with_text(self):
        """String with non-html wrapped spaces."""

        non_wrapped_spaces = '    <h1>Hello, World!</h1>    '
        minifed_text = []

        for char in minify_html(non_wrapped_spaces):
            minifed_text.append(char)

        minified_str = ''.join(minifed_text)
        self.assertEqual(minified_str, '<h1>Hello, World!</h1>')

    def test_html_tags_with_valid_spaces(self):
        """Inline spaces nested within html tags."""

        inline_spaces = '<p>Here is a <a>link</a> to click</p>'
        minifed_text = []

        for char in minify_html(inline_spaces):
            minifed_text.append(char)

        minified_str = ''.join(minifed_text)
        self.assertEqual(minified_str, '<p>Here is a <a>link</a> to click</p>')

    def test_tabs(self):
        """String with tabs."""

        tabs = 'pre\tpost\t'
        minifed_text = []

        for char in minify_html(tabs):
            minifed_text.append(char)

        minified_str = ''.join(minifed_text)
        self.assertEqual(minified_str, 'prepost')

    def test_newlines(self):
        """String with newlines."""

        newlines = 'pre\npost\n'
        minifed_text = []

        for char in minify_html(newlines):
            minifed_text.append(char)

        minified_str = ''.join(minifed_text)
        self.assertEqual(minified_str, 'prepost')

    def test_carriage_returns(self):
        """String with carriage returns."""

        carriage_return = 'abc\r'
        minifed_text = []

        for char in minify_html(carriage_return):
            minifed_text.append(char)

        minified_str = ''.join(minifed_text)
        self.assertEqual(minified_str, 'abc')

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

        comment = '<pre><!-- comment --></post>'
        minifed_text = []

        for char in minify_html(comment):
            minifed_text.append(char)

        minified_str = ''.join(minifed_text)
        self.assertEqual(minified_str, '<pre></post>')
