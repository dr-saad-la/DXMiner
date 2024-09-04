"""
_internal module for formatting data profile reports.

This module provides utility functions to format various sections of data profile reports
generated within the dxminer package. It includes functions for formatting missingness,
uniqueness, category reports, and more. These functions are intended for internal use
and help ensure that reports are structured, readable, and consistent across the package.

Note: This module is not intended to be part of the public API.
"""

from typing import Any
from typing import Dict
from typing import List
from typing import Union

import pandas as pd
import polars as pl
from .config import BOTTOM_JOIN_CHAR
from .config import BOTTOM_LEFT_CHAR
from .config import BOTTOM_RIGHT_CHAR
from .config import CATEGORY_PERCENTAGE
from .config import COL_WIDTH
from .config import FEATURE_NAME
from .config import FREQUENCY
from .config import INNER_SEP_CHAR
from .config import MAX_COL_WIDTH
from .config import MOST_FREQUENT_CATEGORY
from .config import NMISSING
from .config import PMISSING
from .config import SUGGESTION
from .config import TOP_JOIN_CHAR
from .config import TOP_LEFT_CHAR
from .config import TOP_RIGHT_CHAR
from .config import TOTAL_COUNT
from .config import TOTAL_UNIQUE
from .config import UNIQUENESS_PERCENTAGE
from .config import UNIQUENESS_SUGGESTIONS
from .config import UNIQUE_CATEGORIES
from .config import HEADER_SEP_CHAR
from .config import OUTER_SIDE_CHAR
from .config import INNER_VERTICAL_CHAR
from .config import STYLES


