import logging
import os.path


# determine program install location
instal_dir = os.path.dirname(__file__).replace('/sitegen', '')

# project paths
PROJECT_PATH = 'project/source'
LAYOUTS_PATH = 'project/layouts'
SNIPPETS_PATH = 'project/snippets'

# examples paths
EX_PROJECT_PATH = f'{instal_dir}/examples/source'
EX_LAYOUTS_PATH = f'{instal_dir}/examples/layouts'
EX_SNIPPETS_PATH = f'{instal_dir}/examples/snippets'

# path to distribution directory
DIST_PATH = 'dist'

# logging
log_format = logging.Formatter('%(levelname)s - %(message)s')
log_handler = logging.StreamHandler()
log_handler.setFormatter(log_format)

log = logging.getLogger('sitegen')
log.setLevel(logging.WARN)
log.addHandler(log_handler)
