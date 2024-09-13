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
import numpy as np
from scipy import stats

from dxminer._typing import DataFrameType

def _create_centered_header(title: str, length: int = 80, char: str = '=') -> str:
    """
    Helper function to create a centered header with a title in the middle and a specified separator character.

    Parameters
    ----------
    title : str
        The title or name to be displayed in the center of the header.
    length : int, optional
        The total length of the header line (default is 80).
    char : str, optional
        The character to use for the separator (default is '=').

    Returns
    -------
    str
        A formatted string with the title centered and the separator character filling the rest of the line.

    Example
    -------
    >>> print(_create_centered_header('DataFrame A'))
    =============================== DataFrame A ===============================
    """
    if len(title) >= length:
        return title
    
    padding = (length - len(title) - 2) // 2
    return f"{char * padding} {title} {char * padding}"


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
            print(_create_centered_header(name, separator_length))
            print(df.head())
        print("=" * separator_length)
    else:
        for i, df in enumerate(dataframes, start=1):
            print(_create_centered_header(f'DataFrame {i}', separator_length))
            print(df.head())
        print("=" * separator_length)


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
        
# =======================================================================================
#           Statistics part for multiple datasets
#           This section will be move to another module

def compare_means(df1: DataFrameType, df2: DataFrameType) -> DataFrameType:
    """
    Calculate the difference in means between two datasets.

    This function computes the difference in column-wise means between two pandas or polars DataFrames.
    The function assumes that the two DataFrames have matching column names and numerical columns.

    Parameters
    ----------
    df1 : DataFrameType
        The first dataset (pandas or polars DataFrame) to compare.
    df2 : DataFrameType
        The second dataset (pandas or polars DataFrame) to compare.

    Returns
    -------
    DataFrameType
        A DataFrame containing the differences in means for each column.

    Raises
    ------
    ValueError
        If the input datasets have differing columns.

    Example Usage
    -------------
    >>> farm_a = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
    >>> farm_b = pd.DataFrame({'A': [7, 8, 9], 'B': [10, 11, 12]})
    >>> compare_means(farm_a, farm_b)

    Expected Output:
    ----------------
    A   -6.0
    B   -6.0
    dtype: float64
    """
    
    # Ensure both DataFrames have the same columns
    if not df1.columns.equals(df2.columns):
        raise ValueError("The input datasets must have the same columns.")
    
    # Handle pandas DataFrame
    if isinstance(df1, pd.DataFrame) and isinstance(df2, pd.DataFrame):
        mean_diff = df1.mean() - df2.mean()
    
    # Handle polars DataFrame
    elif isinstance(df1, pl.DataFrame) and isinstance(df2, pl.DataFrame):
        mean_diff = df1.select([pl.mean(col) for col in df1.columns]) - df2.select(
                [pl.mean(col) for col in df2.columns])
    
    else:
        raise TypeError("Both inputs must be either pandas or polars DataFrames.")
    
    return mean_diff


