"""
Top-level package for DXMiner.
"""

__author__ = "Dr Saad Laouadi"
__email__ = "dr.saad.laouadi@gmail.com"
__version__ = "0.1.0"

import polars as pl

# Configure Polars to display all columns without truncation
pl.Config.set_tbl_cols(-1)
