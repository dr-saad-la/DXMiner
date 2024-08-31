"""
Information about a data frame.

Get all the necessary information about a data.
"""
import io
import pandas as pd
import polars as pl


def data_info(df, banner_text: str = "DataFrame Information"):
    """
    Display a custom-formatted summary of a DataFrame.

    This function provides a formatted overview of a given DataFrame, with additional headers and footers for clarity.
    It supports both Pandas and Polars DataFrames, ensuring that the appropriate summary information is displayed based
    on the input type. If the DataFrame is of an unsupported type, a ValueError is raised.

    The function will print the shape and a statistical summary of the DataFrame if it is a Polars DataFrame,
    or use the `info()` method if it is a Pandas DataFrame.

    Parameters
    ----------
    df : pd.DataFrame or pl.DataFrame
        The DataFrame to display information about. The DataFrame can be either a Pandas or Polars DataFrame.
    banner_text : str, optional
        The text to display in the banner (default is "DataFrame Information"). This will be centered in a
        banner displayed at the top and bottom of the information summary.

    Raises
    ------
    ValueError
        Raised if the input data is neither a Pandas DataFrame nor a Polars DataFrame.

    Notes
    -----
    - For Pandas DataFrames, this function uses `df.info()` to provide a concise summary of the DataFrame, including
      the index dtype, column dtypes, non-null values, and memory usage.
    - For Polars DataFrames, the function displays the shape of the DataFrame followed by a statistical summary
      generated by the `describe()` method, which includes count, mean, standard deviation, min, max, and percentiles.
    - The banner and footer consist of '=' characters and enclose the specified `banner_text` to visually separate
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
        A string indicating whether the data is a Pandas DataFrame, Polars DataFrame, or invalid.
    """
    if isinstance(df, pd.DataFrame):
        return "pandas"
    elif isinstance(df, pl.DataFrame):
        return "polars"
    else:
        raise ValueError(
            "The input data is neither a Pandas DataFrame nor a Polars DataFrame."
        )