class TableFormatter:
    """
    Internal class for formatting tabular data for display with custom separators.

    This class is used to generate formatted tables with customizable separators, handling
    text wrapping and alignment based on column width. It supports different configurations
    for the top, bottom, and inner separators, as well as the option to adjust column widths
    dynamically.

    Parameters
    ----------
    headers : List[str]
        The table headers.
    report_data : List[List[str]]
        The data to be formatted in the table.
    col_width : int, optional
        The default width for each column, by default 25.
    max_col_width : int, optional
        The maximum width allowed for columns, by default 32.
    inner_sep_char : str, optional
        The character used for inner separators between rows, by default '-'.
    header_sep_char : str, optional
        The character used for the header separator, by default '-'.
    outer_side_char : str, optional
        The character used for the outer side of the table, by default '|'.
    inner_vertical_char : str, optional
        The character used for vertical separators between columns, by default ':'.
    top_rule : bool, optional
        Whether to show the top rule (separator) for the table, by default True.
    inner_horizontal : bool, optional
        Whether to show horizontal rules between rows, by default False.
    outer_sides : bool, optional
        Whether to include outer side characters, by default True.
    inner_verticals : bool, optional
        Whether to include inner vertical separators, by default True.

    Note
    ----
    This class is intended for internal use only and is not part of the public API.
    """
    def __init__(self, headers: List[str], report_data: List[List[str]], col_width: int=
    COL_WIDTH, max_col_width: int = MAX_COL_WIDTH, header_sep_char: str = HEADER_SEP_CHAR,
                 inner_sep_char: str = INNER_SEP_CHAR, outer_side_char: str = OUTER_SIDE_CHAR,
                 inner_vertical_char: str = INNER_VERTICAL_CHAR, top_rule: bool = True,
                 inner_horizontal: bool = False, outer_sides: bool = True, inner_verticals: bool=
        True):
        self.headers = headers
        self.report_data = report_data  # Data to be displayed in the table
        self.col_widths = [col_width] * len(headers)  # Default width for all columns
        self.max_col_width = max_col_width
        self.inner_sep_char = self._validate_char(inner_sep_char)
        self.header_sep_char = self._validate_char(header_sep_char)
        self.outer_side_char = self._validate_char(outer_side_char)  # Outer side characters
        self.inner_vertical_char = self._validate_char(
            inner_vertical_char)  # Inner vertical characters
        self.top_rule = top_rule  # Whether to show the top rule
        self.inner_horizontal = inner_horizontal  # Whether to show horizontal rules between rows
        self.outer_sides = outer_sides  # Whether to include outer side characters
        self.inner_verticals = inner_verticals  # Whether to include inner vertical separators
        self.top_left_char = self._validate_char(TOP_LEFT_CHAR)
        self.top_right_char = self._validate_char(TOP_RIGHT_CHAR)
        self.bottom_left_char = self._validate_char(BOTTOM_LEFT_CHAR)
        self.bottom_right_char = self._validate_char(BOTTOM_RIGHT_CHAR)
        self.top_join_char = self._validate_char(TOP_JOIN_CHAR)
        self.bottom_join_char = self._validate_char(BOTTOM_JOIN_CHAR)
        self.adjust_special_col_widths()  # Adjust column widths for first and last columns

    def _validate_char(self, char: str) -> str:
        """Validate that the character is not empty, replace with a single space if it is."""
        return char if char != "" else " "

    def adjust_special_col_widths(self):
        """Adjust the column width for each column based on the length of the headers and the data."""
        for i, header in enumerate(self.headers):
            max_length = len(header)  # Start with header length
            # Compare to the length of the data in each row for this column
            for row in self.report_data:
                max_length = max(max_length, len(str(row[i])))
            # Set the column width, but limit it to the max_col_width
            self.col_widths[i] = min(max_length, self.max_col_width)

    def _wrap_text(self, text: str, width: int) -> List[str]:
        """Wrap text to fit within the specified column width, avoiding word splits."""
        if text == "":  # Convert empty strings to a single space to maintain alignment
            text = " "
        words = text.split(' ')
        lines = []
        current_line = []

        for word in words:
            # Check if adding this word would exceed the width
            if sum(len(w) for w in current_line) + len(current_line) + len(word) <= width:
                current_line.append(word)
            else:
                # Add current line to the result and start a new line
                lines.append(' '.join(current_line))
                current_line = [word]

        # Add the last line
        if current_line:
            lines.append(' '.join(current_line))

        return lines

    def format_custom_top_rule(self) -> str:
        """Format the top rule with custom characters (e.g., ┌───┬───┐)."""
        separator_parts = [f"{'─' * (self.col_widths[i] + 2)}" for i in range(len(self.col_widths))]
        return f"{self.top_left_char}{self.top_join_char.join(separator_parts)}{self.top_right_char}"

    def format_custom_bottom_rule(self) -> str:
        """Format the bottom rule with custom characters (e.g., └───┴───┘)."""
        separator_parts = [f"{'─' * (self.col_widths[i] + 2)}" for i in range(len(self.col_widths))]
        return f"{self.bottom_left_char}{self.bottom_join_char.join(separator_parts)}{self.bottom_right_char}"

    def format_header(self) -> str:
        """Format the header row."""
        header_parts = [f"{header:<{self.col_widths[i]}}" for i, header in enumerate(self.headers)]
        # Use side characters based on `outer_sides` and `inner_verticals`
        if self.inner_verticals:
            header = f" {self.inner_vertical_char} ".join(header_parts)
        else:
            header = " ".join(header_parts)

        if self.outer_sides:
            return f"{self.outer_side_char} {header} {self.outer_side_char}"
        return f" {header} "

    def format_separator(self, separator_char: str, is_inner: bool = False) -> str:
        """Format a separator row dynamically adjusting the width."""
        separator_parts = [f"{separator_char * (self.col_widths[i] + 2)}" for i in
                           range(len(self.col_widths))]
        if is_inner:
            return f"{self.inner_vertical_char}{self.inner_vertical_char.join(separator_parts)}{self.inner_vertical_char}"
        if self.outer_sides:
            return f"{self.outer_side_char}{separator_char.join(separator_parts)}{self.outer_side_char}"
        return f"{separator_char.join(separator_parts)}"

    def format_row(self, row_data: List[str]) -> str:
        """Format a single row of data, accounting for wrapped text."""
        # Wrap each cell's text and collect the wrapped lines for each column
        wrapped_columns = [self._wrap_text(str(row_data[i]), self.col_widths[i]) for i in
            range(len(row_data))]

        # Determine the maximum number of lines in any column (for multi-line rows)
        max_lines = max(len(wrapped) for wrapped in wrapped_columns)

        # Prepare rows line by line
        result = []
        for line_idx in range(max_lines):
            row_parts = []
            for i, wrapped_lines in enumerate(wrapped_columns):
                # If this column has fewer lines, pad with empty spaces
                if line_idx < len(wrapped_lines):
                    row_parts.append(f"{wrapped_lines[line_idx]:<{self.col_widths[i]}}")
                else:
                    row_parts.append(f"{'':<{self.col_widths[i]}}")
            if self.inner_verticals:
                row = f" {self.inner_vertical_char} ".join(row_parts)
            else:
                row = " ".join(row_parts)
            if self.outer_sides:
                result.append(f"{self.outer_side_char} {row} {self.outer_side_char}")
            else:
                result.append(f" {row} ")

        return "\n".join(result)

    def format_table(self) -> str:
        """Format the entire table, including the header, separators, and report data."""
        result = []

        # Top rule
        result.append(self.format_custom_top_rule())

        # Header
        result.append(self.format_header())

        # Header separator
        result.append(self.format_separator(self.header_sep_char))

        # Rows and inner separators (only add inner separators **between** rows)
        for idx, row_data in enumerate(self.report_data):
            result.append(self.format_row(row_data))
            if self.inner_horizontal and idx < len(
                self.report_data) - 1:  # No separator after last row
                result.append(self.format_separator(self.inner_sep_char, is_inner=True))

        # Bottom separator (only once, after the last row)
        result.append(self.format_custom_bottom_rule())

        return "\n".join(result)

