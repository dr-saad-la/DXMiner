"""
    Functions related to explore multiple data frames simultaneously.
"""
import itertools

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


DataFrameType = Union[pd.DataFrame, pl.DataFrame]


def _validate_dataframes(df1: DataFrameType, df2: DataFrameType) -> None:
    """
    Validate if two DataFrames have the same columns and the numeric columns match.

    Parameters
    ----------
    df1 : DataFrameType
        The first DataFrame to validate.
    df2 : DataFrameType
        The second DataFrame to validate.

    Raises
    ------
    AssertionError
        If the columns of the two DataFrames do not match.
    """
    if isinstance(df1, pd.DataFrame) and isinstance(df2, pd.DataFrame):
        assert df1.columns.equals(df2.columns), "Columns do not match"
    elif isinstance(df1, pl.DataFrame) and isinstance(df2, pl.DataFrame):
        assert df1.columns == df2.columns, "Columns do not match"
    else:
        raise ValueError("Both dataframes must be of the same type (either Pandas or Polars).")


def _get_numeric_columns_only(df: DataFrameType) -> DataFrameType:
    """
    Filter numeric columns from the DataFrame.

    Parameters
    ----------
    df : DataFrameType
        The DataFrame to filter numeric columns from.

    Returns
    -------
    DataFrameType
        A DataFrame with only numeric columns.
    """
    if isinstance(df, pd.DataFrame):
        return df.select_dtypes(include=[int, float])
    elif isinstance(df, pl.DataFrame):
        # Select numeric columns in Polars (Int and Float types)
        numeric_df = df.select(pl.col(pl.Int8, pl.Int16, pl.Int32, pl.Int64, pl.Float32, pl.Float64))
        if numeric_df.width == 0:
            raise ValueError("No numeric columns found in Polars DataFrame.")
        return numeric_df


def _get_descriptive_stats(df: DataFrameType) -> DataFrameType:
    """
    Get descriptive statistics of a DataFrame, only for numeric columns.

    Parameters
    ----------
    df : DataFrameType
        The DataFrame to get descriptive statistics from.

    Returns
    -------
    DataFrameType
        The descriptive statistics of the DataFrame.
    """
    numeric_df = _get_numeric_columns_only(df)
    
    if isinstance(df, pd.DataFrame):
        return numeric_df.describe().T
    elif isinstance(df, pl.DataFrame):
        # Polars `describe()` returns statistics as string, so convert to numeric where applicable
        desc_df = numeric_df.describe()
        
        # Extract 'statistic' as a list of strings to use as headers for transpose
        header_names = desc_df['statistic'].to_list()
        
        # Drop the 'statistic' column and convert remaining columns to numeric where applicable
        numeric_stats = desc_df.drop('statistic').with_columns(
                [pl.col(stat).cast(pl.Float64) for stat in desc_df.columns[1:]])
        
        # Transpose the numeric statistics with proper headers
        return numeric_stats.transpose(column_names=header_names)


def compare_datasets(df1: DataFrameType, df2: DataFrameType) -> DataFrameType:
    """
    Compare the descriptive statistics of two datasets.

    Parameters
    ----------
    df1 : DataFrameType
        The first dataset to compare.
    df2 : DataFrameType
        The second dataset to compare.

    Returns
    -------
    DataFrameType
        The difference between the descriptive statistics of the two datasets.
    """
    # Get descriptive statistics for numeric columns only
    desc_df1 = _get_descriptive_stats(df1)
    desc_df2 = _get_descriptive_stats(df2)
    
    # Ensure the two tables have the same structure
    _validate_dataframes(desc_df1, desc_df2)
    
    # Compute the difference between the two tables
    if isinstance(df1, pd.DataFrame):
        comparison = desc_df1 - desc_df2
    elif isinstance(df1, pl.DataFrame):
        comparison = desc_df1.with_columns(
                [(desc_df1.get_column(col) - desc_df2.get_column(col)).alias(col) for col in desc_df1.columns])
    
    return comparison


