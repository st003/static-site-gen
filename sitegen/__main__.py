"""Main entry point for program."""

import argparse
import logging

from sitegen.new import new_project
from sitegen.run import run


def main():

    parser = argparse.ArgumentParser(prog='python -m sitegen')

    parser.add_argument('-d', '--debug',
                        action='store_true',
                        help='Enables debug output')

    parser.add_argument('-n', '--new',
                        action='store_true',
                        help='Creates a new project folder')

    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        help='Enables verbose output')

    args = parser.parse_args()

    if args.verbose:
        log_level = logging.INFO
    elif args.debug:
        log_level = logging.DEBUG
    else:
        log_level = logging.ERROR

    if args.new:
        new_project()
    else:
        run(log_level=log_level)


if __name__ == '__main__':
    main()
