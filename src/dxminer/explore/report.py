"""
Report generation of different types.

This module provides several utility function to generate
different reports from the provided data.

TO DO:
    GENERATE REPORT FOR OTHER DATA TYPES
    SERIES, DICTIONARIES, SETS, LISTS
    PYARROW TABLES

Other Reports:
    JSON
    HTML
    Convert to PDF

"""

from typing import Any
from typing import Dict
from typing import Union

import numpy as np
import pandas as pd
import polars as pl

from .._formatter import CategoricalReportFormatter
from .._formatter import DuplicateRowsReportFormatter
from .._formatter import MissingnessReportFormatter
from .._formatter import UniquenessReportFormatter
from ..config import CATEGORY_PERCENTAGE
from ..config import FEATURE_NAME
from ..config import FREQUENCY
from ..config import MOST_FREQUENT_CATEGORY
from ..config import SUGGESTION
from ..config import TOTAL_COUNT
from ..config import TOTAL_UNIQUE
from ..config import UNIQUENESS_CONDITIONS
from ..config import UNIQUENESS_PERCENTAGE
from ..config import UNIQUENESS_SUGGESTIONS
from ..config import UNIQUE_CATEGORIES


def formatted_report_data_profile(df: Union[pd.DataFrame, pl.DataFrame]) -> str:
    """
    Generate a comprehensive data profile report for the provided DataFrame.

    This function generates a report including the shape of the DataFrame,
    a missingness report, uniqueness report, category report, and information
    about duplicate rows and columns. The report is formatted as a string.

    Parameters
    ----------
    df : pd.DataFrame or pl.DataFrame
        The DataFrame to profile.

    Returns
    -------
    str
        A formatted string containing the profiling information about the DataFrame.

    Examples
    --------
    >>> import pandas as pd
    >>> data = {
    >>>         'A': [1, 2, 2, None],
    >>>         'B': ['x', 'y', 'x', 'z']
    >>>         }
    >>> df = pd.DataFrame(data)
    >>> print(formatted_report_data_profile(df))
    """
    # Generate the report data
    report = {
        "shape"            : df.shape, "missingness_report": _generate_missingness_report(df),
        "uniqueness_report": _generate_uniqueness_report(df),
        "category_report"  : _generate_category_report(df),
        "duplicate_rows"   : _generate_duplicate_rows_report(df),
        "duplicate_columns": _generate_duplicate_columns_report(df)
        }

    # Create formatter instances
    missingness_formatter = MissingnessReportFormatter()
    uniqueness_formatter = UniquenessReportFormatter()
    category_formatter = CategoricalReportFormatter()

    # Format each section of the report
    formatted_missingness_report = missingness_formatter.format(report["missingness_report"])
    formatted_uniqueness_report = uniqueness_formatter.format(report["uniqueness_report"])
    formatted_category_report = category_formatter.format(report["category_report"])

    # Assemble the full report
    full_report = (f"Data Shape: {report['shape']}\n\n"
                   f"{formatted_missingness_report}\n\n"
                   f"{formatted_uniqueness_report}\n\n"
                   f"{formatted_category_report}\n\n"
                   f"Duplicate Rows: {report['duplicate_rows']}\n"
                   f"Duplicate Columns: {report['duplicate_columns']}\n")

    return full_report


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
    >>> data = {
    >>>         'A': [1, 2, 2, None],
    >>>         'B': ['x', 'y', 'x', 'z']
    >>>         }
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
    report = {
        "shape"            : df.shape, "missingness_report": _generate_missingness_report(df),
        "uniqueness_report": _generate_uniqueness_report(df),
        "category_report"  : _generate_category_report(df),
        "duplicate_rows"   : _generate_duplicate_rows_report(df),
        "duplicate_columns": _generate_duplicate_columns_report(df)
        }
    return report


def _generate_missingness_report(df: Union[pd.DataFrame, pl.DataFrame]) -> Dict[
    str, Dict[str, float]]:
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
    missingness: dict[str, dict[str, float | int | Any]] = {}

    for col in df.columns:
        missing_count = 0
        if isinstance(df, pd.DataFrame):
            missing_count = df[col].isna().sum()
        elif isinstance(df, pl.DataFrame):
            missing_count = df[col].null_count()

        total_count = df.shape[0]
        missing_percentage = (missing_count / total_count) * 100
        missingness[col] = {
            "missing_count": missing_count, "missing_percentage": missing_percentage,
            }

    return missingness


