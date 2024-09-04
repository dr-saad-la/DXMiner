"""
Global configuration constants for dxminer.


"""

# config.py

# Annotation for type hinting
from typing import Dict

# Table formatting configurations stored as a dictionary with multiple styles.
STYLES: Dict[str, Dict[str, str]] = {
    "DEFAULT": {
        "COL_WIDTH": 25,
        "MAX_COL_WIDTH": 32,
        "INNER_SEP_CHAR": "─",
        "HEADER_SEP_CHAR": "─",
        "OUTER_SIDE_CHAR": "|",
        "INNER_VERTICAL_CHAR": "|",
        "TOP_LEFT_CHAR": "┌",
        "TOP_RIGHT_CHAR": "┐",
        "BOTTOM_LEFT_CHAR": "└",
        "BOTTOM_RIGHT_CHAR": "┘",
        "TOP_JOIN_CHAR": "┬",
        "BOTTOM_JOIN_CHAR": "┴"
    },
    "STARS": {
        "COL_WIDTH": 25,
        "MAX_COL_WIDTH": 32,
        "INNER_SEP_CHAR": "*",
        "HEADER_SEP_CHAR": "*",
        "OUTER_SIDE_CHAR": "*",
        "INNER_VERTICAL_CHAR": "*",
        "TOP_LEFT_CHAR": "*",
        "TOP_RIGHT_CHAR": "*",
        "BOTTOM_LEFT_CHAR": "*",
        "BOTTOM_RIGHT_CHAR": "*",
        "TOP_JOIN_CHAR": "*",
        "BOTTOM_JOIN_CHAR": "*"
    },
    "SPSS": {
        "COL_WIDTH": 25,
        "MAX_COL_WIDTH": 32,
        "INNER_SEP_CHAR": "=",
        "HEADER_SEP_CHAR": "=",
        "OUTER_SIDE_CHAR": "|",
        "INNER_VERTICAL_CHAR": "|",
        "TOP_LEFT_CHAR": "+",
        "TOP_RIGHT_CHAR": "+",
        "BOTTOM_LEFT_CHAR": "+",
        "BOTTOM_RIGHT_CHAR": "+",
        "TOP_JOIN_CHAR": "+",
        "BOTTOM_JOIN_CHAR": "+"
    },
    "SAS": {
        "COL_WIDTH": 25,
        "MAX_COL_WIDTH": 32,
        "INNER_SEP_CHAR": "-",
        "HEADER_SEP_CHAR": "-",
        "OUTER_SIDE_CHAR": "|",
        "INNER_VERTICAL_CHAR": "|",
        "TOP_LEFT_CHAR": "+",
        "TOP_RIGHT_CHAR": "+",
        "BOTTOM_LEFT_CHAR": "+",
        "BOTTOM_RIGHT_CHAR": "+",
        "TOP_JOIN_CHAR": "+",
        "BOTTOM_JOIN_CHAR": "+"
    },
    "STATS": {
        "COL_WIDTH": 25,
        "MAX_COL_WIDTH": 32,
        "INNER_SEP_CHAR": "=",
        "HEADER_SEP_CHAR": "=",
        "OUTER_SIDE_CHAR": "|",
        "INNER_VERTICAL_CHAR": "|",
        "TOP_LEFT_CHAR": "=",
        "TOP_RIGHT_CHAR": "=",
        "BOTTOM_LEFT_CHAR": "=",
        "BOTTOM_RIGHT_CHAR": "=",
        "TOP_JOIN_CHAR": "=",
        "BOTTOM_JOIN_CHAR": "="
    },
    "BOLD_LINES": {
        "COL_WIDTH": 25,
        "MAX_COL_WIDTH": 32,
        "INNER_SEP_CHAR": "━",
        "HEADER_SEP_CHAR": "━",
        "OUTER_SIDE_CHAR": "┃",
        "INNER_VERTICAL_CHAR": "┃",
        "TOP_LEFT_CHAR": "┏",
        "TOP_RIGHT_CHAR": "┓",
        "BOTTOM_LEFT_CHAR": "┗",
        "BOTTOM_RIGHT_CHAR": "┛",
        "TOP_JOIN_CHAR": "┳",
        "BOTTOM_JOIN_CHAR": "┻"
    },
    "DASHED_LINES": {
        "COL_WIDTH": 25,
        "MAX_COL_WIDTH": 32,
        "INNER_SEP_CHAR": "-",
        "HEADER_SEP_CHAR": "-",
        "OUTER_SIDE_CHAR": ":",
        "INNER_VERTICAL_CHAR": ":",
        "TOP_LEFT_CHAR": "-",
        "TOP_RIGHT_CHAR": "-",
        "BOTTOM_LEFT_CHAR": "-",
        "BOTTOM_RIGHT_CHAR": "-",
        "TOP_JOIN_CHAR": "-",
        "BOTTOM_JOIN_CHAR": "-"
    },
    "DOUBLE_LINES": {
        "COL_WIDTH": 25,
        "MAX_COL_WIDTH": 32,
        "INNER_SEP_CHAR": "═",
        "HEADER_SEP_CHAR": "═",
        "OUTER_SIDE_CHAR": "║",
        "INNER_VERTICAL_CHAR": "║",
        "TOP_LEFT_CHAR": "╔",
        "TOP_RIGHT_CHAR": "╗",
        "BOTTOM_LEFT_CHAR": "╚",
        "BOTTOM_RIGHT_CHAR": "╝",
        "TOP_JOIN_CHAR": "╦",
        "BOTTOM_JOIN_CHAR": "╩"
    },
    "THIN_LINES": {
        "COL_WIDTH": 25,
        "MAX_COL_WIDTH": 32,
        "INNER_SEP_CHAR": "╌",
        "HEADER_SEP_CHAR": "╌",
        "OUTER_SIDE_CHAR": "│",
        "INNER_VERTICAL_CHAR": "│",
        "TOP_LEFT_CHAR": "┌",
        "TOP_RIGHT_CHAR": "┐",
        "BOTTOM_LEFT_CHAR": "└",
        "BOTTOM_RIGHT_CHAR": "┘",
        "TOP_JOIN_CHAR": "┬",
        "BOTTOM_JOIN_CHAR": "┴"
    },
    "SLANTED_LINES": {
        "COL_WIDTH": 25,
        "MAX_COL_WIDTH": 32,
        "INNER_SEP_CHAR": "/",
        "HEADER_SEP_CHAR": "/",
        "OUTER_SIDE_CHAR": "\\",
        "INNER_VERTICAL_CHAR": "/",
        "TOP_LEFT_CHAR": "/",
        "TOP_RIGHT_CHAR": "\\",
        "BOTTOM_LEFT_CHAR": "\\",
        "BOTTOM_RIGHT_CHAR": "/",
        "TOP_JOIN_CHAR": "/",
        "BOTTOM_JOIN_CHAR": "\\"
    },
    "BLOCK_STYLE": {
        "COL_WIDTH": 25,
        "MAX_COL_WIDTH": 32,
        "INNER_SEP_CHAR": "█",
        "HEADER_SEP_CHAR": "█",
        "OUTER_SIDE_CHAR": "█",
        "INNER_VERTICAL_CHAR": "█",
        "TOP_LEFT_CHAR": "█",
        "TOP_RIGHT_CHAR": "█",
        "BOTTOM_LEFT_CHAR": "█",
        "BOTTOM_RIGHT_CHAR": "█",
        "TOP_JOIN_CHAR": "█",
        "BOTTOM_JOIN_CHAR": "█"
    }
}



