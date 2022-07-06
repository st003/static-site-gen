import logging
import os.path


# determine program install location
install_dir = os.path.dirname(__file__).replace('/sitegen', '')

# logging
log_format = logging.Formatter('%(levelname)s - %(message)s')
log_handler = logging.StreamHandler()
log_handler.setFormatter(log_format)

log = logging.getLogger('sitegen')
log.setLevel(logging.WARN)
log.addHandler(log_handler)

# project paths
PROJECT_PATH = 'project/source'
LAYOUTS_PATH = 'project/layouts'
SNIPPETS_PATH = 'project/snippets'

# examples paths
EX_PROJECT_PATH = f'{install_dir}/examples/source'
EX_LAYOUTS_PATH = f'{install_dir}/examples/layouts'
EX_SNIPPETS_PATH = f'{install_dir}/examples/snippets'

# test paths
TEST_PATH = f'{install_dir}/tests'