def _generate_uniqueness_report(df: Union[pd.DataFrame, pl.DataFrame]) -> pd.DataFrame:
    """
    Generate a uniqueness report for the DataFrame.

    Parameters
    ----------
    df : pd.DataFrame or pl.DataFrame
        The DataFrame to analyze.

    Returns
    -------
    pd.DataFrame
        A DataFrame with uniqueness statistics for each column.
    """
    report_data = []

    for col in df.columns:
        unique_count = 0
        if isinstance(df, pd.DataFrame):
            unique_count = df[col].nunique()
        elif isinstance(df, pl.DataFrame):
            unique_count = df[col].n_unique()

        total_count = df.shape[0]
        unique_percentage = (unique_count / total_count) * 100

        report_data.append({
            "Feature Name"         : col, "Total Unique": unique_count,
            "Uniqueness Percentage": unique_percentage
            })

    uniqueness_report_df = pd.DataFrame(report_data)
    return uniqueness_report_df


def _generate_category_report(df: Union[pd.DataFrame, pl.DataFrame]) -> pd.DataFrame:
    """
    Generate a category report for categorical columns in the DataFrame.

    Parameters
    ----------
    df : pd.DataFrame or pl.DataFrame
        The DataFrame to analyze.

    Returns
    -------
    pd.DataFrame
        A DataFrame with category statistics for each categorical column.
    """
    report_data = []

    for col in df.columns:
        if isinstance(df[col].dtype, pd.CategoricalDtype) or df[col].dtype == "object":
            value_counts = df[col].value_counts()
            most_frequent = value_counts.idxmax()
            frequency = value_counts.max()
            total_count = len(df)

            report_data.append({
                "Feature Name" : col, "Unique Categories": len(value_counts),
                "Most Frequent": most_frequent, "Frequency": frequency,
                "Percentage"   : f"{(frequency / total_count) * 100:.2f}%"
                })

    category_report_df = pd.DataFrame(report_data)
    return category_report_df


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