class ConfigurableTableFormatter(TableFormatter):
    """
    A configurable table formatter that uses predefined styles from the configuration.

    This class extends the `TableFormatter` and allows the user to format tables
    using different styles defined in the `config.py` file.

    Parameters
    ----------
    style_name : str
        The name of the style to apply (e.g., 'DEFAULT', 'STARS', 'SPSS', etc.).
    headers : List[str]
        The table headers.
    report_data : List[List[str]]
        The data to be formatted in the table.

    Styles
    ------
    The following styles are available:

    1. **DEFAULT Style**:
    ┌─────────────────────────┬─────────────┬─────────────────┐
    | Feature Name            | Total Unique| Uniqueness %     |
    ├─────────────────────────┼─────────────┼─────────────────┤
    | Example Feature         | 10          | 50.00%          |
    └─────────────────────────┴─────────────┴─────────────────┘

    2. **STARS Style**:
    *─────────────────────────*─────────────*─────────────────*
    * Feature Name            * Total Unique* Uniqueness %     *
    *─────────────────────────*─────────────*─────────────────*
    * Example Feature         * 10          * 50.00%          *
    *─────────────────────────*─────────────*─────────────────*

    3. **SPSS Style**:
    ───────────────────────────┬─────────────┬──────────────────
    Feature Name               │ Total Unique│ Uniqueness %
    ───────────────────────────┼─────────────┼──────────────────
    Example Feature            │ 10          │ 50.00%
    ───────────────────────────┴─────────────┴──────────────────

    4. **SAS Style**:
    +---------------------------+--------------+--------------+
    | Feature Name              | Total Unique | Uniqueness % |
    |----------------------------------------------------------
    | Example Feature           | 5            | 50.00%       |
    +---------------------------+--------------+--------------+

    5. **STATS Style**:
    = Feature Name              = Total Unique = Uniqueness %
    = Example Feature           = 10           = 50.00%

    6. **BOLD_LINES Style**:
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┓
    ┃ Feature Name            ┃ Total Unique┃ Uniqueness %     ┃
    ┣━━━━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━┫
    ┃ Example Feature         ┃ 10          ┃ 50.00%           ┃
    ┗━━━━━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━┛

    7. **DASHED_LINES Style**:
    - Feature Name             - Total Unique - Uniqueness %
    - Example Feature          - 10           - 50.00%

    8. **DOUBLE_LINES Style**:
    ╔═════════════════════════╦═════════════╦══════════════════╗
    ║ Feature Name            ║ Total Unique║ Uniqueness %     ║
    ╠═════════════════════════╬═════════════╬══════════════════╣
    ║ Example Feature         ║ 10          ║ 50.00%           ║
    ╚═════════════════════════╩═════════════╩══════════════════╝

    9. **THIN_LINES Style**:
    ┌─────────────────────────┬─────────────┬─────────────────┐
    │ Feature Name            │ Total Unique│ Uniqueness %     │
    ├─────────────────────────┼─────────────┼─────────────────┤
    │ Example Feature         │ 10          │ 50.00%          │
    └─────────────────────────┴─────────────┴─────────────────┘

    10. **SLANTED_LINES Style**:
    / Feature Name              / Total Unique / Uniqueness %
    / Example Feature           / 10           / 50.00%

    11. **BLOCK_STYLE**:
    █ Feature Name             █ Total Unique █ Uniqueness %
    █ Example Feature          █ 10           █ 50.00%

    Example
    -------
    >>> headers = ["Feature Name", "Total Unique", "Uniqueness %", "Suggestion"]
    >>> data = [
    >>>     ["A very long feature name", "5", "100.00%", "Key identifier"],
    >>>     ["Another long feature name", "2", "40.00%", "Important feature"]
    >>> ]
    >>> formatter = ConfigurableTableFormatter(style_name="STARS", headers=headers, report_data=data)
    >>> print(formatter.format_table())
    """

    def __init__(self, style_name: str, headers: List[str], report_data: List[List[str]]):
        # Load the style configuration based on the provided style name
        style = STYLES.get(style_name.upper(), STYLES["DEFAULT"])

        # Initialize the base class with the appropriate style settings
        super().__init__(
            headers=headers,
            report_data=report_data,
            col_width=style.get("COL_WIDTH", 25),
            max_col_width=style.get("MAX_COL_WIDTH", 32),
            header_sep_char=style.get("HEADER_SEP_CHAR", "─"),
            inner_sep_char=style.get("INNER_SEP_CHAR", "─"),
            outer_side_char=style.get("OUTER_SIDE_CHAR", "|"),
            inner_vertical_char=style.get("INNER_VERTICAL_CHAR", "|"),
            top_rule=True,
            inner_horizontal=False,
            outer_sides=True,
            inner_verticals=True
        )

        # Set custom corner and join characters from the style
        self.top_left_char = style.get("TOP_LEFT_CHAR", "┌")
        self.top_right_char = style.get("TOP_RIGHT_CHAR", "┐")
        self.bottom_left_char = style.get("BOTTOM_LEFT_CHAR", "└")
        self.bottom_right_char = style.get("BOTTOM_RIGHT_CHAR", "┘")
        self.top_join_char = style.get("TOP_JOIN_CHAR", "┬")
        self.bottom_join_char = style.get("BOTTOM_JOIN_CHAR", "┴")
        self.header_sep_char = style.get("HEADER_SEP_CHAR", "─")
        self.bottom_sep_char = style.get("BOTTOM_SEP_CHAR", "─")

    def format_custom_top_rule(self) -> str:
        """Format the top rule using custom characters from the style."""
        separator_parts = [f"{self.header_sep_char * (self.col_widths[i] + 2)}" for i in range(len(self.col_widths))]
        return f"{self.top_left_char}{self.top_join_char.join(separator_parts)}{self.top_right_char}"

    def format_custom_bottom_rule(self) -> str:
        """Format the bottom rule using custom characters from the style."""
        separator_parts = [f"{self.inner_sep_char * (self.col_widths[i] + 2)}" for i in range(len(self.col_widths))]
        return f"{self.bottom_left_char}{self.bottom_join_char.join(separator_parts)}{self.bottom_right_char}"

    def format_separator(self, separator_char: str, is_inner: bool = False) -> str:
        """Format a separator row dynamically adjusting the width, ensuring consistent characters."""
        separator_parts = [f"{separator_char * (self.col_widths[i] + 2)}" for i in range(len(self.col_widths))]
        if is_inner:
            return f"{self.inner_vertical_char}{self.inner_vertical_char.join(separator_parts)}{self.inner_vertical_char}"
        if self.outer_sides:
            return f"{self.outer_side_char}{separator_char.join(separator_parts)}{self.outer_side_char}"
        return f"{separator_char.join(separator_parts)}"

    def format_table(self) -> str:
        """Generate the formatted table using the selected style."""
        result = []

        # Top rule
        result.append(self.format_custom_top_rule())

        # Header
        result.append(self.format_header())

        # Header separator (uses the header_sep_char)
        result.append(self.format_separator(self.header_sep_char))

        # Rows and inner separators (only add inner separators **between** rows)
        for idx, row_data in enumerate(self.report_data):
            result.append(self.format_row(row_data))
            if self.inner_horizontal and idx < len(self.report_data) - 1:  # No separator after last row
                result.append(self.format_separator(self.inner_sep_char, is_inner=True))

        # Bottom separator (uses the bottom_sep_char)
        result.append(self.format_custom_bottom_rule())

        return "\n".join(result)

