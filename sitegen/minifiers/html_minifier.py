"""
HTML minifier removes:

1. Comments
2. Tabs, newlines, and carriage returns
3. Whitespace not wrapped by html tags
"""

import re
from typing import Generator, Pattern

# regex patterns
space: Pattern = re.compile(r' ')
double_space: Pattern = re.compile(r'  ')
space_before_tag: Pattern = re.compile(r' <')
non_space_whitespace_symbols: Pattern = re.compile(r'\t|\n|\r|\f|\v')
html_tag_left_bracket: Pattern = re.compile(r'<')
html_tag_right_bracket: Pattern = re.compile(r'>')
html_comment_start: Pattern = re.compile(r'<!--')
html_comment_end: Pattern = re.compile(r'-->')

# flags
comment_flag: bool = False
tag_bracket_right: bool = False
potential_inline_tag: bool = False


def minify_html(file_text: str) -> Generator[str, None, None]:

    global comment_flag
    global tag_bracket_right
    global potential_inline_tag

    # simple pass (non-space whitespace & comments)
    simple_pass_buffer: list[str] = []

    for pos, char in enumerate(file_text):

        if non_space_whitespace_symbols.match(char):
            continue

        elif comment_flag:

            # look at the last 3 chars
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

        simple_pass_buffer.append(char)

    simple_pass_result: str = ''.join(simple_pass_buffer)

    # complex pass (single spaces, inline CSS and JavaScript)
    for pos, char in enumerate(simple_pass_result):

        # evaluate spaces
        if space.match(char):
            next_two_chars: str = simple_pass_result[pos:pos + 2]

            # elminate extra spaces
            if double_space.match(next_two_chars):
                continue

            # evaluate spaces before tags
            elif space_before_tag.match(next_two_chars) and not potential_inline_tag:
                continue

        # check for html tag brackets
        elif html_tag_right_bracket.match(char):
            tag_bracket_right = True

        elif html_tag_left_bracket.match(char):
            tag_bracket_right = False
            potential_inline_tag = False

        # check for guaranteed yields directly following an html tag
        elif tag_bracket_right:
            potential_inline_tag = True

        # TODO - inline css
        # TODO - inline javascript

        yield char

    # reset flags to initial state
    comment_flag = False
    tag_bracket_right = False
    potential_inline_tag = False

    return None