def display_comparison(comparison_df: DataFrameType) -> None:
    """
    Display the comparison results.

    Parameters
    ----------
    comparison_df : DataFrameType
        The DataFrame containing the comparison results.
    """
    print("Comparison of Datasets:")
    print(comparison_df)


def compare_multiple_datasets(datasets: Union[List[DataFrameType], Dict[str, DataFrameType]]) -> None:
    """
    Compare all combinations of multiple datasets pairwise and display the results.

    Parameters
    ----------
    datasets : Union[List[pd.DataFrame, pl.DataFrame], Dict[str, pd.DataFrame, pl.DataFrame]]
        A list or dictionary of datasets to compare. If a dictionary is passed, the keys will be used as dataset names.

    Raises
    ------
    ValueError
        If the datasets parameter is neither a list nor a dictionary.

    Example Usage
    -------------
    Example with a list of pandas DataFrames:

    >>> farm_a = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
    >>> farm_b = pd.DataFrame({'A': [7, 8, 9], 'B': [10, 11, 12]})
    >>> farm_c = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
    >>> compare_multiple_datasets([farm_a, farm_b, farm_c])

    Expected Output:
    ----------------
    Comparison between dataset 1 and dataset 2:
        A   B
    mean  4.0  7.0
    std   4.0  4.0
    min   1.0  4.0
    25%   2.0  5.0
    50%   2.0  5.0
    75%   3.0  6.0
    max   7.0  12.0

    Comparison between dataset 1 and dataset 3:
        A   B
    mean  0.0  0.0
    std   0.0  0.0
    min   0.0  0.0
    25%   0.0  0.0
    50%   0.0  0.0
    75%   0.0  0.0
    max   0.0  0.0

    Comparison between dataset 2 and dataset 3:
        A   B
    mean -4.0 -7.0
    std   4.0  4.0
    min   -6.0 -6.0
    25%   -5.0 -5.0
    50%   -5.0 -5.0
    75%   -3.0 -3.0
    max   0.0  0.0

    Example with a dictionary of pandas DataFrames:

    >>> datasets = {
    >>>     'Farm A': pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]}),
    >>>     'Farm B': pd.DataFrame({'A': [7, 8, 9], 'B': [10, 11, 12]}),
    >>>     'Farm C': pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
    >>> }
    >>> compare_multiple_datasets(datasets)

    Expected Output:
    ----------------
    Comparison between Farm A and Farm B:
        A   B
    mean  4.0  7.0
    std   4.0  4.0
    min   1.0  4.0
    25%   2.0  5.0
    50%   2.0  5.0
    75%   3.0  6.0
    max   7.0  12.0

    Comparison between Farm A and Farm C:
        A   B
    mean  0.0  0.0
    std   0.0  0.0
    min   0.0  0.0
    25%   0.0  0.0
    50%   0.0  0.0
    75%   0.0  0.0
    max   0.0  0.0

    Comparison between Farm B and Farm C:
        A   B
    mean -4.0 -7.0
    std   4.0  4.0
    min   -6.0 -6.0
    25%   -5.0 -5.0
    50%   -5.0 -5.0
    75%   -3.0 -3.0
    max   0.0  0.0
    """
    
    # Handle the case where datasets is a dictionary
    if isinstance(datasets, dict):
        dataset_pairs = itertools.combinations(datasets.items(), 2)
    elif isinstance(datasets, list):
        dataset_pairs = itertools.combinations(enumerate(datasets, 1), 2)
    else:
        raise ValueError("Datasets must be a list or a dictionary.")
    
    # Compare each pair of datasets
    for (label1, df1), (label2, df2) in dataset_pairs:
        comparison_result = compare_datasets(df1, df2)
        print(f"\nComparison between {label1} and {label2}:")
        display_comparison(comparison_result)