import logging
import os
import shutil

from .components.layout import Layout
from .components.projectfile import ProjectFile
from .components.snippet import Snippet

from .config import DIST_PATH, log

def run():

    if (os.path.exists(DIST_PATH)):
        shutil.rmtree(DIST_PATH)
    os.mkdir(DIST_PATH)

    log.info('Loading Layouts...')
    layouts = Layout.get_all()
    log.debug(layouts)

    log.info('Loading Snippets...')
    snippets = Snippet.get_all()
    log.debug(snippets)

    log.info('Loading ProjectFiles...')
    project_files = ProjectFile.load_project_files()
    log.debug(f'Project files: {project_files}')

    for pf in project_files:
        if pf.get_extention() in ProjectFile.HTML_TYPES:
            log.info(f'Compiling ProjectFile: {pf.file_name}')
            if pf.extends_layout():
                layout = layouts.get(pf.layout_name)
                pf.lines = layout.compile(pf)
            pf.update_relative_paths()
            pf.lines = Snippet.insert(pf, snippets)

        if (pf.in_sub_dir()):
            sub_dir = f'{DIST_PATH}/{os.path.dirname(pf.file_name)}'
            os.makedirs(sub_dir, exist_ok=True)

        with open(f'{DIST_PATH}/{pf.file_name}', 'w', newline='') as outfile:
            outfile.writelines(pf.lines)

    print(f'Static site generation complete. Output files exported to: {DIST_PATH}/')
