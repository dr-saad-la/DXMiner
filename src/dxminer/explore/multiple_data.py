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


def generate_statistics(*datasets) -> dict:
    """
    Generate descriptive statistics for multiple datasets.

    Parameters:
    -----------
    *datasets : pd.DataFrame
        One or more pandas DataFrames. Each dataset provided as a positional argument will have
        its descriptive statistics computed.

    Returns:
    --------
    dict
        A dictionary where the keys are dataset labels (e.g., 'farm_a', 'farm_b', etc.) and the
        values are the transposed descriptive statistics of each corresponding dataset.

    Example Usage:
    --------------
    >>> farm_a = pd.DataFrame(...)
    >>> farm_b = pd.DataFrame(...)
    >>> stats = generate_statistics(farm_a, farm_b)

    The resulting dictionary will contain descriptive statistics for both `farm_a` and `farm_b`:
    {
        "farm_a": descriptive statistics of farm_a DataFrame,
        "farm_b": descriptive statistics of farm_b DataFrame
    }

    Notes:
    ------
    - The function uses `pd.DataFrame.describe()` to compute the statistics and transposes
      the result to make the columns as rows.
    - Dataset labels are automatically assigned as 'farm_a', 'farm_b', etc., based on the order
      of the arguments provided.
    """
    stats_dict = {}
    for i, dataset in enumerate(datasets, start=1):
        stats_dict[f"farm_{chr(96 + i)}"] = dataset.describe().T
    return stats_dict


def validate_dataframes(df1: pd.DataFrame, df2: pd.DataFrame) -> None:
    """
    Validate if two DataFrames have the same index and columns.

    Parameters
    ----------
    df1 : pd.DataFrame
        The first DataFrame to validate.
    df2 : pd.DataFrame
        The second DataFrame to validate.

    Raises
    ------
    AssertionError
        If the indices or columns of the two DataFrames do not match.
    """
    assert df1.index.equals(df2.index), "Indices do not match"
    assert df1.columns.equals(df2.columns), "Columns do not match"


def compare_datasets(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
    """
    Compare the descriptive statistics of two datasets.

    Parameters
    ----------
    df1 : pd.DataFrame
        The first dataset to compare.
    df2 : pd.DataFrame
        The second dataset to compare.

    Returns
    -------
    pd.DataFrame
        The difference between the descriptive statistics of the two datasets.
    """
    # Get descriptive statistics
    desc_df1 = df1.describe().T
    desc_df2 = df2.describe().T

    # Ensure the two tables have the same index and columns
    validate_dataframes(desc_df1, desc_df2)

    # Compute the difference between the two tables
    comparison = desc_df1 - desc_df2

    return comparison


def display_comparison(comparison_df: pd.DataFrame) -> None:
    """
    Display the comparison results.

    Parameters
    ----------
    comparison_df : pd.DataFrame
        The DataFrame containing the comparison results.
    """
    print("Comparison of Datasets:")
    print(comparison_df)


def compare_multiple_datasets(datasets: list) -> None:
    """
    Compare multiple datasets pairwise and display the results.

    Parameters
    ----------
    datasets : list
        A list of datasets to compare.
    """
    for i in range(len(datasets) - 1):
        df1 = datasets[i]
        df2 = datasets[i + 1]
        comparison_result = compare_datasets(df1, df2)
        print(f"\nComparison between dataset {i + 1} and dataset {i + 2}:")
        display_comparison(comparison_result)