class UniquenessReportFormatter(TableFormatter):
    def __init__(self):
        # Headers that will be used in the formatted table
        headers = [FEATURE_NAME, TOTAL_UNIQUE, UNIQUENESS_PERCENTAGE, SUGGESTION]
        super().__init__(headers)

    @staticmethod
    def determine_suggestion(uniqueness_percentage: float) -> str:
        """Determine the suggestion based on the uniqueness percentage."""
        if uniqueness_percentage == 100:
            return UNIQUENESS_SUGGESTIONS[0]
        elif uniqueness_percentage > 90:
            return UNIQUENESS_SUGGESTIONS[1]
        elif uniqueness_percentage > 50:
            return UNIQUENESS_SUGGESTIONS[2]
        elif uniqueness_percentage > 10:
            return UNIQUENESS_SUGGESTIONS[3]
        else:
            return UNIQUENESS_SUGGESTIONS[4]

    def format_row(self, col: str, data: Dict[str, Any], field_format: str) -> List[str]:
        """Format a row with wrapped column name and data, including the suggestion."""
        # Determine the suggestion based on the uniqueness percentage
        data[SUGGESTION] = self.determine_suggestion(data[UNIQUENESS_PERCENTAGE])
        return super().format_row(col, data, field_format)

    def format(self, uniqueness_report: pd.DataFrame) -> str:
        field_format = (f"{{{TOTAL_UNIQUE}:>12}} | {{{UNIQUENESS_PERCENTAGE}:>10.2f}}% | "
                        f"{{{SUGGESTION}:<{COL_WIDTH}}}")
        return self.format_report(uniqueness_report.to_dict(orient="index"), field_format)


