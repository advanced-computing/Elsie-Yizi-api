import pandas as pd
from lab_5 import check_unique, check_no_missing, parse_dates


def test_check_unique():
    ids = pd.Series([1, 2, 3, 4])
    result = check_unique(ids)
    expected = pd.Series([True])

    assert result.equals(expected)


def test_check_no_missing():
    borough = pd.Series(["MANHATTAN", "BROOKLYN", "QUEENS"])
    result = check_no_missing(borough)
    expected = pd.Series([True])

    assert result.equals(expected)


def test_parse_dates():
    dates = pd.Series(["02/13/2025", "08/22/2025"])
    result = parse_dates(dates)
    expected = pd.to_datetime(pd.Series(["02/13/2025", "08/22/2025"]))

    assert result.equals(expected)
