"""Main entry point for program."""

import argparse

from sitegen.new import new_project
from sitegen.run import run


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--new',
                        action='store_true',
                        help='Creates a new project folder')
    args = parser.parse_args()

    if args.new:
        new_project()
    else:
        run()


if __name__ == '__main__':
    main()
