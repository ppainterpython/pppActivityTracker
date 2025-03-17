#-----------------------------------------------------------------------------+
import datetime, pytest, json
from typing import List
import at_utilities.at_utils as atu
from model.ae import ActivityEntry

def test_iso_date_string():
    """Test the iso_date_string function."""
    dt = datetime.datetime(2023, 10, 1, 12, 0, 0)
    expected_iso = "2023-10-01T12:00:00"
    assert atu.iso_date_string(dt) == expected_iso, "iso_date_string returned incorrect value"

def test_iso_date():
    """Test the iso_date function."""
    dt_str = "2023-10-01T12:00:00"
    expected_dt = datetime.datetime(2023, 10, 1, 12, 0, 0)
    assert atu.iso_date(dt_str) == expected_dt, "iso_date returned incorrect datetime object"

    # Test with None and empty string
    assert atu.iso_date(None) <= datetime.datetime.now(), "iso_date should return now for None"
    assert atu.iso_date("") <= datetime.datetime.now(), "iso_date should return now for empty string"

    # Test with invalid string
    with pytest.raises(ValueError):
        atu.iso_date("invalid-date-string")
    # Test with valid but different format
    dt_str = "2023-10-01 12:00:00"
    expected_dt = datetime.datetime(2023, 10, 1, 12, 0, 0)
    assert atu.iso_date(dt_str) == expected_dt, "iso_date should handle different formats correctly"
    # Test with invalid format
    with pytest.raises(ValueError):
        atu.iso_date("2023/10/01 12:00:00")
    # Test with invalid date
    with pytest.raises(ValueError):
        atu.iso_date("2023-02-30T12:00:00")
    # Test with invalid time
    with pytest.raises(ValueError):
        atu.iso_date("2023-10-01T25:00:00")
    # Test with invalid datetime
    with pytest.raises(ValueError):
        atu.iso_date("2023-10-01T12:60:00")

def test_iso_date_now():
    """Test the iso_date_now function."""
    now = datetime.datetime.now()
    assert isinstance(atu.iso_date_now(), datetime.datetime), "iso_date_now should return a datetime object"
    # Allow for a small delay in the test
    # to ensure the current time is after the recorded 'now'
    assert atu.iso_date_now() >= now, "iso_date_now should return current datetime"

def test_iso_date_now_string():
    """Test the iso_date_now_string function."""
    now = datetime.datetime.now()
    assert isinstance(atu.iso_date_now_string(), str), "iso_date_now_string should return a string"
    # Allow for a small delay in the test
    # to ensure the current time is after the recorded 'now'
    assert datetime.datetime.fromisoformat(atu.iso_date_now_string()) >= now, \
        "iso_date_now_string should return current datetime in ISO format"
    



