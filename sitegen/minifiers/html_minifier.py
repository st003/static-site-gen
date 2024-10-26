"""
HTML minifier removes:

1. Tabs, newlines, and carriage returns
2. Comments
3. Excess whitespace
"""

COMMENT_START_TAG: str = '<!--'
COMMENT_END_TAG: str = '-->'
SINGLE_SPACE: str = ' '
HTML_TAG_OPEN: str = '<'
NON_SPACE_WHITESPACE_CHARS: set[str] = {'\t', '\n', '\r', '\f', '\v'}


def minify_html(file_text: str) -> str:

    tokens: list[str] = []

    comment_flag: bool = False
    html_tag_flag: bool = False

    for pos, char in enumerate(file_text):

        try:

            # comments
            if not comment_flag:
                potential_start_tag: str = file_text[pos:(pos + 4)]
                if potential_start_tag == COMMENT_START_TAG:
                    comment_flag = True

            if comment_flag:

                # do not try to look before the start of the string
                if pos < 2:
                    continue

                potential_end_tag: str = file_text[(pos - 2):(pos + 1)]
                if potential_end_tag == COMMENT_END_TAG:
                    comment_flag = False

                continue

            # newlines, carriage returns, etc.
            if char in NON_SPACE_WHITESPACE_CHARS:
                continue

            # TODO - if last char was new line, you can skip all spaces until tag open?

            # excess spaces
            if char == HTML_TAG_OPEN:
                html_tag_flag = True

            # TODO - check for <pre> here

            if char == SINGLE_SPACE:

                # check for double space
                if file_text[pos + 1] == SINGLE_SPACE:
                    continue

            tokens.append(char)

        except IndexError:
            continue

    return ''.join(tokens)

