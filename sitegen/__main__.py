"""Main entry point for program."""

import argparse
import logging
import traceback
import sys

from .config import log
from .new import new_project
from .run import run


def main():

    try:

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
            log.setLevel(logging.INFO)
        elif args.debug:
            log.setLevel(logging.DEBUG)
        else:
            # log level defaults to WARN
            pass

        if args.new:
            new_project()
        else:
            run()

    except KeyboardInterrupt:
        log.error('\nProgram exited.')
        sys.exit(0)

    except Exception:
        log.error(f'\n{traceback.format_exc()}')
        sys.exit(1)


if __name__ == '__main__':
    main()
