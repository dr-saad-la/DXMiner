
from typing import Dict, Any

def format_missingness_report(missingness_report: Dict[str, Any]) -> str:
    result = ["Missingness Report:"]
    for col, data in missingness_report.items():
        result.append(f"  - {col}: {data['missing_count']} missing values "
                      f"({data['missing_percentage']}%)")
    return "\n".join(result)

def format_uniqueness_report(uniqueness_report: Dict[str, Any]) -> str:
    result = ["Uniqueness Report:"]
    for col, data in uniqueness_report.items():
        result.append(f"  - {col}: {data['unique_count']} unique values "
                      f"({data['unique_percentage']}%)")
    return "\n".join(result)

def format_category_report(category_report: Dict[str, Any]) -> str:
    result = ["Category Report:"]
    for col, data in category_report.items():
        result.append(f"  - {col}: {data['unique_categories']} unique categories, "
                      f"most frequent is '{data['most_frequent_category']}' with "
                      f"{data['frequency']} occurrences")
    return "\n".join(result)

def format_report(report: Dict[str, Any], summary: bool = False) -> str:
    result = [
        f"Data Shape: {report['shape']}"
    ]

    if summary:
        result.append(format_missingness_report(report["missingness_report"]))
        result.append(format_uniqueness_report(report["uniqueness_report"]))
    else:
        result.append(format_missingness_report(report["missingness_report"]))
        result.append(format_uniqueness_report(report["uniqueness_report"]))
        result.append(format_category_report(report["category_report"]))
        result.append(f"Duplicate Rows: {report['duplicate_rows']}")
        result.append(f"Duplicate Columns: {report['duplicate_columns']}")

    return "\n".join(result)