def _generate_duplicate_columns_report(df: Union[pd.DataFrame, pl.DataFrame]) -> Dict[str, int]:
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
    duplicate_columns = {}

    if isinstance(df, pd.DataFrame):
        duplicated = df.T.duplicated(keep=False)
        col_names = df.columns[duplicated]
        for col in col_names:
            duplicate_columns[col] = int(duplicated.sum())

    elif isinstance(df, pl.DataFrame):
        duplicated_columns = df.select(pl.all().is_duplicated()).to_series().to_list()
        for col, is_duplicated in zip(df.columns, duplicated_columns):
            if is_duplicated:
                if col in duplicate_columns:
                    duplicate_columns[col] += 1
                else:
                    duplicate_columns[col] = 1

    return duplicate_columns


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
    # noinspection PyShadowingNames
    Example
    -------
    >>> import pandas as pd
    >>> import polars as pl
    >>> import numpy as np
    >>> from dxminer.explore import report_missingness
    >>>
    >>> # Example with Pandas DataFrame
    >>> data = {
    >>>     'A': [1, 2, np.nan, 4, 5],
    >>>     'B': [np.nan, np.nan, np.nan, 8, 9],
    >>>     'C': ['foo', 'bar', 'baz', None, 'qux']
    >>> }
    >>> df = pd.DataFrame(data)
    >>> report_missingness(df)
    >>>
    >>> # Example with Polars DataFrame
    >>> data = {
    >>>     'A': [1, 2, None, 4, 5],
    >>>     'B': [None, None, None, 8, 9],
    >>>     'C': ['foo', 'bar', 'baz', None, 'qux']
    >>> }
    >>> df_pl = pl.DataFrame(data)
    >>> report_missingness(df_pl)
    """

    if isinstance(df, pd.DataFrame):
        missing_data = df.isnull().sum()
        total_rows = len(df)
    elif isinstance(df, pl.DataFrame):
        missing_data = df.null_count().to_pandas().iloc[0]
        total_rows = df.height
    else:
        raise ValueError("The input data is neither a Pandas DataFrame nor a Polars DataFrame.")

    missing_report = pd.DataFrame(
        {"Total Missing": missing_data, "Percentage": (missing_data / total_rows) * 100})

    # Filter out columns with no missing data
    missing_report = missing_report[missing_report["Total Missing"] > 0]

    # Sort by the percentage of missing values in descending order
    missing_report = missing_report.sort_values(by="Percentage", ascending=False)

    # Add suggestions based on the percentage of missing data
    _conditions = [(missing_report["Percentage"] == 100), (missing_report["Percentage"] > 50),
                   (missing_report["Percentage"] > 20), (missing_report["Percentage"] > 5),
                   (missing_report["Percentage"] > 0)]

    suggestions = ["Consider dropping this column.",
                   "High missingness, consider dropping or advanced imputation.",
                   "Moderate missingness, consider imputation.",
                   "Low missingness, consider simple imputation.",
                   "Very low missingness, may not require action.", ]

    missing_report["Suggestion"] = pd.cut(missing_report["Percentage"], bins=[0, 5, 20, 50, 100],
                                          labels=suggestions[::-1], include_lowest=True)

    print(missing_report.to_string(index=True))

    # Additional summary information
    total_missing = missing_report["Total Missing"].sum()
    print(f"\nTotal missing values across all columns: {total_missing}")
    print(f"Percentage of missing values across all data: "
          f"{(total_missing / (total_rows * len(df.columns))) * 100:.2f}%")


def report_uniqueness(df: Union[pd.DataFrame, pl.DataFrame]) -> str:
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
    str
        A formatted string containing the uniqueness report.

    Example
    -------
    # Example DataFrame usage
    >>> data = {
    >>>     'A': [1, 2, 3, 4, 5],
    >>>     'B': [1, 1, 1, 8, 9],
    >>>     'C': ['foo', 'foo', 'baz', 'baz', 'baz']
    >>> }
    >>> df = pd.DataFrame(data)
    >>>
    >>> # Generate and print the report
    >>> formatted_report = report_uniqueness(df)
    >>> print(formatted_report)

    Expected Output
    ---------------
    | Feature Name | Total Unique | Uniqueness Percentage | Suggestion
         |
    |--------------|--------------|-----------------------|--------------------------------------------|
    | A            |            5 |               100.00% | Likely an identifier or unique key.
         |
    | C            |            2 |                40.00% | High uniqueness, important feature.
         |
    | B            |            2 |                40.00% | High uniqueness, important feature.
         |

    Columns with 100% uniqueness: 1
    Columns with <10% uniqueness: 0
    """

    if isinstance(df, pd.DataFrame):
        unique_data = df.nunique()
        total_rows = len(df)
    elif isinstance(df, pl.DataFrame):
        unique_data = df.select(pl.all().n_unique()).to_series().to_pandas()
        total_rows = df.height
    else:
        raise ValueError("The input data is neither a Pandas DataFrame nor a Polars DataFrame.")

    uniqueness_report = pd.DataFrame({
        FEATURE_NAME         : unique_data.index, TOTAL_UNIQUE: unique_data.values,
        UNIQUENESS_PERCENTAGE: (unique_data.values / total_rows) * 100
        })

    # Sort by the percentage of unique values in descending order
    uniqueness_report = uniqueness_report.sort_values(by=UNIQUENESS_PERCENTAGE, ascending=False)

    # Apply suggestions based on the percentage of unique values
    uniqueness_report[SUGGESTION] = np.select(
        [condition(uniqueness_report[UNIQUENESS_PERCENTAGE]) for condition in
         UNIQUENESS_CONDITIONS], UNIQUENESS_SUGGESTIONS, default="No suggestion available")

    # Format the report using the UniquenessReportFormatter
    uniqueness_formatter = UniquenessReportFormatter()
    formatted_report = uniqueness_formatter.format(uniqueness_report)

    return formatted_report