# Width settings
COL_WIDTH = 25                 # The main column width
MAX_COL_WIDTH = 32             # The max column width

# Separator settings
INNER_SEP_CHAR = '─'           # Inner separator character (between rows)
HEADER_SEP_CHAR = "─"          # Header separator character (below the header)
OUTER_SIDE_CHAR = "|"          # Outer table side character
INNER_VERTICAL_CHAR = "|"      # Inner vertical separator between columns
TOP_LEFT_CHAR = "┌"            # Custom top-left corner character
TOP_RIGHT_CHAR = "┐"           # Custom top-right corner character
BOTTOM_LEFT_CHAR = "└"         # Custom bottom-left corner character
BOTTOM_RIGHT_CHAR = "┘"        # Custom bottom-right corner character
TOP_JOIN_CHAR = "┬"            # Custom character where top rules meet inner verticals
BOTTOM_JOIN_CHAR = "┴"         # Custom character where bottom rules meet inner verticals

# Header Names
FEATURE_NAME: str = "Feature Name"
NMISSING: str = "N Missing"
PMISSING: str = "Missingness Percentage (%)"
TOTAL_UNIQUE: str = "Total Unique"
TOTAL_COUNT: str = "Total Count"
SUGGESTION: str = "Suggestion"
UNIQUENESS_PERCENTAGE: str = "Uniqueness Percentage"
UNIQUE_CATEGORIES: str = "Unique Categories"  # Suggestions: Distinct Classes, Unique Levels ...
MOST_FREQUENT_CATEGORY: str = "Most Frequent Category"  # Suggestions: Most Frequent Class,
# Level ...
FREQUENCY: str = "Frequency"
CATEGORY_PERCENTAGE: str = "Category Percentage"

# CONDITIONS & SUGGESTIONS
UNIQUENESS_CONDITIONS = [(lambda percentage: percentage == 100),
                         (lambda percentage: percentage > 90), (lambda percentage: percentage > 50),
                         (lambda percentage: percentage > 10),
                         (lambda percentage: percentage <= 10)]

UNIQUENESS_SUGGESTIONS = ["Likely an identifier or unique key.",
                          "Very high uniqueness, consider as a key feature.",
                          "High uniqueness, important feature.",
                          "Moderate uniqueness, review as a potential feature.",
                          "Low uniqueness, may have limited feature importance."]
