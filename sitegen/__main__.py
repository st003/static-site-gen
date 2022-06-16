import logging
import os
import shutil

from components.layout import Layout
from components.projectfile import ProjectFile
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

    logging.info('Loading ProjectFiles...')
    project_files = ProjectFile.load_project_files()
    logging.debug(project_files)

    for pf in project_files:
        if pf.get_extention() in ProjectFile.HTML_TYPES:
            logging.info(f'Compiling ProjectFile: {pf.relative_path()}')
            if pf.extends_layout():
                layout = layouts.get(pf.layout_name)
                pf.lines = layout.compile(pf)
            pf.update_relative_paths()
            pf.lines = Snippet.insert(pf, snippets)

        if (pf.in_sub_dir()):
            sub_dir = f'{DIST_PATH}/{os.path.dirname(pf.relative_path())}'
            os.makedirs(sub_dir, exist_ok=True)

        with open(f'{DIST_PATH}/{pf.relative_path()}', 'w', newline='') as outfile:
            outfile.writelines(pf.lines)

    # TODO - user sys stdout instead?
    print(f'Static site generation complete. Output files exported to: {DIST_PATH}/')

if __name__ == '__main__':
    sitegen()
