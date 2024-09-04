"""
Global configuration constants for dxminer.


"""

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
