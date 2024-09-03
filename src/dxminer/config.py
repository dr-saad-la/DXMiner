"""
Global configuration constants for dxminer.


"""
# The wrapping width for column names
COL_WIDTH = 32

# The character for separators in table formatting
SEPARATOR_CHAR = '-'

# Header Names
FEATURE_NAME: str = "Feature Name"
NMISSING: str = "N Missing"
PMISSING: str = "Missingness Percentage (%)"
UNIQUE_COUNT: str = "Unique Count"
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