def perform_ttest(df1: DataFrameType, df2: DataFrameType) -> Dict[str, Dict[str, float]]:
    """
    Perform an independent T-test to compare the means of numeric columns from two datasets (Pandas or Polars).

    The function iterates through all columns in the datasets, identifies the numeric columns,
    and computes the T-statistic and p-value for each column using the T-test.
    Non-numeric columns are ignored.

    Parameters
    ----------
    df1 : DataFrameType
        The first dataset (Pandas or Polars DataFrame) containing numeric and other types of columns.
    df2 : DataFrameType
        The second dataset (Pandas or Polars DataFrame) containing numeric and other types of columns.

    Returns
    -------
    ttest_results : dict
        A dictionary where the keys are the column names, and the values are dictionaries containing
        the T-statistic ("t_stat") and the p-value ("p_val") for each numeric column comparison.
        Example:
        {
            "column_name_1": {"t_stat": float, "p_val": float},
            "column_name_2": {"t_stat": float, "p_val": float},
            ...
        }

    Notes
    -----
    - The function only performs the T-test on numeric columns. Non-numeric columns are ignored.
    - NaN values are dropped from the columns before performing the T-test.
    - A p-value lower than a significance threshold (typically 0.05) indicates that the means of the two
      datasets for the column being tested are significantly different.

    Example
    -------
    >>> df1 = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
    >>> df2 = pd.DataFrame({'A': [7, 8, 9], 'B': [10, 11, 12]})
    >>> ttest_results = perform_ttest(df1, df2)
    >>> for col, result in ttest_results.items():
    >>>     print(f"Column: {col}, T-statistic: {result['t_stat']}, P-value: {result['p_val']}")

    Expected Output:
    ----------------
    Column: A, T-statistic: -6.928, P-value: 0.002
    Column: B, T-statistic: -6.928, P-value: 0.002
    """
    ttest_results = {}
    
    # Determine if we're working with Pandas or Polars DataFrames
    if isinstance(df1, pd.DataFrame) and isinstance(df2, pd.DataFrame):
        # Iterate through columns in the Pandas DataFrame
        for col in df1.columns:
            if np.issubdtype(df1[col].dtype, np.number) and np.issubdtype(df2[col].dtype, np.number):
                # Perform T-test on non-NaN values of the column
                t_stat, p_val = stats.ttest_ind(df1[col].dropna(), df2[col].dropna())
                # Store the results in the dictionary
                ttest_results[col] = {"t_stat": t_stat, "p_val": p_val}
    
    elif isinstance(df1, pl.DataFrame) and isinstance(df2, pl.DataFrame):
        # Iterate through columns in the Polars DataFrame
        for col in df1.columns:
            if df1[col].dtype in [pl.Float32, pl.Float64, pl.Int32, pl.Int64] and df2[col].dtype in [pl.Float32,
                                                                                                     pl.Float64,
                                                                                                     pl.Int32,
                                                                                                     pl.Int64]:
                # Perform T-test on non-NaN values of the column (Polars to Pandas conversion for T-test)
                t_stat, p_val = stats.ttest_ind(df1[col].drop_nulls().to_pandas(), df2[col].drop_nulls().to_pandas())
                # Store the results in the dictionary
                ttest_results[col] = {"t_stat": t_stat, "p_val": p_val}
    
    else:
        raise TypeError("Both inputs must be either Pandas or Polars DataFrames.")
    
    return ttest_results

# The ttest function
def filter_significant_results(ttest_results: Dict[str, Dict[str, float]], p_value_threshold: float = 0.05) -> Dict[str, Dict[str, float]]:
    """
    Filter the T-test results to return only significant results based on the p-value.

    Parameters
    ----------
    ttest_results : dict
        A dictionary where keys are column names, and values are dicts containing 't_stat' and 'p_val'.
    p_value_threshold : float, optional
        The threshold for significance, default is 0.05.

    Returns
    -------
    dict
        A dictionary containing only the significant features where p-value < p_value_threshold.
    """
    significant_results = {
        col: stats for col, stats in ttest_results.items() if stats['p_val'] < p_value_threshold
    }
    return significant_results


def compare_multiple_datasets_significant(datasets: Union[List[pd.DataFrame], List[pl.DataFrame]],
                                          p_value_threshold: float = 0.05) -> Dict[str, Dict[str, Dict[str, float]]]:
    """
    Perform pairwise T-test comparisons between multiple datasets and return only significant features.

    Parameters
    ----------
    datasets : list
        A list of pandas or polars DataFrames to compare.
    p_value_threshold : float, optional
        The p-value threshold for significance (default is 0.05).

    Returns
    -------
    dict
        A dictionary of significant results for each pair of datasets.
        The format is { 'dataset_i_vs_dataset_j': { 'feature': { 't_stat': float, 'p_val': float }, ... } }
    """
    significant_results = {}
    
    # Perform pairwise comparisons
    for i in range(len(datasets) - 1):
        for j in range(i + 1, len(datasets)):
            df1 = datasets[i]
            df2 = datasets[j]
            
            # Perform the T-test for the current pair of datasets
            ttest_results = perform_ttest(df1, df2)
            
            # Filter only significant results
            significant = filter_significant_results(ttest_results, p_value_threshold)
            
            # Store the significant results for the current dataset pair
            if significant:
                significant_results[f'dataset_{i + 1}_vs_dataset_{j + 1}'] = significant
    
    return significant_results