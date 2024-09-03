"""
_internal module for formatting data profile reports.

This module provides utility functions to format various sections of data profile reports
generated within the dxminer package. It includes functions for formatting missingness,
uniqueness, category reports, and more. These functions are intended for internal use
and help ensure that reports are structured, readable, and consistent across the package.

Note: This module is not intended to be part of the public API.
"""

from typing import Dict, Any, List, Union

import pandas as pd
import polars as pl
from .config import (COL_WIDTH, SEPARATOR_CHAR, FEATURE_NAME, NMISSING, PMISSING,
                     MOST_FREQUENT_CATEGORY, FREQUENCY, UNIQUE_CATEGORIES, TOTAL_COUNT,
                     UNIQUENESS_PERCENTAGE, SUGGESTION, CATEGORY_PERCENTAGE)


class TableFormatter:
    def __init__(self, headers: List[str]):
        self.headers = headers

    def format_header(self) -> str:
        """Format the header row."""
        header = " | ".join([f"{header:<{COL_WIDTH}}" for header in self.headers])
        return f"| {header} |"

    def format_separator(self) -> str:
        """Format the separator row."""
        return f"|{SEPARATOR_CHAR * (COL_WIDTH + 2)}|" + "|".join(
            ["-" * (COL_WIDTH + 2) for _ in self.headers]) + "|"

    def format_row(self, col: str, data: Dict[str, Any], field_format: str) -> List[str]:
        """Format a row with wrapped column name and data."""
        wrapped_col = self._wrap_text(col, COL_WIDTH).split('\n')
        first_row = (f"| {wrapped_col[0]:<{COL_WIDTH}} | " + field_format.format(**data) + " |")
        result = [first_row]

        # Add subsequent lines for wrapped column name if any
        for line in wrapped_col[1:]:
            result.append(f"| {line:<{COL_WIDTH}} | {'':>8} | {'':>26} |")

        return result

    @staticmethod
    def _wrap_text(text: str, width: int) -> str:
        """Wrap text to the specified width."""
        return '\n'.join([text[i:i + width] for i in range(0, len(text), width)])

    def format_report(self, data: Dict[str, Any], field_format: str) -> str:
        """Generate the full report as a string."""
        result = [self.format_header(), self.format_separator()]

        for col, col_data in data.items():
            result.extend(self.format_row(col, col_data, field_format))

        return "\n".join(result)


class MissingnessReportFormatter(TableFormatter):
    def __init__(self):
        headers = [FEATURE_NAME, NMISSING, PMISSING]
        super().__init__(headers)

    def format(self, missingness_report: Dict[str, Any]) -> str:
        field_format = "{missing_count:>8} | {missing_percentage:>26.1f}%"
        return self.format_report(missingness_report, field_format)


class UniquenessReportFormatter(TableFormatter):
    def __init__(self):
        # Headers that will be used in the formatted table
        headers = [FEATURE_NAME, TOTAL_COUNT, UNIQUENESS_PERCENTAGE, SUGGESTION]
        super().__init__(headers)

    def format(self, uniqueness_report: pd.DataFrame) -> str:
        field_format = (f"{{{TOTAL_COUNT}:>12}} | {{{UNIQUENESS_PERCENTAGE}:>10.2f}}% | "
                        f"{{{SUGGESTION}:<{COL_WIDTH}}}")
        return self.format_report(uniqueness_report.to_dict(orient="index"), field_format)


class CategoricalReportFormatter(TableFormatter):
    def __init__(self):
        headers = [FEATURE_NAME, UNIQUE_CATEGORIES, MOST_FREQUENT_CATEGORY, FREQUENCY,
                   CATEGORY_PERCENTAGE]
        super().__init__(headers)

    def format(self, category_report: pd.DataFrame) -> str:
        field_format = (f"{{{UNIQUE_CATEGORIES}:>18}} | {{{MOST_FREQUENT_CATEGORY}:<{COL_WIDTH}}} | "
                        f"{{{FREQUENCY}:>10}} | {{{CATEGORY_PERCENTAGE}:>8}}")
        return self.format_report(category_report.to_dict(orient="index"), field_format)

class DuplicateRowsReportFormatter:
    def __init__(self):
        self.headers = ["Duplicate Rows"]

    @staticmethod
    def format(duplicate_rows: Union[pd.DataFrame, pl.DataFrame], stats: Dict[str, Any]) -> str:
        """
        Format the duplicate rows report into a readable string.

        Parameters
        ----------
        duplicate_rows : Union[pd.DataFrame, pl.DataFrame]
            The DataFrame containing the duplicate rows.
        stats : Dict[str, Any]
            A dictionary containing statistics about the duplicates.

        Returns
        -------
        str
            The formatted duplicate rows report.
        """
        report = [
            f"Total duplicate rows: {stats['num_duplicates']}",
            f"Percentage of duplicate rows: {stats['duplicate_percentage']:.2f}%"
        ]

        if stats["num_duplicates"] > 0:
            report.append("\nDuplicate rows:")
            if isinstance(duplicate_rows, pd.DataFrame):
                report.append(duplicate_rows.to_string(index=False))
            else:
                report.append(str(duplicate_rows))

        return "\n".join(report)
