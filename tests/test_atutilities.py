#-----------------------------------------------------------------------------+
import datetime, pytest
from typing import List
import at_utilities.at_utils as atu

#region ISO Date Utilities

#region test_iso_date_string()
def test_iso_date_string():
    """Test the iso_date_string function."""
    expected_iso = atu.current_timestamp()
    dt  = atu.iso_date(expected_iso)
    assert atu.confirm_iso_date(dt), \
        f"iso_date() Returned invalid object Type:'{type(dt).__name__}' "
    assert (res := atu.iso_date_string(dt)) == expected_iso, \
      f"iso_date_string() incorrect return='{res}' expected='{expected_iso}'"
    assert not atu.confirm_iso_date("foo"), \
        "confirm_iso_date() failed to detect incorrect input type' "
    # Test with unvalid type of input
    with pytest.raises(TypeError) : atu.iso_date_string(None)
    with pytest.raises(TypeError) : atu.iso_date_string("")
    with pytest.raises(TypeError) : atu.iso_date_string(12345)
    with pytest.raises(TypeError) : atu.iso_date_string((1,2,3,4,5))
    with pytest.raises(TypeError) : atu.iso_date_string([1,2,3,4,5])
#endregion

#region test_iso_date()
def test_iso_date():
    """Test the iso_date and confirm_iso_date functions."""
    dt_str : str = None
    # Test with current timestamp len is reasonable
    assert len(dt_str := atu.current_timestamp()) >= len("2023-10-01T12:00:00"), \
        f"current_timestamp() invalid ISO date string:'{dt_str}' len={len(dt_str)}"
    
    assert (dt := atu.iso_date(dt_str)) is not None, \
        f"iso_date(\"{dt_str}\") returned None"

    # Test with None and empty string. iso_date() should convert to now()
    assert (dt2_str := atu.current_timestamp()) is not None, \
        f"current_timestamp() returned None"
    assert atu.iso_date_approx(dt_str, dt2_str), \
        f"iso_date(\"{dt_str}\") and iso_date_now() are not approximately equal"
    # Test iso_date(None) and iso_date_now() are approximately equal
    assert atu.iso_date_approx(atu.iso_date(None), dt2_str), \
        "iso_date(None) and iso_date_now() are not approximately equal"
    # Test iso_date("")) and iso_date_now() are approximately equal
    assert atu.iso_date_approx(atu.iso_date("") , dt2_str), \
         "iso_date(\"\") and iso_date_now() are not approximately equal"

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
#endregion

#region test_iso_date_now()
def test_iso_date_now():
    """Test the iso_date_now function."""
    now = datetime.datetime.now()
    assert isinstance(atu.iso_date_now(), datetime.datetime), "iso_date_now should return a datetime object"
    # Allow for a small delay in the test
    # to ensure the current time is after the recorded 'now'
    assert atu.iso_date_now() >= now, "iso_date_now should return current datetime"
#endregion

#region test_iso_date_now_string()
def test_iso_date_now_string():
    """Test the iso_date_now_string function."""
    now = datetime.datetime.now()
    assert isinstance(atu.iso_date_now_string(), str), "iso_date_now_string should return a string"
    # Allow for a small delay in the test
    # to ensure the current time is after the recorded 'now'
    assert datetime.datetime.fromisoformat(atu.iso_date_now_string()) >= now, \
        "iso_date_now_string should return current datetime in ISO format"
#endregion

#region test_iso_date_approx()
def test_iso_date_approx():
    """Test the iso_date_approx function."""
    dt1 = "2023-10-01T12:00:00"
    dt2 = "2023-10-01T12:00:05"  # 5 seconds apart
    assert atu.iso_date_approx(dt1, dt2, tolerance=10), "Dates should be approximately equal within 10 seconds"

    dt1 = atu.iso_date_now_string()  # Current time
    dt2 = atu.iso_date_now_string()  # Current time
    assert atu.iso_date_approx(dt1, dt2, tolerance=1), "Dates should be approximately equal within 1 second"

    # Test with None values
    with pytest.raises(ValueError):
        atu.iso_date_approx(None, dt2)
    with pytest.raises(ValueError):
        atu.iso_date_approx(dt1, None)

    # Test with invalid tolerance
    with pytest.raises(ValueError):
        atu.iso_date_approx(dt1, dt2, tolerance="invalid")

    # Test with invalid date strings
    with pytest.raises(ValueError):
        atu.iso_date_approx("invalid-date-string", dt2)
    with pytest.raises(ValueError):
        atu.iso_date_approx(dt1, "invalid-date-string")
#endregion test_iso_date_approx()
#endregion ISO Date Utilities

#region test_validate_start()
def test_validate_start():
    """Test None, "", invalid ISO, and tuple as input to AE.validate_start()"""
    # Assuming validate_start is a static method of ActivityEntry class
    try:
        valid_start = atu.default_start_time()
        invalid_start = "invalid-date-format"
    except:
        pytest.fail("Setup failed for valid|invalid start time parameters")

    # Test valid start time
    assert atu.validate_start(valid_start) == valid_start

    # Test empty string for start time, expect conversion to default of now()

    # Test invalid start time string value, not valid ISO value
    with pytest.raises(ValueError):
        atu.validate_start(invalid_start)

    # Test invalid input type None start time, expect validate_start() to 
    # return now(), so the comparison should be within 2 seconcds.
    assert atu.iso_date_approx(atu.validate_start(None), atu.iso_date_now_string(), 2)

    # Test invalid input type tuple start time
    with pytest.raises(TypeError):
        atu.validate_start((1,2))
#endregion

#region test_validate_stop()
def test_validate_stop():
    # Assuming validate_stop is a static method of ActivityEntry class
    valid_start : str = atu.default_start_time() 
    valid_stop : str = atu.default_stop_time(valid_start)
    invalid_stop = "invalid-date-format"

    # Test valid stop time 
    assert atu.validate_stop(valid_start, valid_stop) == valid_stop, \
        "Valid stop time failed validation"

    # Test invalid stop time string value
    with pytest.raises(ValueError):
        atu.validate_stop(valid_start, invalid_stop)

    # Test invalid input type None stop time
    # Expect validate_stop() to return default_stop_time()
    assert atu.validate_stop(valid_start, None), "stop time of None failed validation"

    # Test invalid input type tuple stop time
    with pytest.raises(TypeError):
        atu.validate_stop(valid_start, (1,2))
#endregion

#region test_validate_iso_date_string()
def test_validate_iso_date_string():
    valid_iso_date = "2025-01-20T13:00:00"
    invalid_iso_date = "invalid-date-format"
    assert atu.validate_iso_date_string(valid_iso_date) == True, \
        "Valid ISO date string failed validation"
    with pytest.raises(ValueError):
        atu.validate_iso_date_string(invalid_iso_date)
#endregion



