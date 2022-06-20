import logging

# path to project source directory
PROJECT_PATH = 'examples/src'

# path to project layouts directory
LAYOUTS_PATH = 'examples/layouts'

# path to project snippets directory
SNIPPETS_PATH = 'examples/snippets'

# path to distribution directory
DIST_PATH = 'dist'

# logging
log_format = logging.Formatter('%(levelname)s - %(message)s')
log_handler = logging.StreamHandler()
log_handler.setFormatter(log_format)

log = logging.getLogger('sitegen')
log.setLevel(logging.ERROR)
log.addHandler(log_handler)
