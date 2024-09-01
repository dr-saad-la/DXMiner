"""
Report generation of different types.

This module provides several utility function to generate
different reports from the provided data.
"""

from typing import Union, Dict, Any
import pandas as pd
import polars as pl


def report_data_profile(df: Union[pd.DataFrame, pl.DataFrame]) -> Dict[str, Any]:
    """
    Generate a comprehensive data profile report for the provided DataFrame.

    Parameters
    ----------
    df : pd.DataFrame or pl.DataFrame
        The DataFrame to profile.

    Returns
    -------
    Dict[str, Any]
        A dictionary containing various profiling information about the
        DataFrame.

    Examples
    --------
    >>> import pandas as pd
    >>> data = {'A': [1, 2, 2, None], 'B': ['x', 'y', 'x', 'z']}
    >>> df = pd.DataFrame(data)
    >>> report_data_profile(df)
    {
        "shape": (4, 2),
        "missingness_report": {
            "A": {"missing_count": 1, "missing_percentage": 25.0},
            "B": {"missing_count": 0, "missing_percentage": 0.0}
        },
        "uniqueness_report": {
            "A": {"unique_count": 3, "unique_percentage": 75.0},
            "B": {"unique_count": 3, "unique_percentage": 75.0}
        },
        "category_report": {
            "B": {"unique_categories": 3, "most_frequent_category": "x",
             "frequency": 2}
        },
        "duplicate_rows": 0,
        "duplicate_columns": []
    }
    """
    report = {}

    report["shape"] = df.shape

    # Missingness Report
    report["missingness_report"] = _generate_missingness_report(df)

    # Uniqueness Report
    report["uniqueness_report"] = _generate_uniqueness_report(df)

    # Category Report
    report["category_report"] = _generate_category_report(df)

    # Duplicate Rows Report
    report["duplicate_rows"] = _generate_duplicate_rows_report(df)

    # Duplicate Columns Report
    report["duplicate_columns"] = _generate_duplicate_columns_report(df)

    return report


def _generate_missingness_report(
    df: Union[pd.DataFrame, pl.DataFrame]
) -> Dict[str, Dict[str, float]]:
    """
    Generate a missingness report for the DataFrame.

    Parameters
    ----------
    df : pd.DataFrame or pl.DataFrame
        The DataFrame to analyze.

    Returns
    -------
    Dict[str, Dict[str, float]]
        A dictionary with missing data statistics for each column.
    """
    missingness = {}
    for col in df.columns:
        if isinstance(df, pd.DataFrame):
            missing_count = df[col].isna().sum()
            total_count = df.shape[0]
        elif isinstance(df, pl.DataFrame):
            missing_count = df[col].null_count().sum()
            total_count = df.shape[0]
        missing_percentage = (missing_count / total_count) * 100
        missingness[col] = {
            "missing_count": missing_count,
            "missing_percentage": missing_percentage,
        }
    return missingness


def _generate_uniqueness_report(
    df: Union[pd.DataFrame, pl.DataFrame]
) -> Dict[str, Dict[str, float]]:
    """
    Generate a uniqueness report for the DataFrame.

    Parameters
    ----------
    df : pd.DataFrame or pl.DataFrame
        The DataFrame to analyze.

    Returns
    -------
    Dict[str, Dict[str, float]]
        A dictionary with uniqueness statistics for each column.
    """
    uniqueness = {}
    for col in df.columns:
        if isinstance(df, pd.DataFrame):
            unique_count = df[col].nunique()
            total_count = df.shape[0]
        elif isinstance(df, pl.DataFrame):
            unique_count = df[col].n_unique()
            total_count = df.shape[0]
        unique_percentage = (unique_count / total_count) * 100
        uniqueness[col] = {
            "unique_count": unique_count,
            "unique_percentage": unique_percentage,
        }
    return uniqueness


def _generate_category_report(
    df: Union[pd.DataFrame, pl.DataFrame]
) -> Dict[str, Dict[str, Any]]:
    """
    Generate a category report for categorical columns in the DataFrame.

    Parameters
    ----------
    df : pd.DataFrame or pl.DataFrame
        The DataFrame to analyze.

    Returns
    -------
    Dict[str, Dict[str, Any]]
        A dictionary with category statistics for each categorical column.
    """
    category_report = {}
    for col in df.columns:
        if isinstance(df[col], pd.CategoricalDtype) or df[col].dtype == "object":
            value_counts = df[col].value_counts()
            most_frequent = value_counts.idxmax()
            frequency = value_counts.max()
            category_report[col] = {
                "unique_categories": len(value_counts),
                "most_frequent_category": most_frequent,
                "frequency": frequency,
            }
    return category_report


