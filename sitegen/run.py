"""Core static site generation logic."""

import os
import shutil
import sys
import time

from .components.layout import Layout
from .components.projectfile import ProjectFile
from .components.snippet import Snippet

from .config import DIST_PATH, log, PROJECT_PATH, EX_LAYOUTS_PATH, EX_PROJECT_PATH, EX_SNIPPETS_PATH

def run(use_examples=False):

    if use_examples:
        print('Generating output using examples...')

    if not os.path.exists(PROJECT_PATH):
        raise FileNotFoundError('Project source directory cannot be located.')

    if os.path.exists(DIST_PATH):
        shutil.rmtree(DIST_PATH)
    os.mkdir(DIST_PATH)

    start_time = time.perf_counter()

    log.info('Loading Layouts...')
    if use_examples:
        layouts = Layout.get_all(path=EX_LAYOUTS_PATH)
    else:
        layouts = Layout.get_all()
    log.debug(layouts)

    log.info('Loading Snippets...')
    if use_examples:
        snippets = Snippet.get_all(path=EX_SNIPPETS_PATH)
    else:
        snippets = Snippet.get_all()
    log.debug(snippets)

    log.info('Loading ProjectFiles...')
    if use_examples:
        project_files = ProjectFile.load_project_files(base_path=EX_PROJECT_PATH)
    else:
        project_files = ProjectFile.load_project_files()
    if not len(project_files):
        log.error(f'There are no files in {PROJECT_PATH}')
        sys.exit(0)

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

    end_time = time.perf_counter()
    exec_time = round((end_time - start_time), 5)

    print(f'\nStatic site generation complete. Output files exported to: {DIST_PATH}/')
    print(f'Execuion time: {exec_time} seconds')
