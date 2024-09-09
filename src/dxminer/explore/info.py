"""
Information about a data frame.

Get all the necessary information about a data.
"""
import io
from typing import Callable
from typing import List
from typing import Optional
from typing import Union
from typing import Dict

import pandas as pd
import polars as pl


def data_info(df, banner_text: str = "DataFrame Information"):
    """
    Display a custom-formatted summary of a DataFrame.

    This function provides a formatted overview of a given DataFrame, with
    additional headers and footers for clarity.
    It supports both Pandas and Polars DataFrames, ensuring that the
    appropriatesummary information is displayed based
    on the input type. If the DataFrame is of an unsupported type, a
    ValueError is raised.

    The function will print the shape and a statistical summary of the
    DataFrame if it is a Polars DataFrame, or use the `info()` method if it is
    a Pandas DataFrame.

    Parameters
    ----------
    df : pd.DataFrame or pl.DataFrame
        The DataFrame to display information about. The DataFrame can be either
        a Pandas or Polars DataFrame.
    banner_text : str, optional
        The text to display in the banner (default is "DataFrame Information").
        This will be centered in a banner displayed at the top and bottom of
        the information summary.

    Raises
    ------
    ValueError
        Raised if the input data is neither a Pandas DataFrame nor a Polars
        DataFrame.

    Notes
    -----
    - For Pandas DataFrames, this function uses `df.info()` to provide a
    concise summary of the DataFrame, including
      the index dtype, column dtypes, non-null values, and memory usage.
    - For Polars DataFrames, the function displays the shape of the DataFrame
     followed by a statistical summary
      gene rated by the `describe()` method, which includes count, mean,
      standard deviation, min, max, and percentiles.
    - The banner and footer consist of '=' characters and enclose the
    specified `banner_text` to visually separate
      the DataFrame information from other content.

    Examples
    --------
    Display information about a Pandas DataFrame:

    >>> import pandas as pd
    >>> df = pd.DataFrame({
    >>>     'A': [1, 2, 3],
    >>>     'B': [4, 5, 6],
    >>>     'C': ['a', 'b', 'c']
    >>> })
    >>> data_info(df, banner_text="Pandas DataFrame Info")

    Display information about a Polars DataFrame:

    >>> import polars as pl
    >>> df = pl.DataFrame({
    >>>     'A': [1, 2, 3],
    >>>     'B': [4, 5, 6],
    >>>     'C': ['a', 'b', 'c']
    >>> })
    >>> data_info(df, banner_text="Polars DataFrame Info")
    """
    # Check the DataFrame type
    df_type = _check_dtype(df)

    banner_length = len(banner_text) + 4
    banner = f"\n{'=' * banner_length}\n= {banner_text} =\n{'=' * banner_length}\n"  # noqa: E501
    footer = "=" * banner_length

    # Print banner
    print(banner)

    if df_type == "pandas":
        buffer = io.StringIO()
        df.info(buf=buffer)
        print(buffer.getvalue())
    elif df_type == "polars":
        print(f"shape: {df.shape}")
        print(df.describe())

    # Print footer
    print(f"\n{footer}")


def _check_dtype(df):
    """
    Check whether the input data is a Pandas or Polars DataFrame.

    Parameters
    ----------
    df : Any
        The input data to check.

    Returns
    -------
    str
        A string indicating whether the data is a Pandas DataFrame, Polars
        DataFrame, or invalid.
    """
    if isinstance(df, pd.DataFrame):
        return "pandas"
    if isinstance(df, pl.DataFrame):
        return "polars"
    raise ValueError("The input data is neither a Pandas DataFrame nor a Polars DataFrame.")