def _generate_duplicate_rows_report(df: Union[pd.DataFrame, pl.DataFrame]) -> int:
    """
    Generate a report on the number of duplicate rows in the DataFrame.

    Parameters
    ----------
    df : pd.DataFrame or pl.DataFrame
        The DataFrame to analyze.

    Returns
    -------
    int
        The number of duplicate rows in the DataFrame.
    """
    if isinstance(df, pd.DataFrame):
        return df.duplicated().sum()
    elif isinstance(df, pl.DataFrame):
        return df.is_duplicated().sum()


def _generate_duplicate_columns_report(
    df: Union[pd.DataFrame, pl.DataFrame]
) -> Dict[str, int]:
    """
    Generate a report on the duplicate columns in the DataFrame.

    Parameters
    ----------
    df : pd.DataFrame or pl.DataFrame
        The DataFrame to analyze.

    Returns
    -------
    Dict[str, int]
        A dictionary with duplicate column names and their count.
    """
    if isinstance(df, pd.DataFrame):
        col_duplicates = df.T.duplicated().sum()
    elif isinstance(df, pl.DataFrame):
        col_duplicates = df.columns[df.select(pl.all().is_duplicated()).columns]
    return col_duplicates


def report_missingness(df: Union[pd.DataFrame, pl.DataFrame]) -> None:
    """
    Generate a comprehensive report of missing data in the DataFrame.

    This function provides a summary of missing data points in each column, including:
    - Total missing values.
    - Percentage of missing values.
    - Columns sorted by missing values.
    - Suggestions based on missingness (e.g., drop, impute).

    Parameters
    ----------
    df : Union[pd.DataFrame, pl.DataFrame]
        The DataFrame to analyze.

    Returns
    -------
    None

    Example
    -------
    >>> import pandas as pd
    >>> import polars as pl
    >>> import numpy as np
    >>> from dxminer.explore import missingness_report
    >>>
    >>> # Example with Pandas DataFrame
    >>> data = {
    >>>     'A': [1, 2, np.nan, 4, 5],
    >>>     'B': [np.nan, np.nan, np.nan, 8, 9],
    >>>     'C': ['foo', 'bar', 'baz', None, 'qux']
    >>> }
    >>> df = pd.DataFrame(data)
    >>> missingness_report(df)
    >>>
    >>> # Example with Polars DataFrame
    >>> data = {
    >>>     'A': [1, 2, None, 4, 5],
    >>>     'B': [None, None, None, 8, 9],
    >>>     'C': ['foo', 'bar', 'baz', None, 'qux']
    >>> }
    >>> df_pl = pl.DataFrame(data)
    >>> missingness_report(df_pl)
    """

    if isinstance(df, pd.DataFrame):
        missing_data = df.isnull().sum()
        total_rows = len(df)
    elif isinstance(df, pl.DataFrame):
        missing_data = df.null_count().to_pandas().iloc[0]
        total_rows = df.height
    else:
        raise ValueError(
            "The input data is neither a Pandas DataFrame nor a Polars DataFrame."
        )

    missing_report = pd.DataFrame(
        {"Total Missing": missing_data, "Percentage": (missing_data / total_rows) * 100}
    )

    # Filter out columns with no missing data
    missing_report = missing_report[missing_report["Total Missing"] > 0]

    # Sort by the percentage of missing values in descending order
    missing_report = missing_report.sort_values(by="Percentage", ascending=False)

    # Add suggestions based on the percentage of missing data
    conditions = [
        (missing_report["Percentage"] == 100),
        (missing_report["Percentage"] > 50),
        (missing_report["Percentage"] > 20),
        (missing_report["Percentage"] > 5),
        (missing_report["Percentage"] > 0),
    ]
    suggestions = [
        "Consider dropping this column.",
        "High missingness, consider dropping or advanced imputation.",
        "Moderate missingness, consider imputation.",
        "Low missingness, consider simple imputation.",
        "Very low missingness, may not require action.",
    ]
    missing_report["Suggestion"] = pd.cut(
        missing_report["Percentage"],
        bins=[0, 5, 20, 50, 100],
        labels=suggestions[::-1],
        include_lowest=True,
    )

    print(missing_report.to_string(index=True))

    # Additional summary information
    total_missing = missing_report["Total Missing"].sum()
    print(f"\nTotal missing values across all columns: {total_missing}")
    print(
        f"Percentage of missing values across all data: {(total_missing / (total_rows * len(df.columns))) * 100:.2f}%"
    )


