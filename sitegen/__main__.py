"""Main entry point for program."""

import argparse
import logging
import sys
import traceback

from .config import log
from .exceptions import TagSyntaxError
from .new import new_project
from .run import run
from .io import clear_dist


def main():

    try:

        parser = argparse.ArgumentParser(prog='python -m sitegen')

        parser.add_argument('-n', '--new',
                            action='store_true',
                            help='Creates a new project folder')

        parser.add_argument('-e', '--example',
                            action='store_true',
                            help='Export examples')

        parser.add_argument('-v', '--verbose',
                            action='store_true',
                            help='Enables verbose output')

        parser.add_argument('-d', '--debug',
                            action='store_true',
                            help='Enables debug output')


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
        elif args.example:
            run(use_examples=True)
        else:
            run()

    except KeyboardInterrupt:
        log.error('\nProgram exited.\n')
        clear_dist()
        sys.exit(0)

    except TagSyntaxError as syntax_error:
        log.error(f'{syntax_error}\nProgram exited.\n')
        clear_dist()
        sys.exit(1)

    except Exception:
        log.error(f'\n{traceback.format_exc()}\n')
        clear_dist()
        sys.exit(1)


if __name__ == '__main__':
    main()
