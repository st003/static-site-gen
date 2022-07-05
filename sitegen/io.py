"""File Read and Write functions."""

import os
import os.path
import shutil

from .config import DIST_PATH


def clear_dist():
    """Create empty dist folder."""
    if os.path.exists(DIST_PATH):
        shutil.rmtree(DIST_PATH)
    os.mkdir(DIST_PATH)
