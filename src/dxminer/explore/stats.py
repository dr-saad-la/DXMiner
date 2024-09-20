"""Statistical reports."""

import pandas as pd
import polars as pl

from .._typing import DataFrameType


def correlation_matrix(df):
    pass


def outlier_detection_report(df):
    pass


def skewness_kurtosis_report(df):
    pass


def numerical_distributions(df):
    pass


def categorical_distributions(df):
    pass


def feature_importance(df, model):
    pass


def pairwise_scatter_plots(df, features=None):
    pass


def target_variable_analysis(df, target):
    pass


def feature_correlation_with_target(df, target):
    pass


def univariate_analysis(df, feature):
    pass


def multivariate_analysis(df, features):
    pass


def time_series_decomposition(df, date_column):
    pass


def sampling_summary(df):
    pass


def compare_means(df1: DataFrameType, df2: DataFrameType) -> DataFrameType:
    """
    Calculate the difference in column-wise means between two datasets (Pandas or Polars DataFrames).

    This function computes the difference in the means for each matching column between two
    datasets. It assumes that the columns of both DataFrames are numerical and have the same names.

    Parameters
    ----------
    df1 : DataFrameType
                                                                    The first dataset (Pandas or Polars DataFrame) to compare.
    df2 : DataFrameType
                                                                    The second dataset (Pandas or Polars DataFrame) to compare.

    Returns
    -------
    DataFrameType
                                                                    A DataFrame or Series containing the difference in means for each column.

    Raises
    ------
    ValueError
                                                                    If the input datasets have differing columns.
    TypeError
                                                                    If the input datasets are not both Pandas or Polars DataFrames.

    Examples
    --------
    Example usage with Pandas DataFrames:

    >>> df_a = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
    >>> df_b = pd.DataFrame({'A': [7, 8, 9], 'B': [10, 11, 12]})
    >>> compare_means(df_a, df_b)
    A   -6.0
    B   -6.0
    dtype: float64

    Example usage with Polars DataFrames:

    >>> df_a = pl.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
    >>> df_b = pl.DataFrame({'A': [7, 8, 9], 'B': [10, 11, 12]})
    >>> compare_means(df_a, df_b)
    shape: (1, 2)
    ┌──────┬──────┐
    │ A    │ B    │
    ├──────┼──────┤
    │ -6.0 │ -6.0 │
    └──────┴──────┘
    """

    # Ensure both DataFrames have the same columns
    if isinstance(df1, pd.DataFrame) and isinstance(df2, pd.DataFrame):
        if not df1.columns.equals(df2.columns):
            raise ValueError("The input datasets must have the same columns.")

    elif isinstance(df1, pl.DataFrame) and isinstance(df2, pl.DataFrame):
        if df1.columns != df2.columns:
            raise ValueError("The input datasets must have the same columns.")

    else:
        raise TypeError("Both inputs must be either Pandas or Polars DataFrames.")

    # Compute mean differences for Pandas DataFrames
    if isinstance(df1, pd.DataFrame):
        mean_diff = df1.mean() - df2.mean()

    # Compute mean differences for Polars DataFrames
    elif isinstance(df1, pl.DataFrame):
        df1_means = df1.select([pl.mean(col) for col in df1.columns])
        df2_means = df2.select([pl.mean(col) for col in df2.columns])
        mean_diff = df1_means - df2_means

    return mean_diff