def report_categoricals(df: Union[pd.DataFrame, pl.DataFrame]) -> str:
    """
    Generate a report on the categorical features in the DataFrame.

    This function provides a summary of all categorical columns, including:
    - Number of unique categories.
    - Most frequent category.
    - Frequency of the most frequent category.
    - Percentage of the most frequent category relative to the total number of rows.

    Parameters
    ----------
    df : Union[pd.DataFrame, pl.DataFrame]
        The DataFrame to analyze.

    Returns
    -------
    str
        A formatted string containing the categorical report.

    Example
    -------
    >>> import pandas as pd
    >>> import polars as pl
    >>> from dxminer.explore import report_categoricals
    >>>
    >>> # Example with Pandas DataFrame
    >>> data = {
    >>>     'A': ['apple', 'banana', 'apple', 'apple', 'banana'],
    >>>     'B': ['red', 'red', 'green', 'green', 'red'],
    >>>     'C': [1, 2, 3, 4, 5]
    >>> }
    >>> df = pd.DataFrame(data)
    >>> print(report_categoricals(df))
    >>>
    >>> # Example with Polars DataFrame
    >>> data = {
    >>>     'A': ['apple', 'banana', 'apple', 'apple', 'banana'],
    >>>     'B': ['red', 'red', 'green', 'green', 'red'],
    >>>     'C': [1, 2, 3, 4, 5]  # Non-categorical
    >>> }
    >>> df_pl = pl.DataFrame(data)
    >>> print(report_categoricals(df_pl))

    Expected Output
    ---------------
    | Feature Name | Unique Categories | Most Frequent       |  Frequency | Percentage |
    |--------------|-------------------|---------------------|------------|------------|
    | A            |                 2 | apple               |          3 |     60.00% |
    | B            |                 2 | red                 |          3 |     60.00% |

    Columns analyzed: 2
    Columns with only one unique category: 0
    """

    if isinstance(df, pd.DataFrame):
        cat_data = df.select_dtypes(include=["category", "object"])
    elif isinstance(df, pl.DataFrame):
        cat_data = df.select(pl.col(pl.Utf8))
    else:
        raise ValueError("The input data is neither a Pandas DataFrame nor a Polars DataFrame.")

    report = []
    total_rows = len(df) if isinstance(df, pd.DataFrame) else df.height

    for col in cat_data.columns:
        unique_vals = (
            cat_data[col].nunique() if isinstance(df, pd.DataFrame) else cat_data[col].n_unique())
        most_freq_val = (cat_data[col].mode()[0] if isinstance(df, pd.DataFrame) else cat_data[
            col].mode().item())
        freq_count = (cat_data[col].value_counts().iloc[0] if isinstance(df, pd.DataFrame) else
                      cat_data[col].value_counts().to_pandas().iloc[0, 1])
        freq_percentage = (freq_count / total_rows) * 100

        report.append({
            FEATURE_NAME          : col, UNIQUE_CATEGORIES: unique_vals,
            MOST_FREQUENT_CATEGORY: most_freq_val, FREQUENCY: freq_count,
            CATEGORY_PERCENTAGE   : f"{freq_percentage:.2f}%",
            })

    category_report_df = pd.DataFrame(report)

    # Sort report by the number of unique categories
    category_report_df = category_report_df.sort_values(by=UNIQUE_CATEGORIES, ascending=False)

    # Format the report using the CategoricalReportFormatter
    category_formatter = CategoricalReportFormatter()
    formatted_report = category_formatter.format(category_report_df)

    # Additional summary information
    summary = (f"\nColumns analyzed: {len(category_report_df)}\n"
               f"Columns with only one unique category: "
               f"{len(category_report_df[category_report_df[UNIQUE_CATEGORIES] == 1])}")

    return formatted_report + summary


def _detect_duplicated_columns_pandas(df: pd.DataFrame) -> pd.Index:
    """Detect duplicated columns in a Pandas DataFrame."""
    return df.columns[df.T.duplicated(keep=False)]


def _detect_duplicated_columns_polars(df: pl.DataFrame) -> list:
    """Detect duplicated columns in a Polars DataFrame."""
    duplicated_columns = []
    columns_checked = set()

    for col in df.columns:
        if col in columns_checked:
            continue

        col_series = df[col].to_list()
        for other_col in df.columns:
            if col != other_col and other_col not in columns_checked:
                other_col_series = df[other_col].to_list()
                if col_series == other_col_series:
                    duplicated_columns.append(other_col)
                    columns_checked.add(other_col)

        columns_checked.add(col)

    return duplicated_columns


