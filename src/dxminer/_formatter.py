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
from typing import Optional
from typing import Union

import pandas as pd
import polars as pl

from .config import BOTTOM_JOIN_CHAR
from .config import BOTTOM_LEFT_CHAR
from .config import BOTTOM_RIGHT_CHAR
from .config import CATEGORY_PERCENTAGE
from .config import COL_WIDTH
from .config import DUPLICATE_COUNT
from .config import DUPLICATE_PERCENTAGE
from .config import DUPLICATE_ROWS
from .config import FEATURE_NAME
from .config import FIRST_OCCURRENCE
from .config import FREQUENCY
from .config import HEADER_SEP_CHAR
from .config import INNER_SEP_CHAR
from .config import INNER_VERTICAL_CHAR
from .config import LAST_OCCURRENCE
from .config import MAX_COL_WIDTH
from .config import MOST_FREQUENT_CATEGORY
from .config import OUTER_SIDE_CHAR
from .config import STYLES
from .config import SUGGESTION
from .config import TOP_JOIN_CHAR
from .config import TOP_LEFT_CHAR
from .config import TOP_RIGHT_CHAR
from .config import TOTAL_DUPLICATES
from .config import TOTAL_UNIQUE
from .config import UNIQUENESS_PERCENTAGE
from .config import UNIQUENESS_SUGGESTIONS
from .config import UNIQUE_CATEGORIES


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

    def __init__(self, headers: List[str], report_data: List[List[str]], col_width: int = COL_WIDTH,
                 max_col_width: int = MAX_COL_WIDTH, header_sep_char: str = HEADER_SEP_CHAR,
                 inner_sep_char: str = INNER_SEP_CHAR, outer_side_char: str = OUTER_SIDE_CHAR,
                 inner_vertical_char: str = INNER_VERTICAL_CHAR, top_rule: bool = True, inner_horizontal: bool = False,
                 outer_sides: bool = True, inner_verticals: bool = True):
        self.headers = headers
        self.report_data = report_data                                         # Data to be displayed in the table
        self.col_widths = [col_width] * len(headers)                           # Default width for all columns
        self.max_col_width = max_col_width
        self.inner_sep_char = self._validate_char(inner_sep_char)
        self.header_sep_char = self._validate_char(header_sep_char)
        self.outer_side_char = self._validate_char(outer_side_char)            # Outer side characters
        self.inner_vertical_char = self._validate_char(inner_vertical_char)    # Inner vertical characters
        self.top_rule = top_rule                                               # Whether to show the top rule
        self.inner_horizontal = inner_horizontal                               # Whether to show horizontal rules
        # between rows
        self.outer_sides = outer_sides                                         # Whether to include outer side
        # characters
        self.inner_verticals = inner_verticals                                 # Whether to include inner vertical
        # separators
        self.top_left_char = self._validate_char(TOP_LEFT_CHAR)
        self.top_right_char = self._validate_char(TOP_RIGHT_CHAR)
        self.bottom_left_char = self._validate_char(BOTTOM_LEFT_CHAR)
        self.bottom_right_char = self._validate_char(BOTTOM_RIGHT_CHAR)
        self.top_join_char = self._validate_char(TOP_JOIN_CHAR)
        self.bottom_join_char = self._validate_char(BOTTOM_JOIN_CHAR)
        self.adjust_special_col_widths()                                       # Adjust column widths for first and
        # last columns

    def _validate_char(self, char: str) -> str:
        """Validate that the character is not empty, replace with a single space if it is."""
        return char if char != "" else " "

    def adjust_special_col_widths(self):
        """Adjust the column width for each column based on the length of the headers and the
        data."""
        for i, header in enumerate(self.headers):
            max_length = len(header)
            for row in self.report_data:
                max_length = max(max_length, len(str(row[i])))
            self.col_widths[i] = min(max_length, self.max_col_width)

    @staticmethod
    def _wrap_text(text: str, width: int) -> List[str]:
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

        if current_line:
            lines.append(' '.join(current_line))

        return lines

    def format_custom_top_rule(self) -> str:
        """Format the top rule with custom characters (e.g., ┌───┬───┐)."""
        separator_parts = [f"{'─' * (self.col_widths[i] + 2)}" for i in range(len(self.col_widths))]
        return (f"{self.top_left_char}{self.top_join_char.join(separator_parts)}"
                f"{self.top_right_char}")

    def format_custom_bottom_rule(self) -> str:
        """Format the bottom rule with custom characters (e.g., └───┴───┘)."""
        separator_parts = [f"{'─' * (self.col_widths[i] + 2)}" for i in range(len(self.col_widths))]
        return (f"{self.bottom_left_char}{self.bottom_join_char.join(separator_parts)}"
                f"{self.bottom_right_char}")

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
        separator_parts = [f"{separator_char * (self.col_widths[i] + 2)}" for i in range(len(self.col_widths))]
        if is_inner:
            return (f"{self.inner_vertical_char}{self.inner_vertical_char.join(separator_parts)}"
                    f"{self.inner_vertical_char}")
        if self.outer_sides:
            return (f"{self.outer_side_char}{separator_char.join(separator_parts)}"
                    F"{self.outer_side_char}")
        return f"{separator_char.join(separator_parts)}"

    def format_row(self, row_data: List[str]) -> str:
        """Format a single row of data, accounting for wrapped text."""
        # Wrap each cell's text and collect the wrapped lines for each column
        wrapped_columns = [self._wrap_text(str(row_data[i]), self.col_widths[i]) for i in range(len(row_data))]

        max_lines = max(len(wrapped) for wrapped in wrapped_columns)

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
        result = [
            self.format_custom_top_rule(),
            self.format_header(),
            self.format_separator(self.header_sep_char)
            ]

        # Rows and inner separators (only add inner separators **between** rows)
        for idx, row_data in enumerate(self.report_data):
            result.append(self.format_row(row_data))
            if self.inner_horizontal and idx < len(self.report_data) - 1:  # No separator after last row
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
    >>> formatter = ConfigurableTableFormatter(style_name="STARS", headers=headers,
    report_data=data)
    >>> print(formatter.format_table())
    """

    def __init__(self, style_name: str, headers: List[str], report_data: List[List[str]]):
        # Load the style configuration based on the provided style name
        self.style_name = style_name
        style = STYLES.get(style_name.upper(), STYLES["DEFAULT"])

        # Initialize the base class with the appropriate style settings
        super().__init__(headers=headers, report_data=report_data, col_width=style.get("COL_WIDTH", 25),
                         max_col_width=style.get("MAX_COL_WIDTH", 32),
                         header_sep_char=style.get("HEADER_SEP_CHAR", "─"),
                         inner_sep_char=style.get("INNER_SEP_CHAR", "─"),
                         outer_side_char=self._validate_char(style.get("OUTER_SIDE_CHAR", "|")),
                         inner_vertical_char=style.get("INNER_VERTICAL_CHAR", "|"), top_rule=True,
                         inner_horizontal=False, outer_sides=True, inner_verticals=True)

        # Set custom corner and join characters from the style
        self.top_left_char = style.get("TOP_LEFT_CHAR", "┌")
        self.top_right_char = style.get("TOP_RIGHT_CHAR", "┐")
        self.bottom_left_char = style.get("BOTTOM_LEFT_CHAR", "└")
        self.bottom_right_char = style.get("BOTTOM_RIGHT_CHAR", "┘")
        self.top_join_char = style.get("TOP_JOIN_CHAR", "┬")
        self.bottom_join_char = style.get("BOTTOM_JOIN_CHAR", "┴")
        self.header_sep_char = style.get("HEADER_SEP_CHAR", "─")
        self.bottom_sep_char = style.get("BOTTOM_SEP_CHAR", "─")

    def _validate_char(self, char: str) -> str:
        """
        Override to keep empty strings for OUTER_SIDE_CHAR in the STATS style
        without replacing them with spaces.
        """
        # If the style is "STATS" and the character is empty, return it as-is
        if self.style_name.upper() == "STATS" and char == "":
            return ""
        return char if char != "" else " "

    def format_custom_top_rule(self) -> str:
        """Format the top rule using custom characters from the style."""
        separator_parts = [f"{self.header_sep_char * (self.col_widths[i] + 2)}" for i in range(len(self.col_widths))]
        return (f"{self.top_left_char}{self.top_join_char.join(separator_parts)}"
                f"{self.top_right_char}")

    def format_custom_bottom_rule(self) -> str:
        """Format the bottom rule using custom characters from the style."""
        separator_parts = [f"{self.inner_sep_char * (self.col_widths[i] + 2)}" for i in range(len(self.col_widths))]
        return (f"{self.bottom_left_char}{self.bottom_join_char.join(separator_parts)}"
                f"{self.bottom_right_char}")

    def format_separator(self, separator_char: str, is_inner: bool = False) -> str:
        """
        Format a separator row dynamically adjusting the width, ensuring consistent characters.
        Fill any empty spaces at the ends with the separator character.
        """
        # Adjust total width based on the style
        if self.style_name.upper() == "STATS":
            total_width = sum(self.col_widths) + len(self.col_widths) * 3 + 1
        else:
            total_width = sum(self.col_widths) + len(self.col_widths) * 3 - 1

        separator_line = separator_char * total_width

        if is_inner and not self.outer_sides:  # If there's no outer side chars, return separator directly
            return separator_line
        if self.outer_sides:
            return f"{self.outer_side_char}{separator_line}{self.outer_side_char}"
        return separator_line

    def format_table(self) -> str:
        """Generate the formatted table using the selected style."""
        result = [self.format_custom_top_rule(), self.format_header(), self.format_separator(self.header_sep_char)]

        # Rows and inner separators (only add inner separators **between** rows)
        for idx, row_data in enumerate(self.report_data):
            result.append(self.format_row(row_data))
            if self.inner_horizontal and idx < len(self.report_data) - 1:  # No separator after last row
                result.append(self.format_separator(self.inner_sep_char, is_inner=True))

        # Bottom separator (uses the bottom_sep_char)
        result.append(self.format_custom_bottom_rule())

        return "\n".join(result)


class ConfigurableSplitTableFormatter(ConfigurableTableFormatter):
    """
    A configurable table formatter that splits the table horizontally and dynamically adjusts the columns
    to fit the entire page width, with a max width of 120 characters. If the next column does not fit,
    it will be moved to the next line entirely, ensuring no extra empty columns are added.

    This class extends the `TableFormatter` and allows splitting tables when they exceed the given width.

    Parameters
    ----------
    style_name : str
        The name of the style to apply (e.g., 'DEFAULT', 'STARS', 'SPSS', etc.).
    headers : List[str]
        The table headers.
    report_data : List[List[str]]
        The data to be formatted in the table.
    max_total_width : int, optional
        The maximum allowed width for the table (default is 120 characters).

    Example
    -------
    1. Default Style
    ┌───────────────────────────┬──────────────┬──────────────┬───────────────────┬─────────────────────┐
    | Feature Name              | Total Unique | Uniqueness % | Suggestion        | Additional Column 1 |
    |───────────────────────────────────────────────────────────────────────────────────────────────────|
    | A very long feature name  | 5            | 100.00%      | Key identifier     | Extra Data 1        |
    | Another long feature name | 2            | 40.00%       | Important feature | More Data           |
    | Short name                | 1            | 50.00%       | Moderate          | Short Data          |
    └───────────────────────────┴──────────────┴──────────────┴───────────────────┴─────────────────────┘
    ┌─────────────────────┐
    | Additional Column 2 |
    |─────────────────────|
    | Extra Data 2        |
    | More Data           |
    | Short Data          |
    └─────────────────────┘
    2. Thin lines Style
    ┌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┬╌╌╌╌╌╌╌╌╌╌╌╌╌╌┬╌╌╌╌╌╌╌╌╌╌╌╌╌╌┬╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┬╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┐
    │ Feature Name              │ Total Unique │ Uniqueness % │ Suggestion        │ Additional Column 1 │
    │╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌│
    │ A very long feature name  │ 5            │ 100.00%      │ Key identifier     │ Extra Data 1        │
    │ Another long feature name │ 2            │ 40.00%       │ Important feature │ More Data           │
    │ Short name                │ 1            │ 50.00%       │ Moderate          │ Short Data          │
    └╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┴╌╌╌╌╌╌╌╌╌╌╌╌╌╌┴╌╌╌╌╌╌╌╌╌╌╌╌╌╌┴╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┴╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┘
    ┌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┐
    │ Additional Column 2 │
    │╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌│
    │ Extra Data 2        │
    │ More Data           │
    │ Short Data          │
    └╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┘
    """

    def __init__(self, style_name: str, headers: List[str], report_data: List[List[str]], max_total_width: int = 120):
        # Store the style_name
        self.style_name = style_name

        # Initialize from ConfigurableTableFormatter
        super().__init__(style_name, headers, report_data)
        self.max_total_width = max_total_width

    def split_columns(self) -> List[List[int]]:
        """
        Split the headers and data into chunks based on the max_total_width.

        Returns
        -------
        List[List[int]]
            A list of sub-lists, each representing a chunk of column indices.
        """
        current_width = 0
        current_chunk = []
        table_chunks = []

        for i, header in enumerate(self.headers):
            col_width = self.col_widths[i] + 3  # Add padding for separators
            if current_width + col_width <= self.max_total_width:
                current_chunk.append(i)
                current_width += col_width
            else:
                # If the current column exceeds the max width, move the chunk to the table_chunks
                table_chunks.append(current_chunk)
                current_chunk = [i]  # Start the new chunk
                current_width = col_width

        if current_chunk:
            table_chunks.append(current_chunk)

        return table_chunks

    def format_chunk(self, chunk: List[int]) -> str:
        """
        Format a chunk of columns.

        Parameters
        ----------
        chunk : List[int]
            The list of column indices for the current chunk.

        Returns
        -------
        str
            The formatted table chunk.
        """
        chunk_headers = [self.headers[i] for i in chunk]
        chunk_data = [[row[i] for i in chunk] for row in self.report_data]

        # Use the same style for the chunk
        chunk_formatter = ConfigurableTableFormatter(self.style_name, chunk_headers, chunk_data)

        # Return the formatted chunk using the same style
        return chunk_formatter.format_table()

    def format_split_table(self) -> str:
        """
        Format the entire table, splitting columns based on the max total width.

        Returns
        -------
        str
            The formatted table with splits applied.
        """
        result = []
        chunks = self.split_columns()

        for chunk in chunks:
            # Format each chunk of headers and data
            result.append(self.format_chunk(chunk))

        return "\n".join(result)

    def format_table(self) -> str:
        """Override the format_table method to apply the splitting logic."""
        return self.format_split_table()


class UniquenessReportFormatter(ConfigurableSplitTableFormatter):
    def __init__(self, style_name: str, report_data: pd.DataFrame, max_total_width: int = 120):
        """
        Formatter for generating and displaying a uniqueness report in a tabular format.

        This class inherits from ConfigurableSplitTableFormatter and uses a predefined style
        to format and display the uniqueness report.

        Parameters
        ----------
        style_name : str
            The name of the style to apply (e.g., 'DEFAULT', 'THIN_LINES', 'DOUBLE_LINES').
        report_data : pd.DataFrame
            The data to be formatted in the table.
        max_total_width : int, optional
            The maximum allowed width for the table (default is 120 characters).

        Example Usage
        -------------
        >>> import pandas as pd
        >>> data = {
        >>>     "Feature Name": ["A very long feature name", "Another long feature name", "Short name"],
        >>>     "Total Unique": [5, 2, 1],
        >>>     "Uniqueness Percentage": [100.0, 40.0, 50.0]
        >>> }
        >>> uniqueness_report_df = pd.DataFrame(data)

        >>> # Using the DEFAULT style
        >>> formatter = UniquenessReportFormatter(style_name="DEFAULT", report_data=uniqueness_report_df,
        max_total_width=120)
        >>> print(formatter.format_table())

        >>> # Using the THIN_LINES style
        >>> formatter = UniquenessReportFormatter(style_name="THIN_LINES", report_data=uniqueness_report_df,
        max_total_width=120)
        >>> print(formatter.format_table())

        >>> # Using the DOUBLE_LINES style
        >>> formatter = UniquenessReportFormatter(style_name="DOUBLE_LINES", report_data=uniqueness_report_df,
        max_total_width=120)
        >>> print(formatter.format_table())

        Expected Outputs
        ----------------
        1. **DEFAULT Style**:
        ┌───────────────────────────┬──────────────┬──────────────────┬──────────────────────────────────┐
        | Feature Name              | Total Unique | Uniqueness %     | Suggestion                       |
        ├───────────────────────────┼──────────────┼──────────────────┼──────────────────────────────────┤
        | A very long feature name  | 5            | 100.00%          | Likely an identifier or unique key|
        | Another long feature name | 2            | 40.00%           | Moderate uniqueness, review as a |
        |                           |              |                  | potential feature.               |
        | Short name                | 1            | 50.00%           | High uniqueness important feature|
        └───────────────────────────┴──────────────┴──────────────────┴──────────────────────────────────┘

        2. **THIN_LINES Style**:
        ┌───────────────────────────┬──────────────┬──────────────────┬──────────────────────────────────┐
        │ Feature Name              │ Total Unique │ Uniqueness %     │ Suggestion                       │
        ├───────────────────────────┼──────────────┼──────────────────┼──────────────────────────────────┤
        │ A very long feature name  │ 5            │ 100.00%          │ Likely an identifier or unique key│
        │ Another long feature name │ 2            │ 40.00%           │ Moderate uniqueness, review as a │
        │                           │              │                  │ potential feature.               │
        │ Short name                │ 1            │ 50.00%           │ High uniqueness important feature│
        └───────────────────────────┴──────────────┴──────────────────┴──────────────────────────────────┘

        3. **DOUBLE_LINES Style**:
        ╔═══════════════════════════╦══════════════╦══════════════════╦════════════════════════════════════╗
        ║ Feature Name              ║ Total Unique ║ Uniqueness %     ║ Suggestion                         ║
        ╠═══════════════════════════╬══════════════╬══════════════════╬════════════════════════════════════╣
        ║ A very long feature name  ║ 5            ║ 100.00%          ║ Likely an identifier or unique key. ║
        ║ Another long feature name ║ 2            ║ 40.00%           ║ Moderate uniqueness, review as a   ║
        ║                           ║              ║                  ║ potential feature.                 ║
        ║ Short name                ║ 1            ║ 50.00%           ║ High uniqueness, important feature.║
        ╚═══════════════════════════╩══════════════╩══════════════════╩════════════════════════════════════╝
            """
        # Define the headers that will be used in the formatted table
        headers = [FEATURE_NAME, TOTAL_UNIQUE, UNIQUENESS_PERCENTAGE, SUGGESTION]

        # Prepare the report data in a list format for the table
        formatted_data = self.prepare_report_data(report_data)

        # Initialize the base class with the headers and formatted data
        super().__init__(style_name, headers, formatted_data, max_total_width)

    @staticmethod
    def determine_suggestion(uniqueness_percentage: float) -> str:
        """
        Determine the suggestion based on the uniqueness percentage.

        Parameters
        ----------
        uniqueness_percentage : float
            The percentage of uniqueness in the column.

        Returns
        -------
        str
            A suggestion based on the uniqueness percentage.
        """
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

    def prepare_report_data(self, report_data: pd.DataFrame) -> List[List[str]]:
        """
        Prepare the uniqueness report data to be formatted.

        Parameters
        ----------
        report_data : pd.DataFrame
            The raw report data.

        Returns
        -------
        List[List[str]]
            The formatted data for the table, with suggestions included.
        """
        formatted_data = []
        for _, row in report_data.iterrows():
            suggestion = self.determine_suggestion(row[UNIQUENESS_PERCENTAGE])
            formatted_row = [str(row[FEATURE_NAME]), f"{row[TOTAL_UNIQUE]:>12}",
                             f"{row[UNIQUENESS_PERCENTAGE]:>10.2f}%", suggestion]
            formatted_data.append(formatted_row)
        return formatted_data

    def format_table(self) -> str:
        """
        Override the format_table method to apply the formatting for the uniqueness report.

        Returns
        -------
        str
            The formatted uniqueness report.
        """
        return super().format_table()


class CategoricalReportFormatter(ConfigurableSplitTableFormatter):
    """
    Formatter for generating and displaying a categorical report in a tabular format.

    This class extends the `ConfigurableSplitTableFormatter` and provides additional functionality
    to filter, sort, and format categorical data for reporting purposes. The user can specify a style
    (e.g., 'DEFAULT', 'THIN_LINES', 'DOUBLE_LINES'), a maximum total table width, sorting options, and
    a filter threshold for category percentages.

    Parameters
    ----------
    style_name : str
        The name of the style to apply (e.g., 'DEFAULT', 'THIN_LINES', 'DOUBLE_LINES').
    report_data : pd.DataFrame
        The categorical report data in a pandas DataFrame format.
    max_total_width : int, optional
        The maximum allowed width for the table (default is 120 characters).
    sort_by : str, optional
        The column to sort the report by (default is None).
    filter_threshold : float, optional
        Filter categories below this percentage (default is None).
    include_missing : bool, optional
        Whether to include missing data handling in the report (default is True).

    Attributes
    ----------
    headers : List[str]
        The table headers, including feature names and categorical information.
    report_data : pd.DataFrame
        The report data provided for formatting.
    sort_by : str
        The column to sort the report by.
    filter_threshold : float
        The threshold for filtering categories based on percentage.
    include_missing : bool
        Flag to include missing data handling in the report.

    Methods
    -------
    apply_threshold()
        Filter out categories below the specified percentage threshold.
    sort_report()
        Sort the report by the specified column, if sorting is enabled.
    prepare_report_data() -> list
        Prepare the report data into a list of lists for display in a formatted table.
    format_table() -> str
        Format the entire categorical report into a styled table based on the specified style.

    Example
    -------
    ```python
    # Sample Data
    import pandas as pd

    data = {
        "Feature Name": ["Category A", "Category B", "Category C", "Category D"],
        "Unique Categories": [10, 5, 8, 3],
        "Most Frequent Category": ["X", "Y", "Z", "W"],
        "Frequency": [100, 50, 80, 20],
        "Category Percentage": [20.0, 10.0, 16.0, 5.0]
    }
    category_report_df = pd.DataFrame(data)

    # Using the DEFAULT style
    formatter = CategoricalReportFormatter(
        style_name="DEFAULT",
        report_data=category_report_df,
        sort_by="Category Percentage",
        filter_threshold=10.0
    )

    print(formatter.format_table())

    # Using the THIN_LINES style
    formatter = CategoricalReportFormatter(
        style_name="THIN_LINES",
        report_data=category_report_df,
        sort_by="Category Percentage",
        filter_threshold=10.0
    )

    print(formatter.format_table())

    # Using the DOUBLE_LINES style
    formatter = CategoricalReportFormatter(
        style_name="DOUBLE_LINES",
        report_data=category_report_df,
        sort_by="Category Percentage",
        filter_threshold=10.0
    )

    print(formatter.format_table())
    ```

    Expected Outputs
    ----------------
    1. **DEFAULT Style**:
    ┌──────────────────────┬────────────────┬─────────────────────────┬──────────┬─────────────────────┐
    | Feature Name          | Unique Categories | Most Frequent Category | Frequency | Category Percentage |
    ├──────────────────────┼────────────────┼─────────────────────────┼──────────┼─────────────────────┤
    | Category A            | 10             | X                       | 100      | 20.00%              |
    | Category B            | 5              | Y                       | 50       | 10.00%              |
    | Category C            | 8              | Z                       | 80       | 16.00%              |
    └──────────────────────┴────────────────┴─────────────────────────┴──────────┴─────────────────────┘

    2. **THIN_LINES Style**:
    ┌──────────────────────┬────────────────┬─────────────────────────┬──────────┬─────────────────────┐
    │ Feature Name          │ Unique Categories │ Most Frequent Category | Frequency | Category Percentage │
    ├──────────────────────┼────────────────┼─────────────────────────┼──────────┼─────────────────────┤
    │ Category A            │ 10             │ X                       │ 100      │ 20.00%              │
    │ Category B            │ 5              │ Y                       │ 50       │ 10.00%              │
    │ Category C            │ 8              │ Z                       │ 80       │ 16.00%              │
    └──────────────────────┴────────────────┴─────────────────────────┴──────────┴─────────────────────┘

    3. **DOUBLE_LINES Style**:
    ╔══════════════════════╦════════════════╦═════════════════════════╦══════════╦═════════════════════╗
    ║ Feature Name          ║ Unique Categories ║ Most Frequent Category ║ Frequency ║ Category Percentage ║
    ╠══════════════════════╬════════════════╬═════════════════════════╬══════════╬═════════════════════╣
    ║ Category A            ║ 10             ║ X                       ║ 100      ║ 20.00%              ║
    ║ Category B            ║ 5              ║ Y                       ║ 50       ║ 10.00%              ║
    ║ Category C            ║ 8              ║ Z                       ║ 80       ║ 16.00%              ║
    ╚══════════════════════╩════════════════╩═════════════════════════╩══════════╩═════════════════════╝
    """

    def __init__(self, style_name: str, report_data: pd.DataFrame, max_total_width: int = 120,
                 sort_by: Optional[str] = None, filter_threshold: Optional[float] = None, include_missing: bool = True):
        # Define the headers using imported global variables from the config
        headers = [FEATURE_NAME, UNIQUE_CATEGORIES, MOST_FREQUENT_CATEGORY, FREQUENCY, CATEGORY_PERCENTAGE]

        # Prepare the report data for formatting, applying filters and sorting as needed
        self.report_data = report_data
        self.sort_by = sort_by
        self.filter_threshold = filter_threshold
        self.include_missing = include_missing

        # Apply filtering and sorting if needed
        self.apply_threshold()
        self.sort_report()

        # Format the report data into a list of lists for display
        formatted_data = self.prepare_report_data()

        # Initialize the base class (ConfigurableSplitTableFormatter)
        super().__init__(style_name, headers, formatted_data, max_total_width)

    def apply_threshold(self):
        """
        Filter categories below a certain percentage threshold, if a threshold is set.
        """
        if self.filter_threshold:
            self.report_data = self.report_data[self.report_data[CATEGORY_PERCENTAGE] > self.filter_threshold]

    def sort_report(self):
        """
        Sort the report by a specified column, if sorting is enabled.
        """
        if self.sort_by and self.sort_by in self.report_data.columns:
            self.report_data = self.report_data.sort_values(by=self.sort_by, ascending=False)

    def prepare_report_data(self) -> list:
        """
        Prepare the report data for display, formatting it as a list of lists.

        Returns
        -------
        List[List[str]]
            The formatted report data.
        """
        formatted_data = []
        for _, row in self.report_data.iterrows():
            formatted_row = [str(row[FEATURE_NAME]), f"{row[UNIQUE_CATEGORIES]:>10}", str(row[MOST_FREQUENT_CATEGORY]),
                             f"{row[FREQUENCY]:>10}", f"{row[CATEGORY_PERCENTAGE]:>10.2f}%"]
            formatted_data.append(formatted_row)
        return formatted_data

    def format_table(self) -> str:
        """
        Override the format_table method to apply the specific formatting for the categorical report.

        Returns
        -------
        str
            The formatted categorical report.
        """
        return super().format_table()


class DuplicateRowsReportFormatter(ConfigurableSplitTableFormatter):
    """
    Formatter for generating and displaying a report of duplicate rows in a tabular format.

    This class extends `ConfigurableSplitTableFormatter` and formats a DataFrame containing
    duplicate rows along with useful statistics such as the total number of duplicate rows,
    percentage of duplicates, and the indices of first and last occurrences.

    Parameters
    ----------
    style_name : str
        The name of the style to apply (e.g., 'DEFAULT', 'THIN_LINES', 'DOUBLE_LINES').
    duplicate_rows : Union[pd.DataFrame, pl.DataFrame]
        The DataFrame containing the duplicate rows.
    stats : Dict[str, Any]
        A dictionary containing statistics about the duplicates (e.g., number of duplicates, percentage).
    max_total_width : int, optional
        The maximum allowed width for the table (default is 120 characters).

    Example Usage
    -------------
    >>> import pandas as pd
    >>> data = {
    >>>     "Column A": [1, 2, 2, 3, 4, 4],
    >>>     "Column B": ["A", "B", "B", "C", "D", "D"]
    >>> }
    >>> df = pd.DataFrame(data)
    >>> duplicate_rows = df[df.duplicated(keep=False)]
    >>> stats = {
    >>>     "num_duplicates": len(duplicate_rows),
    >>>     "duplicate_percentage": (len(duplicate_rows) / len(df)) * 100
    >>> }

    >>> formatter = DuplicateRowsReportFormatter(style_name="DEFAULT", duplicate_rows=duplicate_rows, stats=stats)
    >>> print(formatter.format_table())

    Expected Output
    ---------------
    1. **DEFAULT Style**:
    ┌───────────────────────┬──────────────────────┬──────────────────────────┬─────────────────────┬─────────────────────┬───────────────────┐
    | Duplicate Rows        | Total Duplicates     | Percentage (%)           | First Occurrence     | Last
    Occurrence     | Duplicate Count   |
    ├───────────────────────┼──────────────────────┼──────────────────────────┼─────────────────────┼─────────────────────┼───────────────────┤
    | Column A: 2, Column B: B  | 2                   | 33.33%                   | 1                   | 2
           | 2                 |
    | Column A: 4, Column B: D  | 2                   | 33.33%                   | 4                   | 5
           | 2                 |
    └───────────────────────┴──────────────────────┴──────────────────────────┴─────────────────────┴─────────────────────┴───────────────────┘
    """

    def __init__(self, style_name: str, duplicate_rows: Union[pd.DataFrame, pl.DataFrame], stats: Dict[str, Any],
                 max_total_width: int = 120):
        # Define the headers using imported global variables from the config
        headers = [DUPLICATE_ROWS, TOTAL_DUPLICATES, DUPLICATE_PERCENTAGE, FIRST_OCCURRENCE, LAST_OCCURRENCE,
                   DUPLICATE_COUNT]

        # Store the duplicate rows and stats
        self.duplicate_rows = duplicate_rows
        self.stats = stats

        # Format the report data into a list of lists for display
        formatted_data = self.prepare_report_data()

        # Initialize the base class (ConfigurableSplitTableFormatter)
        super().__init__(style_name, headers, formatted_data, max_total_width)

    def prepare_report_data(self) -> List[List[str]]:
        """
        Prepare the duplicate rows report data, including statistics.

        Returns
        -------
        List[List[str]]
            The formatted duplicate rows report data.
        """
        formatted_data = []

        # Get first and last occurrences of the duplicate rows
        first_occurrences = self.duplicate_rows.drop_duplicates(keep="first").index
        last_occurrences = self.duplicate_rows.drop_duplicates(keep="last").index

        # Iterate over duplicate rows and format the report
        for idx, row in self.duplicate_rows.iterrows():
            first_occurrence = first_occurrences.get_loc(idx) if idx in first_occurrences else "N/A"
            last_occurrence = last_occurrences.get_loc(idx) if idx in last_occurrences else "N/A"
            duplicate_count = self.duplicate_rows.duplicated(keep=False).sum()

            formatted_row = [", ".join([f"{col}: {row[col]}" for col in self.duplicate_rows.columns]),
                str(self.stats["num_duplicates"]), f"{self.stats['duplicate_percentage']:.2f}%", str(first_occurrence),
                str(last_occurrence), str(duplicate_count)]
            formatted_data.append(formatted_row)

        return formatted_data

    def format_table(self) -> str:
        """
        Override the format_table method to apply the specific formatting for the duplicate rows report.

        Returns
        -------
        str
            The formatted duplicate rows report.
        """
        return super().format_table()


# ========================
# To do:
# Class needs more work
# ========================
class DuplicateColumnsReportFormatter(ConfigurableSplitTableFormatter):
    """
    Formatter for generating and displaying a duplicate columns report in a tabular format.

    This class inherits from `ConfigurableSplitTableFormatter` and formats and displays the duplicate
    columns report. It supports optional filtering and custom table styles.

    Parameters
    ----------
    style_name : str
        The name of the style to apply (e.g., 'DEFAULT', 'THIN_LINES', 'DOUBLE_LINES').
    duplicate_columns : pd.DataFrame
        A DataFrame containing only the duplicate columns.
    stats : Dict[str, Any]
        A dictionary containing statistics about the duplicate columns (e.g., total number of duplicate columns).
    max_total_width : int, optional
        The maximum allowed width for the table (default is 120 characters).

    Example Usage
    -------------
    >>> # Sample Data
    >>> import pandas as pd
    >>> data = {
    >>>     'A': [1, 2, 3],
    >>>     'B': [1, 2, 3],
    >>>     'C': [4, 5, 6],
    >>>     'D': [1, 2, 3]
    >>> }
    >>> df = pd.DataFrame(data)

    >>> # Detect duplicate columns
    >>> duplicate_columns = df.loc[:, df.T.duplicated()]
    >>> stats = {
    >>>     'num_duplicates': len(duplicate_columns.columns),
    >>>     'duplicate_percentage': (len(duplicate_columns.columns) / len(df.columns)) * 100
    >>> }

    >>> # Using the DEFAULT style
    >>> formatter_default = DuplicateColumnsReportFormatter(
    >>>     style_name="DEFAULT",
    >>>     duplicate_columns=duplicate_columns,
    >>>     stats=stats,
    >>>     max_total_width=120
    >>> )

    >>> print("DEFAULT Style Table:")
    >>> print(formatter_default.format_table())

    Styles
    ------
    **DEFAULT Style:**
    ┌───────────────────────────┬─────────────────────┬───────────────────────────┐
    | Column Name               | Number of Duplicates | Duplicate Percentage      |
    ├───────────────────────────┼─────────────────────┼───────────────────────────┤
    | A                         | 2                   | 50.00%                    |
    | D                         | 2                   | 50.00%                    |
    └───────────────────────────┴─────────────────────┴───────────────────────────┘

    **THIN_LINES Style:**
    ┌───────────────────────────┬─────────────────────┬───────────────────────────┐
    │ Column Name               │ Number of Duplicates │ Duplicate Percentage      │
    ├───────────────────────────┼─────────────────────┼───────────────────────────┤
    │ A                         │ 2                   │ 50.00%                    │
    │ D                         │ 2                   │ 50.00%                    │
    └───────────────────────────┴─────────────────────┴───────────────────────────┘

    **DOUBLE_LINES Style:**
    ╔═══════════════════════════╦═════════════════════╦═══════════════════════════╗
    ║ Column Name               ║ Number of Duplicates ║ Duplicate Percentage      ║
    ╠═══════════════════════════╬═════════════════════╬═══════════════════════════╣
    ║ A                         ║ 2                   ║ 50.00%                    ║
    ║ D                         ║ 2                   ║ 50.00%                    ║
    ╚═══════════════════════════╩═════════════════════╩═══════════════════════════╝
    """

    def __init__(self, style_name: str, duplicate_columns: pd.DataFrame, stats: Dict[str, Any],
                 max_total_width: int = 120):
        """
        Initialize the duplicate columns report formatter.
        """
        # Define the headers for the duplicate columns report
        headers = [FEATURE_NAME, "Number of Duplicates", "Duplicate Percentage"]

        # Store the provided stats and duplicate columns for formatting
        self.duplicate_columns = duplicate_columns
        self.stats = stats

        # Format the report data into a list of lists for display
        formatted_data = self.prepare_report_data()

        # Initialize the base class (ConfigurableSplitTableFormatter)
        super().__init__(style_name, headers, formatted_data, max_total_width)

    def prepare_report_data(self) -> List[List[str]]:
        """
        Prepare the duplicate columns report data to be formatted.

        Returns
        -------
        List[List[str]]
            The formatted data for the table, with stats included.
        """
        formatted_data = []
        for col in self.duplicate_columns.columns:
            formatted_row = [str(col), str(self.duplicate_columns[col].duplicated().sum() + 1),
                             # Include the original column as well
                             f"{self.stats['duplicate_percentage']:.2f}%"]
            formatted_data.append(formatted_row)
        return formatted_data

    def format_table(self) -> str:
        """
        Override the format_table method to apply the formatting for the duplicate columns report.

        Returns
        -------
        str
            The formatted duplicate columns report.
        """
        return super().format_table()

# Other reports
# 	1.	Missing Data Report
# 	2.	Outlier Detection Report
# 	3.	Data Type Consistency Report
# 	4.	Cardinality and Frequency Distribution Report
# 	5.	Correlated Features Report
# 	6.	Imbalance Report for Target Variables
# 	7.	Feature Interaction Report

# ================================================
# Other Advanced Reports
# 	1.	Time Series Analysis Report
# 	2.	Multi-collinearity Detection Report
# 	3.	Feature Importance Report
# 	4.	PCA & Dimensionality Reduction Report
# 	5.	Data Distribution Analysis Report
# 	6.	Clustering Analysis Report
# 	7.	Residual Analysis Report
# 	8.	Noise Detection and Removal Report
# 	9.	Anomaly Detection Report
# 	10.	Dataset Summary and Overview Report
# 	11.	Data Imputation Strategy Report
# ================================================


# class MissingnessReportFormatter(TableFormatter):
#     def __init__(self):
#         headers = [FEATURE_NAME, NMISSING, PMISSING]
#         super().__init__(headers)
#
#     def format(self, missingness_report: Dict[str, Any]) -> str:
#         field_format = "{missing_count:>8} | {missing_percentage:>26.1f}%"
#         return self.format_report(missingness_report, field_format)