def report_uniqueness(df: Union[pd.DataFrame, pl.DataFrame]) -> None:
    """
    Generate a report of the uniqueness of data in each column of the DataFrame.

    This function provides a summary of unique values in each column, including:
    - Total unique values.
    - Percentage of unique values relative to the total number of rows.
    - Identification of columns with high or low uniqueness.

    Parameters
    ----------
    df : Union[pd.DataFrame, pl.DataFrame]
        The DataFrame to analyze.

    Returns
    -------
    None

    Example
    -------
    >>> import pandas as pd
    >>> import polars as pl
    >>> from dxminer.explore import report_uniqueness
    >>>
    >>> # Example with Pandas DataFrame
    >>> data = {
    >>>     'A': [1, 2, 3, 4, 5],
    >>>     'B': [1, 1, 1, 8, 9],
    >>>     'C': ['foo', 'foo', 'baz', 'baz', 'baz']
    >>> }
    >>> df = pd.DataFrame(data)
    >>> report_uniqueness(df)
    >>>
    >>> # Example with Polars DataFrame
    >>> data = {
    >>>     'A': [1, 2, 3, 4, 5],
    >>>     'B': [1, 1, 1, 8, 9],
    >>>     'C': ['foo', 'foo', 'baz', 'baz', 'baz']
    >>> }
    >>> df_pl = pl.DataFrame(data)
    >>> report_uniqueness(df_pl)
    """

    if isinstance(df, pd.DataFrame):
        unique_data = df.nunique()
        total_rows = len(df)
    elif isinstance(df, pl.DataFrame):
        unique_data = df.n_unique().to_pandas().iloc[0]
        total_rows = df.height
    else:
        raise ValueError(
            "The input data is neither a Pandas DataFrame nor a Polars DataFrame."
        )

    uniqueness_report = pd.DataFrame(
        {"Total Unique": unique_data, "Percentage": (unique_data / total_rows) * 100}
    )

    # Sort by the percentage of unique values in descending order
    uniqueness_report = uniqueness_report.sort_values(by="Percentage", ascending=False)

    # Suggestions based on the percentage of unique data
    conditions = [
        (uniqueness_report["Percentage"] == 100),
        (uniqueness_report["Percentage"] > 90),
        (uniqueness_report["Percentage"] > 50),
        (uniqueness_report["Percentage"] > 10),
        (uniqueness_report["Percentage"] > 0),
    ]
    suggestions = [
        "Likely an identifier or unique key.",
        "Very high uniqueness, consider as a key feature.",
        "High uniqueness, important feature.",
        "Moderate uniqueness, review as a potential feature.",
        "Low uniqueness, may have limited feature importance.",
    ]
    uniqueness_report["Suggestion"] = pd.cut(
        uniqueness_report["Percentage"],
        bins=[0, 10, 50, 90, 100],
        labels=suggestions[::-1],
        include_lowest=True,
    )

    print(uniqueness_report.to_string(index=True))

    # Additional summary information
    print(
        f"\nColumns with 100% uniqueness: {len(uniqueness_report[uniqueness_report['Percentage'] == 100])}"
    )
    print(
        f"Columns with <10% uniqueness: {len(uniqueness_report[uniqueness_report['Percentage'] < 10])}"
    )


