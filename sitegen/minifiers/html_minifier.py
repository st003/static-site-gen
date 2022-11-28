"""
HTML minifier removes:

1. Whitespace not wrapped by html tags
2. Tabs, newlines, and carriage returns
3. Comments
"""

import re
from typing import Generator, Pattern

# regex patterns

html_open: Pattern = re.compile(r'<')
html_close_start: Pattern = re.compile(r'</')
html_close_end: Pattern = re.compile(r'>')
html_whitespace: Pattern = re.compile(r'\t|\n|\r|\f|\v')
non_html_whitespace: Pattern = re.compile(r'\s')
html_comment_start: Pattern = re.compile(r'<!--')
html_comment_end: Pattern = re.compile(r'-->')

# flags
html_flag: bool = False
html_close_flag: bool = False
comment_flag: bool = False


def minify_html(file_text: str) -> Generator[str, None, None]:

    global comment_flag
    global html_flag
    global html_close_flag

    for pos, char in enumerate(file_text):

        # html
        if html_flag:

            if html_close_flag and html_close_end.match(char):
                html_flag = False
                html_close_flag = False

            # look at the next char
            elif html_close_start.match(file_text[pos:(pos + 2)]):
                html_close_flag = True

            else:
                if html_whitespace.match(char):
                    continue

        else:

            if html_open.match(char):
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
