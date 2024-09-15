"""
Example Usage of the `data_heads` Function in DXMiner

This example demonstrates how to use the `data_heads` function to display the heads of multiple
pandas and polars DataFrames. The `data_heads` function can handle both a list and a dictionary
of DataFrames, with separator lines for better readability.

In this example:
- We create two pandas DataFrames and two polars DataFrames with random data.
- The `data_heads` function is called twice: once with a list of DataFrames, and once with a
  dictionary of DataFrames.
- The output displays the first few rows of each DataFrame with a clearly marked separator.

"""

import pandas as pd
import polars as pl
import numpy as np
from dxminer.explore.multiple_data import data_heads
# Create random data using Pandas
pandas_df1 = pd.DataFrame({
    'A': np.random.rand(10),
    'B': np.random.rand(10),
    'C': np.random.randint(0, 100, size=10)
})

pandas_df2 = pd.DataFrame({
    'X': np.random.rand(10),
    'Y': np.random.rand(10),
    'Z': np.random.randint(0, 100, size=10)
})

# Create random data using Polars
polars_df1 = pl.DataFrame({
    'D': np.random.rand(10),
    'E': np.random.rand(10),
    'F': np.random.randint(0, 100, size=10)
})

polars_df2 = pl.DataFrame({
    'M': np.random.rand(10),
    'N': np.random.rand(10),
    'O': np.random.randint(0, 100, size=10)
})

# Using a list of DataFrames
data_heads([pandas_df1, pandas_df2, polars_df1, polars_df2])

# Using a dictionary of DataFrames
dataframes_dict = {
    'Pandas DF 1': pandas_df1,
    'Pandas DF 2': pandas_df2,
    'Polars DF 1': polars_df1,
    'Polars DF 2': polars_df2
}

data_heads(dataframes_dict)