"""
This module defines type aliases used internally in the DXMiner package to improve type consistency
and readability. These types are intended for use by developers working on the package and should not
be exposed as part of the public API.

Types Defined:
- DataFrameType: Alias for either a pandas or polars DataFrame.
- SeriesType: Alias for either a pandas or polars Series.
- ArrayLike: Alias for array-like structures (e.g., lists, NumPy arrays).
- PathType: Alias for file paths, allowing strings or Path objects.
- DataFrameList: List of pandas or polars DataFrames.
- DataFrameDict: Dictionary of DataFrames, keyed by strings.
- Numeric: Union of int and float for numerical data types.
- StringType: Alias for strings.
- ColumnName: Alias for either strings or integers used as column names.
- ColumnList: List of column names (strings or integers).
- NumRowType: Alias for rows containing numeric values (e.g., float, int, str).
- RowType: Alias for a row of data represented as a dictionary or list.
- IndexType: Alias for pandas or polars index types (i.e., for referencing rows).
- DataFrameFunction: Alias for functions that transform a DataFrame.
- RowFunction: Alias for functions that transform individual rows of data.
- DataFrameTuple: Tuple of DataFrames.
- OptionalDataFrame: DataFrame that could be None.
- MetadataType: Dictionary for storing metadata or configuration options.
- NumericList: List of numeric values (e.g., for storing statistics or results).
- OptionalMetadata: Metadata that could be None.
- ExceptionType: Generic exception type, used to represent an exception or error message.

Note: This module is intended for internal use only.
"""

from pathlib import Path
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import numpy as np
import pandas as pd
import polars as pl

# DataFrame type that could be either pandas or polars
DataFrameType = Union[pd.DataFrame, pl.DataFrame]

# List of DataFrames
DataFrameList = List[DataFrameType]

# Series type for pandas or polars
SeriesType = Union[pd.Series, pl.Series]

# Dict of DataFrames with string keys
DataFrameDict = Dict[str, DataFrameType]

# Numeric columns (e.g., for statistics)
Numeric = Union[int, float]

# Alias for strings
StringType = str

# Alias for column names (could be strings or integers)
ColumnName = Union[str, int]

# List of column names
ColumnList = List[ColumnName]

# Alias for rows containing numeric values
NumRowType = List[Union[str, float, int]]

# Alias for rows of data, represented as lists or dictionaries
RowType = Union[Dict[ColumnName, Any], List[Any]]

# Index type for row indexing (could be pandas or polars index)
IndexType = Union[pd.Index, pl.Index]

# Array-like structures (e.g., lists or NumPy arrays)
ArrayLike = Union[List, np.ndarray]

# Alias for file paths, allowing either strings or Path objects
PathType = Union[str, Path]

# Function type for functions taking a DataFrame and returning a DataFrame
DataFrameFunction = Callable[[DataFrameType], DataFrameType]

# Function type for transformations that operate on individual rows
RowFunction = Callable[[RowType], RowType]

# Tuple of DataFrames (useful when returning multiple DataFrames)
DataFrameTuple = Tuple[DataFrameType, DataFrameType]

# Optional data, allowing for None values
OptionalDataFrame = Optional[DataFrameType]

# General object with string key and any value (useful for metadata, configurations)
MetadataType = Dict[str, Any]

# List of numeric values (useful for storing statistics, index values, etc.)
NumericList = List[Numeric]

# Optional metadata for additional context when performing operations
OptionalMetadata = Optional[MetadataType]

# Generic exception type (for handling errors in the package)
ExceptionType = Union[Exception, str]
