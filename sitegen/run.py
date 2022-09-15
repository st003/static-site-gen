"""Core static site generation logic."""

import os.path
import sys
import time

import sitegen
from .config import log, LAYOUTS_PATH, PROJECT_PATH, SNIPPETS_PATH
from .config import EX_LAYOUTS_PATH, EX_PROJECT_PATH, EX_SNIPPETS_PATH
from .components.layout import Layout
from .components.projectfile import ProjectFile
from .components.snippet import Snippet
from .io import clear_dist


def run(use_examples: bool = False):

    src_location: str = PROJECT_PATH
    layouts_path: str = LAYOUTS_PATH
    snippets_path: str = SNIPPETS_PATH

    if use_examples:
        src_location = EX_PROJECT_PATH
        layouts_path = EX_LAYOUTS_PATH
        snippets_path = EX_SNIPPETS_PATH

    if not os.path.exists(src_location):
        raise FileNotFoundError('Project source directory cannot be located.')

    print(f'\nGenerating output from: {src_location}')

    clear_dist()

    start_time: float = time.perf_counter()

    log.info('Loading Layouts...')
    layouts: dict[str, Layout] = Layout.get_all(path=layouts_path)
    log.debug(layouts)

    log.info('Loading Snippets...')
    snippets: list[Snippet] = Snippet.get_all(path=snippets_path)
    log.debug(snippets)

    log.info('Loading ProjectFiles...')
    project_files: list[ProjectFile] = ProjectFile.load_project_files(src_location)

    if not len(project_files):
        log.error(f'There are no files in {src_location}')
        sys.exit(0)

    log.info('Compiling and exporting ProjectFiles...')
    for pf in project_files:
        if pf.is_html():
            log.debug(f'Compiling ProjectFile: {pf.file_name}')
            if pf.extends_layout():
                layout = layouts.get(pf.layout_name)
                pf.lines = layout.compile(pf)
            pf.lines = Snippet.insert(pf, snippets)
            pf.update_relative_paths()
        pf.save_file()

    end_time: float = time.perf_counter()
    exec_time: float = round((end_time - start_time), 5)

    print(f'\nStatic site generation complete. Output files exported to: {sitegen.DIST_PATH}')
    print(f'Execution time: {exec_time} seconds\n')