def _calculate_duplicate_value_percentage_pandas(df: pd.DataFrame) -> dict:
    """Calculate the percentage of duplicate values for each column in a Pandas DataFrame."""
    total_rows = len(df)
    return df.apply(lambda col: col.duplicated(keep=False).sum() / total_rows * 100).to_dict()


def _calculate_duplicate_value_percentage_polars(df: pl.DataFrame) -> dict:
    """Calculate the percentage of duplicate values for each column in a Polars DataFrame."""
    total_rows = df.shape[0]
    return {col: df.select(pl.col(col).is_duplicated().sum()).item() / total_rows * 100 for col in
            df.columns}


def report_duplicate_cols(df: Union[pd.DataFrame, pl.DataFrame]) -> None:
    """
    Generate a report on duplicated columns and analyze the percentage of duplicate values within
    each column.

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
    """
    if isinstance(df, pd.DataFrame):
        duplicated_columns = _detect_duplicated_columns_pandas(df)
        duplicate_value_report = _calculate_duplicate_value_percentage_pandas(df)
    elif isinstance(df, pl.DataFrame):
        duplicated_columns = _detect_duplicated_columns_polars(df)
        duplicate_value_report = _calculate_duplicate_value_percentage_polars(df)
    else:
        raise ValueError("The input data is neither a Pandas DataFrame nor a Polars DataFrame.")

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
            print(f"  Suggestion: Consider removing or further analyzing column '{col}' as it "
                  f"contains a high percentage of duplicate values.")

    print("\nSuggestions:")
    if num_duplicated_cols > 0:
        print(f"- Consider removing or merging the {num_duplicated_cols} duplicated columns to "
              f"avoid redundancy.")
    for col, percent in duplicate_value_report.items():
        if percent > 50:
            print(f"- Column '{col}' has a high percentage of duplicate values ({percent:.2f}%). "
                  f"Consider removing or further analyzing this column.")


def _detect_duplicate_rows(df: Union[pd.DataFrame, pl.DataFrame]) -> Union[
    pd.DataFrame, pl.DataFrame]:
    """Detect duplicate rows in the DataFrame."""
    if isinstance(df, pd.DataFrame):
        return df[df.duplicated()]
    elif isinstance(df, pl.DataFrame):
        return df.filter(pl.concat_list(df.columns).duplicated())
    else:
        raise ValueError("The input data is neither a Pandas DataFrame nor a Polars DataFrame.")


def _calculate_duplicate_stats(df: Union[pd.DataFrame, pl.DataFrame],
                               duplicate_rows: Union[pd.DataFrame, pl.DataFrame]) -> Dict[
    str, float]:
    """Calculate the number and percentage of duplicate rows."""
    num_duplicates = len(duplicate_rows) if isinstance(df, pd.DataFrame) else duplicate_rows.height
    total_rows = len(df) if isinstance(df, pd.DataFrame) else df.height
    duplicate_percentage = (num_duplicates / total_rows) * 100
    return {"num_duplicates": num_duplicates, "duplicate_percentage": duplicate_percentage}


def _format_duplicate_rows_report(duplicate_rows: Union[pd.DataFrame, pl.DataFrame],
                                  stats: Dict[str, float]) -> str:
    """Format the duplicate rows report."""
    report = [f"Total duplicate rows: {stats['num_duplicates']}",
              f"Percentage of duplicate rows: {stats['duplicate_percentage']:.2f}%"]

    if stats["num_duplicates"] > 0:
        report.append("\nDuplicate rows:")
        if isinstance(duplicate_rows, pd.DataFrame):
            report.append(duplicate_rows.to_string(index=False))
        else:
            report.append(str(duplicate_rows))

    return "\n".join(report)


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

    # Detect duplicate rows
    duplicate_rows = _detect_duplicate_rows(df)

    # Calculate statistics
    stats = _calculate_duplicate_stats(df, duplicate_rows)

    # Format the report using DuplicateRowsReportFormatter
    formatter = DuplicateRowsReportFormatter()
    formatted_report = formatter.format(duplicate_rows, stats)

    # Print the report
    print(formatted_report)

# def missing_data_patterns(df):
#     pass
