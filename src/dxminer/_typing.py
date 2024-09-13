"""
_typing.py

This module defines type aliases used internally in the DXMiner package to improve type consistency
and readability. These types are intended for use by developers working on the package and should not
be exposed as part of the public API.

Types Defined:
- DataFrameType: Alias for either a pandas or polars DataFrame.
- SeriesType: Alias for either a pandas or polars Series.
- ArrayLike: Alias for array-like structures (e.g., lists, NumPy arrays).
- PathType: Alias for file paths, allowing strings or Path objects.

Note: This module is intended for internal use only.
"""


from typing import Union, List, Dict
import pandas as pd
import polars as pl

# Generic DataFrame type that could be either pandas or polars
DataFrameType = Union[pd.DataFrame, pl.DataFrame]

# Lists of DataFrames
DataFrameList = List[DataFrameType]

# Dict of DataFrames with string keys
DataFrameDict = Dict[str, DataFrameType]

# Numeric columns (e.g., for statistics)
Numeric = Union[int, float]