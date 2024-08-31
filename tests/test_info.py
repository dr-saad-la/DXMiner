import io
import pytest
import pandas as pd
import polars as pl
from dxminer.explore.info import data_info


@pytest.fixture
def sample_data():
    # Create sample data for testing
    pandas_df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6], "C": ["a", "b", "c"]})

    polars_df = pl.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6], "C": ["a", "b", "c"]})

    return pandas_df, polars_df


def test_data_info_pandas(capsys, sample_data):
    pandas_df, _ = sample_data

    data_info(pandas_df, banner_text="Pandas DataFrame Info")

    captured = capsys.readouterr()

    assert "Pandas DataFrame Info" in captured.out
    assert "RangeIndex: 3 entries, 0 to 2" in captured.out
    assert "Data columns (total 3 columns):" in captured.out
    assert "dtypes: int64(2), object(1)" in captured.out

    # Count the expected number of banner lines (3 each for top and bottom)
    # assert captured.out.count("=" * len("= Pandas DataFrame Info =")) == 2


def test_data_info_polars(capsys, sample_data):
    _, polars_df = sample_data

    data_info(polars_df, banner_text="Polars DataFrame Info")

    captured = capsys.readouterr()

    assert "Polars DataFrame Info" in captured.out
    assert "shape: (3, 3)" in captured.out
    assert "shape: (3, 3)" in captured.out

    # Check for columns' presence in the output
    assert "A" in captured.out
    assert "B" in captured.out
    assert "C" in captured.out

    assert "f64" in captured.out
    assert "str" in captured.out

    # Count the expected number of banner lines (2 total, one for top and one for bottom)
    assert captured.out.count("=" * len("= Polars DataFrame Info =")) == 3

    # assert "┌─────┬─────┬─────┐" in captured.out  # Check for Polars table format
    # assert captured.out.count("=" * len("= Polars DataFrame Info =")) == 2


def test_invalid_input():
    with pytest.raises(ValueError):
        data_info([1, 2, 3], banner_text="Invalid Input")
