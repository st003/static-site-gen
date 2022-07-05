"""New project logic."""

import os
import shutil
import sys

from .config import log


def new_project():

    if (os.path.exists('project')):
        while True:
            res = input('A project folder already exists. Would you like to delete it? [y/n]: ')
            if res.lower() == 'y':
                shutil.rmtree('project')
                print('Existing project folder deleted.')
                break
            elif res.lower() == 'n':
                sys.exit('New project creation cancelled.')
            else:
                print('input not recognized. Please try again.')

    log.info('Creating new project folder.')

    os.makedirs('project/source')
    log.debug('created project/source folder')

    os.makedirs('project/layouts')
    log.debug('created project/layouts folder')

    os.makedirs('project/snippets')
    log.debug('created project/snippets folder')

    # TODO - add support for custom project folder names?
    print('New project folder called "project" created')
