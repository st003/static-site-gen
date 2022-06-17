import os
import shutil
import sys

def new_project():
    """Logic for creating a new project."""

    if (os.path.exists('project')):
        while True:
            res = input('A project folder already exists. Would you like to delete it? [y/n]: ')
            if res == 'y':
                shutil.rmtree('project')
                print('Existing project folder deleted.')
                break
            elif res == 'n':
                sys.exit('New project creation cancelled.')
            else:
                print('input not recognized. Please try again.')

    os.makedirs('project/source')
    os.makedirs('project/layouts')
    os.makedirs('project/snippets')

    # TODO - add support for custom project folder names?
    print('New project folder called "project" created')
