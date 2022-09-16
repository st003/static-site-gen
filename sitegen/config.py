import logging
import os.path


# determine program install location
install_dir: str = os.path.dirname(__file__).replace('/sitegen', '')

# logging
log_format: logging.Formatter = logging.Formatter('%(levelname)s - %(message)s')
log_handler: logging.StreamHandler = logging.StreamHandler()
log_handler.setFormatter(log_format)

log: logging.Logger = logging.getLogger('sitegen')
log.setLevel(logging.WARN)
log.addHandler(log_handler)

# project paths
PROJECT_PATH: str = 'project/source'
LAYOUTS_PATH: str = 'project/layouts'
SNIPPETS_PATH: str = 'project/snippets'

# examples paths
EX_PROJECT_PATH: str = f'{install_dir}/examples/source'
EX_LAYOUTS_PATH: str = f'{install_dir}/examples/layouts'
EX_SNIPPETS_PATH: str = f'{install_dir}/examples/snippets'

# test paths
TEST_PATH: str = f'{install_dir}/tests'
