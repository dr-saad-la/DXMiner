"""
    Functions related to explore multiple data frames simultaneously.
"""

import itertools
from typing import Dict
from typing import List
from typing import Union

import pandas as pd
import polars as pl

from .._typing import DataFrameDict
from .._typing import DataFrameList
from .._typing import DataFrameType


def _create_centered_header(title: str, length: int = 80, char: str = "=") -> str:
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
					A formatted string with the title centered and the separator character filling the rest of the
					line.

	Example
	-------
	>>> print(_create_centered_header('DataFrame A'))
	=============================== DataFrame A ===============================

	>>> print(_create_centered_header('Example', length=50, char='-'))
	-------------------- Example --------------------
	"""
	if len(title) >= length:
		return title
	
	padding = (length - len(title) - 2) // 2
	return f"{char * padding} {title} {char * padding}"


def data_heads(dataframes: Union[DataFrameList, DataFrameDict], separator_length: int = 80) -> None:
	"""
	Print the head of multiple DataFrames (Pandas or Polars) with a separator line in between.

	Parameters
	----------
	dataframes : Union[DataFrameList, DataFrameDict]
					A list or dictionary of Pandas or Polars DataFrames to display.
	separator_length : int, optional
					Length of the separator line (default is 80).

	Examples
	--------
	Using a list of DataFrames:

	>>> import pandas as pd
	>>> import polars as pl
	>>> df_a = pd.DataFrame({'Column1': [1, 2, 3], 'Column2': [4, 5, 6]})
	>>> df_b = pl.DataFrame({'Column3': [7, 8, 9], 'Column4': [10, 11, 12]})
	>>> data_heads([df_a, df_b])

	Output:
	=============================== DataFrame 1 ===============================
	   Column1  Column2
	0        1        4
	1        2        5
	2        3        6
	=============================== DataFrame 2 ===============================
	shape: (3, 2)
	┌─────────┬─────────┐
	│ Column3 │ Column4 │
	├─────────┼─────────┤
	│ 7       │ 10      │
	│ 8       │ 11      │
	│ 9       │ 12      │
	└─────────┴─────────┘

	Using a dictionary of DataFrames:

	>>> dataframes_dict = {'Dataset A': df_a, 'Dataset B': df_b}
	>>> data_heads(dataframes_dict)

	Output:
	=============================== Dataset A ===============================
	   Column1  Column2
	0        1        4
	1        2        5
	2        3        6
	=============================== Dataset B ===============================
	shape: (3, 2)
	┌─────────┬─────────┐
	│ Column3 │ Column4 │
	├─────────┼─────────┤
	│ 7       │ 10      │
	│ 8       │ 11      │
	│ 9       │ 12      │
	└─────────┴─────────┘
	"""
	if isinstance(dataframes, dict):
		for name, df in dataframes.items():
			print(_create_centered_header(name, separator_length))
			print(df.head())
		print("=" * separator_length)
	else:
		for i, df in enumerate(dataframes, start=1):
			print(_create_centered_header(f"DataFrame {i}", separator_length))
			print(df.head())
		print("=" * separator_length)


def _validate_dataframes(df1: DataFrameType, df2: DataFrameType) -> None:
	"""
	Validate whether two DataFrames (either Pandas or Polars) have matching columns and ensure both
	DataFrames are of the same type (either both Pandas or both Polars).

	This function raises an AssertionError if the columns of the two DataFrames do not match. It also ensures
	that the DataFrames being compared are both of the same type, either Pandas or Polars.

	Parameters
	----------
	df1 : DataFrameType
					The first DataFrame to validate (either Pandas or Polars).
	df2 : DataFrameType
					The second DataFrame to validate (either Pandas or Polars).

	Raises
	------
	AssertionError
					If the column names of the two DataFrames do not match.
	ValueError
					If the two DataFrames are not of the same type (either both Pandas or both Polars).

	Examples
	--------
	>>> df1 = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
	>>> df2 = pd.DataFrame({'A': [7, 8, 9], 'B': [10, 11, 12]})
	>>> _validate_dataframes(df1, df2)  # No assertion error raised, columns match

	>>> df1 = pl.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
	>>> df2 = pl.DataFrame({'A': [7, 8, 9], 'C': [10, 11, 12]})
	>>> _validate_dataframes(df1, df2)  # Raises AssertionError: Columns do not match
	"""
	if type(df1) != type(df2):
		raise ValueError("Both DataFrames must be of the same type (either Pandas or Polars).")
	
	# Validate columns for Pandas DataFrames
	if isinstance(df1, pd.DataFrame) and isinstance(df2, pd.DataFrame):
		if not df1.columns.equals(df2.columns):
			raise AssertionError("Columns do not match")
	
	# Validate columns for Polars DataFrames
	elif isinstance(df1, pl.DataFrame) and isinstance(df2, pl.DataFrame):
		if df1.columns != df2.columns:
			raise AssertionError("Columns do not match")


def _get_num_cols(df: DataFrameType) -> DataFrameType:
	"""
	Filter and return only the numeric columns from the given DataFrame (either Pandas or Polars).

	Parameters
	----------
	df : DataFrameType
					The DataFrame from which numeric columns are to be extracted. It can be either a Pandas or Polars
					DataFrame.

	Returns
	-------
	DataFrameType
					A DataFrame containing only the numeric columns.

	Raises
	------
	ValueError
					If no numeric columns are found in the DataFrame.
	TypeError
					If the input is neither a Pandas nor a Polars DataFrame.

	Example
	-------
	>>> df = pd.DataFrame({'A': [1, 2, 3], 'B': ['a', 'b', 'c'], 'C': [4.5, 5.5, 6.5]})
	>>> numeric_df = _get_num_cols(df)
	>>> print(numeric_df)
	   A    C
	0  1  4.5
	1  2  5.5
	2  3  6.5
	"""
	if isinstance(df, pd.DataFrame):
		# Select numeric columns from Pandas DataFrame (int and float)
		numeric_df = df.select_dtypes(include=[int, float])
		if numeric_df.empty:
			raise ValueError("No numeric columns found in the Pandas DataFrame.")
		return numeric_df
	
	elif isinstance(df, pl.DataFrame):
		# Select numeric columns from Polars DataFrame (Int and Float types)
		numeric_df = df.select(pl.col(pl.Int8, pl.Int16, pl.Int32, pl.Int64, pl.Float32, pl.Float64))
		if numeric_df.width == 0:
			raise ValueError("No numeric columns found in the Polars DataFrame.")
		return numeric_df
	
	else:
		raise TypeError("The input must be either a Pandas or Polars DataFrame.")


def _get_descriptive_stats(df: DataFrameType) -> DataFrameType:
	"""
	Get descriptive statistics for numeric columns in a DataFrame.

	This function handles both Pandas and Polars DataFrames and returns descriptive statistics
	only for numeric columns, transposed for better readability.

	Parameters
	----------
	df : DataFrameType
					The DataFrame to calculate descriptive statistics for. Can be either a Pandas or Polars DataFrame.

	Returns
	-------
	DataFrameType
					A DataFrame containing the transposed descriptive statistics for numeric columns in the input
					DataFrame.
					The statistics include measures like mean, std, min, max, and percentiles.

	Raises
	------
	ValueError
					If the input DataFrame is neither a Pandas nor a Polars DataFrame.
	"""
	# Helper function to extract only numeric columns
	numeric_df = _get_numeric_columns_only(df)
	
	if isinstance(df, pd.DataFrame):
		# Return transposed Pandas descriptive statistics for numeric columns
		return numeric_df.describe().T
	
	elif isinstance(df, pl.DataFrame):
		# Polars describe() includes a 'statistic' row, handle it accordingly
		desc_df = numeric_df.describe()
		
		# Extract 'statistic' as a list to use for transposing column names
		header_names = desc_df["statistic"].to_list()
		
		# Convert all numeric statistics columns (except 'statistic' column) to float
		numeric_stats = desc_df.drop("statistic").with_columns(
				[pl.col(stat).cast(pl.Float64) for stat in desc_df.columns[1:]])
		
		# Transpose the DataFrame and assign correct headers
		return numeric_stats.transpose(column_names=header_names)
	
	else:
		raise ValueError("Input must be either a Pandas or Polars DataFrame.")


def compare_datasets(df1: DataFrameType, df2: DataFrameType) -> DataFrameType:
	"""
	Compare the descriptive statistics of two datasets and return the difference.

	This function computes and compares the descriptive statistics (only for numeric columns)
	of two datasets, ensuring both datasets have the same structure and columns before comparison.

	Parameters
	----------
	df1 : DataFrameType
					The first dataset (Pandas or Polars DataFrame) to compare.
	df2 : DataFrameType
					The second dataset (Pandas or Polars DataFrame) to compare.

	Returns
	-------
	DataFrameType
					A DataFrame containing the difference between the descriptive statistics
					(e.g., mean, standard deviation, min, max) of the two datasets.

	Raises
	------
	ValueError
					If the input DataFrames are not of the same type (both Pandas or both Polars).
	AssertionError
					If the columns of the two DataFrames do not match.

	Example
	-------
	>>> df1 = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
	>>> df2 = pd.DataFrame({'A': [1, 1, 2], 'B': [3, 5, 7]})
	>>> compare_datasets(df1, df2)
					  mean  std  min  max
	A     0.33  0.2  1.0  1.0
	B     1.0   0.0  0.0  1.0
	"""
	# Get descriptive statistics for numeric columns in both DataFrames
	desc_df1 = _get_descriptive_stats(df1)
	desc_df2 = _get_descriptive_stats(df2)
	
	# Ensure both DataFrames have the same columns
	_validate_dataframes(desc_df1, desc_df2)
	
	# Compare descriptive statistics by subtracting the second DataFrame from the first
	if isinstance(df1, pd.DataFrame):
		comparison = desc_df1 - desc_df2
	elif isinstance(df1, pl.DataFrame):
		# For Polars, subtract column-wise between the two DataFrames
		comparison = desc_df1.with_columns([(desc_df1[col] - desc_df2[col]).alias(col) for col in desc_df1.columns])
	else:
		raise ValueError("Both datasets must be either Pandas or Polars DataFrames.")
	
	return comparison


def _display_comparison(comparison_df: DataFrameType) -> None:
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

	This function compares multiple datasets (Pandas or Polars DataFrames) pairwise. It outputs the
	descriptive statistics differences between the datasets. If the input is a dictionary, the keys
	will be used as labels for the datasets.

	Parameters
	----------
	datasets : Union[List[DataFrameType], Dict[str, DataFrameType]]
					A list or dictionary of datasets to compare. If a dictionary is provided, the keys will be
					used as dataset names. If a list is provided, they will be labeled generically as "Dataset 1",
					"Dataset 2", etc.

	Raises
	------
	ValueError
					If the datasets parameter is neither a list nor a dictionary.

	Example Usage
	-------------
	Example with a list of DataFrames:

	>>> df1 = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
	>>> df2 = pd.DataFrame({'A': [7, 8, 9], 'B': [10, 11, 12]})
	>>> df3 = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
	>>> compare_multiple_datasets([df1, df2, df3])

	Expected Output:
	----------------
	Comparison between Dataset 1 and Dataset 2:
	   A    B
	mean  4.0  7.0
	std   4.0  4.0
	min   1.0  4.0
	25%   2.0  5.0
	50%   2.0  5.0
	75%   3.0  6.0
	max   7.0  12.0

	Comparison between Dataset 1 and Dataset 3:
	   A    B
	mean  0.0  0.0
	std   0.0  0.0
	min   0.0  0.0
	25%   0.0  0.0
	50%   0.0  0.0
	75%   0.0  0.0
	max   0.0  0.0

	Example with a dictionary of DataFrames:

	>>> datasets = {
	>>>     'Dataset A': pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]}),
	>>>     'Dataset B': pd.DataFrame({'A': [7, 8, 9], 'B': [10, 11, 12]}),
	>>>     'Dataset C': pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
	>>> }
	>>> compare_multiple_datasets(datasets)

	Expected Output:
	----------------
	Comparison between Dataset A and Dataset B:
	   A    B
	mean  4.0  7.0
	std   4.0  4.0
	min   1.0  4.0
	25%   2.0  5.0
	50%   2.0  5.0
	75%   3.0  6.0
	max   7.0  12.0

	Comparison between Dataset A and Dataset C:
	   A    B
	mean  0.0  0.0
	std   0.0  0.0
	min   0.0  0.0
	25%   0.0  0.0
	50%   0.0  0.0
	75%   0.0  0.0
	max   0.0  0.0
	"""
	
	if isinstance(datasets, dict):
		dataset_pairs = itertools.combinations(datasets.items(), 2)
	elif isinstance(datasets, list):
		dataset_pairs = itertools.combinations(enumerate(datasets, 1), 2)
	else:
		raise ValueError("Datasets must be a list or a dictionary.")
	
	for (label1, df1), (label2, df2) in dataset_pairs:
		comparison_result = compare_datasets(df1, df2)
		print(f"\nComparison between {label1} and {label2}:")
		_display_comparison(comparison_result)