class MissingnessReportFormatter(TableFormatter):
    def __init__(self):
        headers = [FEATURE_NAME, NMISSING, PMISSING]
        super().__init__(headers)

    def format(self, missingness_report: Dict[str, Any]) -> str:
        field_format = "{missing_count:>8} | {missing_percentage:>26.1f}%"
        return self.format_report(missingness_report, field_format)


class CategoricalReportFormatter(TableFormatter):
    def __init__(self):
        headers = [FEATURE_NAME, UNIQUE_CATEGORIES, MOST_FREQUENT_CATEGORY, FREQUENCY,
                   CATEGORY_PERCENTAGE]
        super().__init__(headers)

    def format(self, category_report: pd.DataFrame) -> str:
        field_format = (
            f"{{{UNIQUE_CATEGORIES}:>18}} | {{{MOST_FREQUENT_CATEGORY}:<{COL_WIDTH}}} | "
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
        report = [f"Total duplicate rows: {stats['num_duplicates']}",
                  f"Percentage of duplicate rows: {stats['duplicate_percentage']:.2f}%"]

        if stats["num_duplicates"] > 0:
            report.append("\nDuplicate rows:")
            if isinstance(duplicate_rows, pd.DataFrame):
                report.append(duplicate_rows.to_string(index=False))
            else:
                report.append(str(duplicate_rows))

        return "\n".join(report)