def report_categoricals(df: Union[pd.DataFrame, pl.DataFrame]) -> None:
    """
    Generate a report on the categorical features in the DataFrame.

    This function provides a summary of all categorical columns, including:
    - Number of unique categories.
    - Most frequent category.
    - Frequency of the most frequent category.
    - Percentage of the most frequent category relative to the total number of
    rows.

    Parameters
    ----------
    df : Union[pd.DataFrame, pl.DataFrame]
        The DataFrame to analyze.

    Returns
    -------
    None

    Example
    -------
    >>> import pandas as pd
    >>> import polars as pl
    >>> from dxminer.explore import category_report
    >>>
    >>> # Example with Pandas DataFrame
    >>> data = {
    >>>     'A': ['apple', 'banana', 'apple', 'apple', 'banana'],
    >>>     'B': ['red', 'red', 'green', 'green', 'red'],
    >>>     'C': [1, 2, 3, 4, 5]  # Non-categorical
    >>> }
    >>> df = pd.DataFrame(data)
    >>> category_report(df)
    >>>
    >>> # Example with Polars DataFrame
    >>> data = {
    >>>     'A': ['apple', 'banana', 'apple', 'apple', 'banana'],
    >>>     'B': ['red', 'red', 'green', 'green', 'red'],
    >>>     'C': [1, 2, 3, 4, 5]  # Non-categorical
    >>> }
    >>> df_pl = pl.DataFrame(data)
    >>> category_report(df_pl)
    """

    if isinstance(df, pd.DataFrame):
        cat_data = df.select_dtypes(include=["category", "object"])
    elif isinstance(df, pl.DataFrame):
        cat_data = df.select(pl.col(pl.Utf8))
    else:
        raise ValueError(
            "The input data is neither a Pandas DataFrame nor a Polars"
            "DataFrame."  # noqa: E501
        )

    report = []
    total_rows = len(df) if isinstance(df, pd.DataFrame) else df.height

    for col in cat_data.columns:
        unique_vals = (
            cat_data[col].nunique()
            if isinstance(df, pd.DataFrame)
            else cat_data[col].n_unique()
        )
        most_freq_val = (
            cat_data[col].mode()[0]
            if isinstance(df, pd.DataFrame)
            else cat_data[col].mode().item()
        )
        freq_count = (
            cat_data[col].value_counts().iloc[0]
            if isinstance(df, pd.DataFrame)
            else cat_data[col].value_counts().to_pandas().iloc[0, 1]
        )
        freq_percentage = (freq_count / total_rows) * 100

        report.append(
            {
                "Column": col,
                "Unique Categories": unique_vals,
                "Most Frequent": most_freq_val,
                "Frequency": freq_count,
                "Percentage": f"{freq_percentage:.2f}%",
            }
        )

    category_report_df = pd.DataFrame(report)

    # Sort report by the number of unique categories
    category_report_df = category_report_df.sort_values(
        by="Unique Categories", ascending=False
    )

    # Print report in a format similar to `print(df)`
    print(category_report_df.to_string(index=False))

    # Additional summary information
    print(f"\nColumns analyzed: {len(category_report_df)}")
    print(
        f"Columns with only one unique category: {len(category_report_df[category_report_df['Unique Categories'] == 1])}"
    )


def report_duplicate_rows(df: Union[pd.DataFrame, pl.DataFrame]) -> None:
    """
    Generate a report on duplicate rows in the DataFrame.

    This function provides a summary of duplicate rows, including:
    - Total number of duplicate rows.
    - Percentage of duplicate rows relative to the total number of rows.
    - Display the duplicate rows (if any).

    Parameters
    ----------
    df : Union[pd.DataFrame, pl.DataFrame]
        The DataFrame to analyze.

    Returns
    -------
    None

    Example
    -------
    >>> import pandas as pd
    >>> import polars as pl
    >>> from dxminer.explore import report_duplicate_rows
    >>>
    >>> # Example with Pandas DataFrame
    >>> data = {
    >>>     'A': [1, 2, 2, 4, 5, 5],
    >>>     'B': [10, 20, 20, 40, 50, 50],
    >>>     'C': ['x', 'y', 'y', 'z', 'w', 'w']
    >>> }
    >>> df = pd.DataFrame(data)
    >>> report_duplicate_rows(df)
    >>>
    >>> # Example with Polars DataFrame
    >>> data = {
    >>>     'A': [1, 2, 2, 4, 5, 5],
    >>>     'B': [10, 20, 20, 40, 50, 50],
    >>>     'C': ['x', 'y', 'y', 'z', 'w', 'w']
    >>> }
    >>> df_pl = pl.DataFrame(data)
    >>> report_duplicate_rows(df_pl)
    """

    if isinstance(df, pd.DataFrame):
        duplicate_rows = df[df.duplicated()]
    elif isinstance(df, pl.DataFrame):
        duplicate_rows = df.filter(pl.concat_list(df.columns).duplicated())
    else:
        raise ValueError(
            "The input data is neither a Pandas DataFrame nor a Polars DataFrame."
        )

    num_duplicates = (
        len(duplicate_rows) if isinstance(df, pd.DataFrame) else duplicate_rows.height
    )
    total_rows = len(df) if isinstance(df, pd.DataFrame) else df.height
    duplicate_percentage = (num_duplicates / total_rows) * 100

    print(f"Total duplicate rows: {num_duplicates}")
    print(f"Percentage of duplicate rows: {duplicate_percentage:.2f}%\n")

    if num_duplicates > 0:
        print("Duplicate rows:")
        print(
            duplicate_rows.to_string(index=False)
            if isinstance(df, pd.DataFrame)
            else duplicate_rows
        )


