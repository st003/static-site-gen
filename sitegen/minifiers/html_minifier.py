"""
HTML minifier removes:

1. Whitespace (tabs and spaces) not wrapped by html tags
2. Newlines and carriage returns
3. Comments
"""

from typing import Generator


comment_flag: bool = False


def minify_html(file_text: str) -> Generator[str, None, None]:

    global comment_flag

    for pos, char in enumerate(file_text):

        # TODO - HTML tag wrappers
        # html tags can't have spaces, so maybe stop, sub-string scan until
        # find a space or a closing tag, then set flag to True until you find
        # the closing tag. Maybe save the tag name internally?

        if (comment_flag):
            if file_text[(pos - 2):(pos + 1)] == '-->':
                comment_flag = False
                continue
            else:
                continue

        elif file_text[pos:(pos + 4)] == '<!--':
            comment_flag = True
            continue

        elif char == ' ':
            continue

        elif char == '\t':
            continue

        elif char == '\n':
            continue

        elif char == '\r':
            continue

        yield char

    return None
