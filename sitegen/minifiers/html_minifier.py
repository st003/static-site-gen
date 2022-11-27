"""
HTML minifier removes:

1. Whitespace (tabs and spaces) not wrapped by html tags
2. Newlines and carriage returns
3. Comments
"""

import re
from typing import Generator, Pattern

# regex
html_comment_start: Pattern = re.compile(r'<!--')
html_comment_end: Pattern = re.compile(r'-->')
whitespace: Pattern = re.compile(r'\s')

# flags
comment_flag: bool = False


def minify_html(file_text: str) -> Generator[str, None, None]:

    global comment_flag

    for pos, char in enumerate(file_text):

        # TODO - HTML tag wrappers
        # TODO - inline css
        # TODO - inline javascript

        if (comment_flag):
            # look at last 3 chars
            if html_comment_end.match(file_text[(pos - 2):(pos + 1)]):
                comment_flag = False
                continue
            else:
                continue

        # looks at next 4 chars
        elif html_comment_start.match(file_text[pos:(pos + 4)]):
            comment_flag = True
            continue

        elif whitespace.match(char):
            continue

        yield char

    return None
