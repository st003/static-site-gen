import logging
import os
import shutil

from components.layout import Layout
from components.page import Page
from components.snippet import Snippet

from config import DIST_PATH, LOG_FORMAT

def sitegen():

    LOG_LEVEL = logging.ERROR
    logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)

    if (os.path.exists(DIST_PATH)):
        shutil.rmtree(DIST_PATH)
    os.mkdir(DIST_PATH)

    logging.info('Loading Layouts...')
    layouts = Layout.get_all()
    logging.debug(layouts)

    logging.info('Loading Snippets...')
    snippets = Snippet.get_all()
    logging.debug(snippets)

    logging.info('Loading Pages...')
    pages = Page.load_pages()
    logging.debug(pages)

    for page in pages:
        if page.get_type() in Page.HTML_TYPES:
            logging.info(f'Compiling page: {page.relative_path()}')
            if page.uses_layout():
                layout = layouts.get(page.layout_name)
                page.lines = layout.compile(page)
            page.update_relative_paths()
            page.lines = Snippet.insert(page.lines, snippets)

        if (page.in_sub_dir()):
            sub_dir = f'{DIST_PATH}/{os.path.dirname(page.relative_path())}'
            os.makedirs(sub_dir, exist_ok=True)

        with open(f'{DIST_PATH}/{page.relative_path()}', 'w', newline='') as outfile:
            outfile.writelines(page.lines)

    # TODO - user sys stdout instead?
    print(f'Static site generation complete. Output files exported to: {DIST_PATH}/')

if __name__ == '__main__':
    sitegen()