def head_tail(df: Union[pd.DataFrame, pl.DataFrame], n: int = 5, sort: bool = False,
    cols: Optional[Union[str, List[str]]] = None, sort_ascending: Union[bool, List[bool]] = True,
    filter_funcs: Optional[
        List[Callable[[Union[pd.DataFrame, pl.DataFrame]], Union[pd.DataFrame, pl.DataFrame]]]] = None,
    select_cols: Optional[Union[str, List[str]]] = None, handle_na: Optional[str] = None,  # Options: 'drop', 'fill'
    fill_value: Optional[Union[int, float, str]] = None, display_width: Optional[int] = None, verbose: bool = True,
    save_output: Optional[str] = None,  # Path to save the output
    ) -> None:
    """
    Display the first and last `n` rows of the DataFrame with optional sorting, filtering, NaN handling, and more.


    Parameters
    ----------
    df : pd.DataFrame or pl.DataFrame
        The DataFrame to display.
    n : int, optional
        Number of rows to display from the start and end of the DataFrame.
        Default is 5.
    sort : bool, optional
        Whether to sort the DataFrame before displaying. Default is False.
    cols : str or list of str, optional
        The column(s) to sort by if sorting is enabled. If not provided and
        `sort` is True, raises ValueError.
    sort_ascending : bool or list of bool, optional
        Sort order for each column in `cols`. If a single bool, applies to all
        `cols`. If a list, each entry corresponds to each column. Default is
        True.
    filter_funcs : list of callable, optional
        A list of functions to filter the DataFrame before displaying. Each
        function should take a DataFrame as input and return a filtered
        DataFrame.
    select_cols: str or list of str, optional
        Column(s) to display. If not provided, all columns are displayed.
    handle_na: str, optional
        How to handle NaN values. Options are 'drop' to remove NaNs or 'fill'
        to fill NaNs with a specified value. Default is None.
    fill_value: int, float, or str, optional
        The value to fill NaN with if `handle_na` is 'fill'. Default is None.
    display_width: int, optional
        The maximum number of columns to display. If not provided, all columns
        are displayed.
    verbose : bool, optional
        If True, prints the head and tail of the DataFrame. If False,
        suppresses output. Default is True.
    save_output : str, optional
        Path to save the output as a CSV or Excel file. Default is None.

    Raises
    ------
    ValueError
        If `sort` is True and `cols` is not provided.

    Returns
    -------
    None

    Example
    -------
    >>> import pandas as pd
    >>> df = pd.DataFrame({
    >>>     'A': [1, 2, None, 4, 5],
    >>>     'B': [10, 20, 30, 40, 50],
    >>>     'C': ['a', 'b', 'c', 'd', 'e']
    >>> })
    >>>
    >>> def filter_func(df):
    >>>     return df[df['A'] > 2]
    >>>
    >>> head_tail(
    >>>     df,
    >>>     n=2,
    >>>     sort=True,
    >>>     cols='B',
    >>>     sort_ascending=False,
    >>>     filter_funcs=[filter_func],
    >>>     select_cols=['A', 'B'],
    >>>     handle_na='fill',
    >>>     fill_value=0,
    >>>     display_width=2,
    >>>     save_output='output.csv',
    >>>     verbose=True
    >>> )
    """
    if handle_na == "drop":
        df = df.dropna()
    elif handle_na == "fill" and fill_value is not None:
        df = df.fillna(fill_value)

    if sort:
        if not cols:
            raise ValueError("`cols` must be provided when `sort` is True.")
        df = (df.sort(by=cols, reverse=not sort_ascending) if isinstance(df, pl.DataFrame) else df.sort_values(by=cols,
                                                                                                               ascending=sort_ascending))

    if filter_funcs:
        for func in filter_funcs:
            df = func(df)

    if select_cols:
        df = df[select_cols] if isinstance(df, pl.DataFrame) else df.loc[:, select_cols]

    if display_width is not None:
        pd.set_option("display.max_columns", display_width)

    if verbose:
        print("\nHead of the DataFrame:")
        print(df.head(n))

        print("\nTail of the DataFrame:")
        print(df.tail(n))

    if save_output:
        if isinstance(df, pd.DataFrame):
            df.to_csv(save_output, index=False)
        elif isinstance(df, pl.DataFrame):
            df.write_csv(save_output)

    if display_width is not None:
        pd.reset_option("display.max_columns")


def ntop(df: Union[pd.DataFrame, pl.DataFrame], n: int = 5, cols: Optional[Union[str, List[str]]] = None,
    ascending: bool = False, display_width: Optional[int] = None, verbose: bool = True,
    save_output: Optional[str] = None, ) -> None:
    """
    Display the top `n` rows of the DataFrame, sorted by the specified columns in descending order by default.

    Parameters
    ----------
    df : pd.DataFrame or pl.DataFrame
        The DataFrame to display.
    n : int, optional
        Number of rows to display. Default is 5.
    cols : str or list of str, optional
        The column(s) to sort by. If not provided, raises ValueError.
    ascending : bool, optional
        If True, sort in ascending order (default is False, which means descending order).
    display_width : int, optional
        The maximum number of columns to display. If not provided, all columns are displayed.
    verbose : bool, optional
        If True, prints the top `n` rows of the DataFrame. If False, suppresses output. Default is True.
    save_output : str, optional
        Path to save the output as a CSV or Excel file. Default is None.

    Raises
    ------
    ValueError
        If `cols` is not provided.

    Returns
    -------
    None

    Example
    -------
    >>> import pandas as pd
    >>> df = pd.DataFrame({
    >>>     'A': [1, 2, 3, 4, 5],
    >>>     'B': [10, 20, 30, 40, 50],
    >>>     'C': ['a', 'b', 'c', 'd', 'e']
    >>> })
    >>>
    >>> ntop(df, n=3, cols='B', ascending=False)
    Showing top 3 highest rows based on B
    >>>
    >>> ntop(df, n=3, cols='B', ascending=True)
    Showing top 3 lowest rows based on B
    """
    if not cols:
        raise ValueError("`cols` must be provided for sorting.")

    sort_order = "lowest" if ascending else "highest"

    if verbose:
        print(f"Showing top {n} {sort_order} rows based on {cols}")

    if isinstance(df, pd.DataFrame):
        df_sorted = df.sort_values(by=cols, ascending=ascending)
    elif isinstance(df, pl.DataFrame):
        df_sorted = df.sort(by=cols, reverse=not ascending)

    if display_width is not None:
        pd.set_option("display.max_columns", display_width)

    if verbose:
        print(df_sorted.head(n))

    if save_output:
        if isinstance(df_sorted, pd.DataFrame):
            df_sorted.head(n).to_csv(save_output, index=False)
        elif isinstance(df_sorted, pl.DataFrame):
            df_sorted.head(n).write_csv(save_output)

    if display_width is not None:
        pd.reset_option("display.max_columns")


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

def data_summary(df):
    pass


def memory_optimization_suggestions(df):
    pass


# def describe_percentiles(df, percentiles=[0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99]):
#    pass


def duplicate_rows_report(df):
    pass


def time_series_summary(df):
    pass


def missing_data_heatmap(df):
    pass


def value_counts_summary(df):
    pass


def data_profile_report(df):
    pass


def interactions_report(df, features=None):
    pass


def text_data_summary(df, text_column):
    pass

def transformation_suggestions(df): #noqu:
    pass
