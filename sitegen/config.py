import logging

# project paths
PROJECT_PATH = 'project/source'
LAYOUTS_PATH = 'project/layouts'
SNIPPETS_PATH = 'project/snippets'

# examples paths
EX_PROJECT_PATH = 'examples/source'
EX_LAYOUTS_PATH = 'examples/layouts'
EX_SNIPPETS_PATH = 'examples/snippets'

# path to distribution directory
DIST_PATH = 'dist'

# logging
log_format = logging.Formatter('%(levelname)s - %(message)s')
log_handler = logging.StreamHandler()
log_handler.setFormatter(log_format)

log = logging.getLogger('sitegen')
log.setLevel(logging.ERROR)
log.addHandler(log_handler)
