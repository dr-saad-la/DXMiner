"""
Utility function to visualize multiple dataframe and multiple features
"""
from typing import List

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def _plot_kde(data: pd.DataFrame, label: str, col: str, ax: plt.Axes) -> None:
	"""Helper function to plot a KDE."""
	sns.kdeplot(data[col], label=label, fill=True, ax=ax)


def _plot_histogram(data: pd.DataFrame, label: str, col: str, ax: plt.Axes) -> None:
	"""Helper function to plot a histogram."""
	sns.histplot(data[col], label=label, ax=ax, kde=True)


def _plot_boxplot(data: pd.DataFrame, col: str, ax: plt.Axes, orientation: str) -> None:
	"""Helper function to plot a boxplot with hue for color."""
	if orientation == 'vertical':
		sns.boxplot(x='Dataset', y=col, data=data, ax=ax, hue='Dataset')
	else:
		sns.boxplot(x=col, y='Dataset', data=data, ax=ax, orient='h', hue='Dataset')


def _plot_violin(data: pd.DataFrame, col: str, ax: plt.Axes, orientation: str) -> None:
	"""Helper function to plot a violin plot with hue for color."""
	if orientation == 'vertical':
		sns.violinplot(x='Dataset', y=col, data=data, ax=ax, hue='Dataset')
	else:
		sns.violinplot(x=col, y='Dataset', data=data, ax=ax, orient='h', hue='Dataset')


def _plot_swarm(data: pd.DataFrame, col: str, ax: plt.Axes, orientation: str) -> None:
	"""Helper function to plot a swarm plot with hue for color."""
	if orientation == 'vertical':
		sns.swarmplot(x='Dataset', y=col, data=data, ax=ax, hue='Dataset')
	else:
		sns.swarmplot(x=col, y='Dataset', data=data, ax=ax, orient='h', hue='Dataset')


def _plot_ecdf(data: pd.DataFrame, label: str, col: str, ax: plt.Axes) -> None:
	"""Helper function to plot an ECDF."""
	sns.ecdfplot(data[col], label=label, ax=ax)


def plot_distribution_comparison(datasets: List[pd.DataFrame], dataset_labels: List[str], plot_type: str = 'kde',
                                 cols_per_row: int = 4, orientation: str = 'vertical') -> None:
	"""
	Compare the distribution of columns from multiple datasets using various plot types.

	Parameters
	----------
	datasets : List[pd.DataFrame]
		A list of datasets to compare.
	dataset_labels : List[str]
		A list of labels corresponding to each dataset (must match the number of datasets).
	plot_type : str, optional
		The type of plot to use for comparison. Supported options: 'kde', 'hist', 'boxplot', 'violin', 'swarm', 'ecdf'.
		Default is 'kde'.
	cols_per_row : int, optional
		Number of columns per row in the subplot grid. Default is 4.
	orientation : str, optional
		The orientation of the plot ('vertical' or 'horizontal'). Applies to boxplot, violin, and swarm plots.
		Default is 'vertical'.

	Raises
	------
	AssertionError
		If the number of datasets and dataset labels are not equal.

	Example Usage
	-------------
	datasets = [farm_a, farm_b, farm_c]
	dataset_labels = ['Farm A', 'Farm B', 'Farm C']

	# KDE Plot
	plot_distribution_comparison(datasets, dataset_labels, plot_type='kde')

	# Boxplot with vertical orientation
	plot_distribution_comparison(datasets, dataset_labels, plot_type='boxplot', orientation='vertical')

	# Boxplot with horizontal orientation
	plot_distribution_comparison(datasets, dataset_labels, plot_type='boxplot', orientation='horizontal')
	"""
	assert len(datasets) == len(dataset_labels), "Number of datasets and labels must be the same."
	
	# Get the numeric columns from the first dataset (assuming all datasets have the same columns)
	numeric_cols = datasets[0].select_dtypes(include=np.number).columns
	num_features = len(numeric_cols)
	
	num_rows = int(np.ceil(num_features / cols_per_row))
	
	fig, axes = plt.subplots(num_rows, cols_per_row, figsize=(cols_per_row * 5, num_rows * 5))
	axes = axes.flatten()
	
	plot_function = {
			'kde'  : _plot_kde, 'hist': _plot_histogram, 'boxplot': _plot_boxplot, 'violin': _plot_violin,
			'swarm': _plot_swarm, 'ecdf': _plot_ecdf
			}.get(plot_type)
	
	if not plot_function:
		raise ValueError(f"Unsupported plot type '{plot_type}'. Supported types are:"
		                 f" 'kde', 'hist', 'boxplot', 'violin', 'swarm', 'ecdf'.")
	
	# Plot each numeric column
	for i, col in enumerate(numeric_cols):
		if plot_type in ['boxplot', 'violin', 'swarm']:
			# Prepare data for plotting
			combined_data = pd.concat([dataset[col] for dataset in datasets], axis=1)
			combined_data.columns = dataset_labels
			
			# Melt the data to a long format for sns.boxplot, violin, or swarm
			melted_data = pd.melt(combined_data, var_name='Dataset', value_name=col)
			
			# Plot with orientation option and hue to differentiate colors by 'Dataset'
			plot_function(melted_data, col, axes[i], orientation)
			axes[i].set_title(f"{plot_type.capitalize()} of {col} by Dataset")
		else:
			# For KDE, hist, ecdf
			for dataset, label in zip(datasets, dataset_labels):
				plot_function(dataset, label, col, axes[i])
			axes[i].set_title(f"Distribution of {col}")
			axes[i].legend()
	
	for j in range(i + 1, len(axes)):
		fig.delaxes(axes[j])
	
	plt.tight_layout()
	plt.show()