def report_duplicate_cols(df: Union[pd.DataFrame, pl.DataFrame]) -> None:
    """
    Generate a report on duplicated columns and analyze the percentage of duplicate values within each column.

    This function provides a summary of duplicated columns and duplicate values, including:
    - Total number of duplicated columns.
    - List of duplicated columns.
    - Percentage of duplicate values in each column.
    - Suggestions based on the findings.

    Parameters
    ----------
    df : Union[pd.DataFrame, pl.DataFrame]
        The DataFrame to analyze.

    Returns
    -------
    None

    Example
    -------
    >>> import pandas as pd
    >>> import polars as pl
    >>> from dxminer.explore import report_duplicated_cols
    >>>
    >>> # Example with Pandas DataFrame
    >>> data = {
    >>>     'A': [1, 2, 3, 4],
    >>>     'B': [5, 6, 7, 8],
    >>>     'C': [1, 2, 3, 4],  # Duplicate of column 'A'
    >>>     'D': [5, 6, 7, 8],  # Duplicate of column 'B'
    >>>     'E': [1, 1, 1, 1]   # 100% duplicate values
    >>> }
    >>> df = pd.DataFrame(data)
    >>> report_duplicated_cols(df)
    >>>
    >>> # Example with Polars DataFrame
    >>> data = {
    >>>     'A': [1, 2, 3, 4],
    >>>     'B': [5, 6, 7, 8],
    >>>     'C': [1, 2, 3, 4],  # Duplicate of column 'A'
    >>>     'D': [5, 6, 7, 8],  # Duplicate of column 'B'
    >>>     'E': [1, 1, 1, 1]   # 100% duplicate values
    >>> }
    >>> df_pl = pl.DataFrame(data)
    >>> report_duplicated_cols(df_pl)
    """

    if isinstance(df, pd.DataFrame):
        duplicated_columns = df.columns[df.T.duplicated(keep=False)]
        total_rows = len(df)
        duplicate_value_report = df.apply(
            lambda col: col.duplicated(keep=False).sum() / total_rows * 100
        )
    elif isinstance(df, pl.DataFrame):
        duplicated_columns = [
            col
            for col in df.columns
            if df.select(col).frame_equal(
                df.select(df.columns).unique(), null_equal=True
            )
        ]
        total_rows = df.shape[0]
        duplicate_value_report = {
            col: df.select(pl.col(col).is_duplicated().sum()).item() / total_rows * 100
            for col in df.columns
        }
    else:
        raise ValueError(
            "The input data is neither a Pandas DataFrame nor a Polars DataFrame."
        )

    num_duplicated_cols = len(duplicated_columns)

    print(f"Total duplicated columns: {num_duplicated_cols}")

    if num_duplicated_cols > 0:
        print("\nDuplicated columns:")
        for col in duplicated_columns:
            print(f"- {col}")

    print("\nDuplicate Values Report:")
    for col, percent in duplicate_value_report.items():
        print(f"- Column '{col}': {percent:.2f}% duplicate values")
        if percent > 50:
            print(
                f"  Suggestion: Consider removing or further analyzing column '{col}' as it contains a high percentage of duplicate values."
            )

    print("\nSuggestions:")
    if num_duplicated_cols > 0:
        print(
            f"- Consider removing or merging the {num_duplicated_cols} duplicated columns to avoid redundancy."
        )
    for col, percent in duplicate_value_report.items():
        if percent > 50:
            print(
                f"- Column '{col}' has a high percentage of duplicate values ({percent:.2f}%). Consider removing or further analyzing this column."
            )


def missing_data_patterns(df):
    pass
