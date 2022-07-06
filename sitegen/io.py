"""File Read and Write functions."""

import os
import os.path
import shutil

import sitegen


def clear_dist():
    """Create empty dist folder."""
    if os.path.exists(sitegen.DIST_PATH):
        shutil.rmtree(sitegen.DIST_PATH)
    os.mkdir(sitegen.DIST_PATH)
