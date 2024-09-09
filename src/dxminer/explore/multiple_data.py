"""
    Functions related to explore multiple data frames simultaneously.
"""

from typing import List
from typing import Dict
from typing import Optional
from typing import Union

import pandas as pd
import polars as pl

def _separator_line(name: str, length: int = 80) -> str:
    """
    Helper function to create a separator line with the DataFrame name centered.

    Parameters
    ----------
    name : str
        The name to be displayed in the center of the separator.
    length : int, optional
        The total length of the separator line (default is 80).

    Returns
    -------
    str
        A formatted string with the name centered in the separator line.
    """
    return f"{'=' * ((length - len(name)) // 2)} {name} {'=' * ((length - len(name)) // 2)}"


def data_heads(dataframes: Union[List[Union[pd.DataFrame, pl.DataFrame]], Dict[str, Union[pd.DataFrame, pl.DataFrame]]],
               separator_length: int = 80) -> None:
    """
    Print the head of multiple DataFrames (Pandas or Polars) with a separator line in between.

    Parameters
    ----------
    dataframes : Union[List[Union[pd.DataFrame, pl.DataFrame]], Dict[str, Union[pd.DataFrame, pl.DataFrame]]]
        A list or dictionary of Pandas or Polars DataFrames to display.
    separator_length : int, optional
        Length of the separator line (default is 80).

    Examples
    --------
    Using a list of DataFrames:

    >>> import pandas as pd
    >>> import polars as pl
    >>> farm_a = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
    >>> farm_b = pl.DataFrame({'C': [7, 8, 9], 'D': [10, 11, 12]})
    >>> data_heads([farm_a, farm_b])

    Output:
    =============================== DataFrame 1 ===============================
       A  B
    0  1  4
    1  2  5
    2  3  6
    =============================== DataFrame 2 ===============================
    shape: (3, 2)
    ┌─────┬─────┐
    │ C   │ D   │
    ├─────┼─────┤
    │ 7   │ 10  │
    │ 8   │ 11  │
    │ 9   │ 12  │
    └─────┴─────┘

    Using a dictionary of DataFrames:

    >>> dataframes_dict = {'Farm A': farm_a, 'Farm B': farm_b}
    >>> data_heads(dataframes_dict)

    Output:
    =============================== Farm A ===============================
       A  B
    0  1  4
    1  2  5
    2  3  6
    =============================== Farm B ===============================
    shape: (3, 2)
    ┌─────┬─────┐
    │ C   │ D   │
    ├─────┼─────┤
    │ 7   │ 10  │
    │ 8   │ 11  │
    │ 9   │ 12  │
    └─────┴─────┘
    """
    if isinstance(dataframes, dict):
        for name, df in dataframes.items():
            print(_separator_line(name, separator_length))
            print(df.head())
        print("=" * separator_length)
    else:
        for i, df in enumerate(dataframes, start=1):
            print(_separator_line(f'DataFrame {i}', separator_length))
            print(df.head())
        print("=" * separator_length)
