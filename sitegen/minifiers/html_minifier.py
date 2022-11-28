"""
HTML minifier removes:

1. Whitespace not wrapped by html tags
2. Tabs, newlines, and carriage returns
3. Comments
"""

import re
from typing import Generator, Pattern

# regex patterns
html_tag_start_bracket: Pattern = re.compile(r'<')
html_tag_close_start_bracket: Pattern = re.compile(r'</')
html_tag_end_bracket: Pattern = re.compile(r'>')
html_whitespace: Pattern = re.compile(r'\t|\n|\r|\f|\v')
non_html_padding: Pattern = re.compile(r'\n ')
non_html_whitespace: Pattern = re.compile(r'\s')
html_comment_start: Pattern = re.compile(r'<!--')
html_comment_end: Pattern = re.compile(r'-->')

# flags
html_flag: bool = False
html_padding_flag: bool = False
html_close_flag: bool = False
comment_flag: bool = False


def reset_html_minifier_flags() -> None:
    """Set global html minifier flags to False."""

    global html_flag
    global html_padding_flag
    global html_close_flag
    global comment_flag

    html_flag = False
    html_padding_flag = False
    html_close_flag = False
    comment_flag = False


def minify_html(file_text: str) -> Generator[str, None, None]:

    global html_flag
    global html_padding_flag
    global html_close_flag
    global comment_flag

    for pos, char in enumerate(file_text):

        # html
        if html_flag:

            # check for closing html bracket. ie: "</h1>"
            if html_close_flag and html_tag_end_bracket.match(char):
                html_flag = False
                html_close_flag = False

            # check for closing html bracket start. ie: "</"
            elif html_tag_close_start_bracket.match(file_text[pos:(pos + 2)]):
                html_close_flag = True

            # check for indentation using spaces
            elif non_html_padding.match(file_text[pos:(pos + 2)]):
                html_padding_flag = True
                continue

            # evalutate indentation spaces
            elif html_padding_flag:
                if non_html_whitespace.match(char):
                    continue
                else:
                    html_padding_flag = False

            else:
                if html_whitespace.match(char):
                    continue

        else:

            if html_tag_start_bracket.match(char):
                html_flag = True

            else:
                if non_html_whitespace.match(char):
                    continue

        # comments
        if comment_flag:

            # look at last 3 chars
            comment_end_check: str = file_text[(pos - 2):(pos + 1)]

            if html_comment_end.match(comment_end_check):
                comment_flag = False
                continue
            else:
                continue

        else:

            # look at next 4 chars for comment start
            comment_start_check: str = file_text[pos:(pos + 4)]

            if html_comment_start.match(comment_start_check):
                comment_flag = True
                continue

        # TODO - inline css
        # TODO - inline javascript

        yield char

    return None
