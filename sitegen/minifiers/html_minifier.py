"""
HTML minifier removes:

1. Whitespace not wrapped by html tags
2. Tabs, newlines, and carriage returns
3. Comments
"""

import re
from typing import Generator, Pattern

# regex patterns
non_space_whitespace_symbols: Pattern = re.compile(r'\t|\n|\r|\f|\v')
html_tag_start_bracket: Pattern = re.compile(r'<')
html_comment_start: Pattern = re.compile(r'<!--')
html_comment_end: Pattern = re.compile(r'-->')

# flags
html_flag: bool = False
comment_flag: bool = False


def minify_html(file_text: str) -> Generator[str, None, None]:

    global html_flag
    global comment_flag

    for pos, char in enumerate(file_text):

        # html
        if html_flag:

            if non_space_whitespace_symbols.match(char):
                continue

            # evaluate spaces
            elif char == ' ':

                # TODO - deal with "<div> <p>" vs. "<p>link: <a>asdsad</a></p>"
                # seems like I need a flag for "> + char + space"

                # TODO - replace string compares with regex matches

                this_and_next: str = file_text[pos:pos + 2]
                if this_and_next == '  ':
                    continue
                elif this_and_next == ' <':
                    continue

        else:

            if html_tag_start_bracket.match(char):
                html_flag = True

            elif char == ' ':
                continue

        # TODO - inline css
        # TODO - inline javascript

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

        yield char

    # reset flags to initial state
    html_flag = False
    comment_flag = False

    return None
