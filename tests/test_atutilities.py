#-----------------------------------------------------------------------------+
import pytest
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
    # Obtain current_timestamp() to use as input to iso_date()
    # Test with current_timestamp() len is reasonable
    assert len(dt_str := atu.current_timestamp()) >= len("2023-10-01T12:00:00"), \
        f"current_timestamp() invalid ISO date string:'{dt_str}' len={len(dt_str)}"
    assert (dt := atu.iso_date(dt_str)) is not None, \
        f"iso_date(\"{dt_str}\") returned None"
    assert atu.confirm_iso_date(dt), \
        f"iso_date(\"{dt_str}\") returned invalid internal ISO Date object"
    
    # Test iso_date() with invalid recoverable input of None or ""
    # Test iso_date() converts None and "" inputs to current time 
    # Note: the default tolerance is 1 second, be careful with breakpoints
    # and delays in the test.
    assert atu.confirm_iso_date((dt := atu.iso_date(None))), \
        "iso_date(None) returned invalid internal ISO Date object"
    assert atu.iso_date_approx(atu.iso_date_string(dt), \
                               atu.current_timestamp()), \
        f"iso_date(None) not approx = to current_timestamp() default tolerance"
    assert atu.confirm_iso_date((dt := atu.iso_date(""))), \
        f"iso_date(\"\") returned invalid internal ISO Date object"
    assert atu.iso_date_approx(atu.iso_date_string(dt), \
                               atu.current_timestamp()), \
        f"iso_date(\"\") is not approximately equal to current_timestamp()"

    # Test with invalid ISO date string
    with pytest.raises(ValueError):
        atu.iso_date("invalid-date-string")
    # Test with valid but different ISO date format
    dt_str = "2023-10-01 12:00:00"
    assert (dt := atu.iso_date(dt_str)) is not None, \
        f"iso_date(\"{dt_str}\") returned None"
    assert dt == atu.iso_date(dt_str), \
        "iso_date() should handle different formats correctly"
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

#region test_now_iso_date()
def test_now_iso_date():
    """Test the now_iso_date function."""
    now = atu.now_iso_date()
    assert atu.confirm_iso_date(atu.now_iso_date()), \
        "now_iso_date() returned an invalid internal ISO Date object"
    # Allow for a small delay in the test
    # to ensure the current time is after the recorded 'now'
    assert atu.now_iso_date() >= now, "now_iso_date should return current datetime"
#endregion

#region test_now_iso_date_string()
def test_now_iso_date_string():
    """Test the now_iso_date_string function."""
    assert (now := atu.now_iso_date()) is not None, \
        "now_iso_date() returned None"
    assert atu.confirm_iso_date(now), \
        "now_iso_date() returned an invalid internal ISO Date object"
    # Allow for a small delay in the test
    # to ensure the current time is after the recorded 'now'
    assert atu.now_iso_date() >= now, \
        "now_iso_date() did compare greater than a previous call"
#endregion

#region test_iso_date_approx()
def test_iso_date_approx():
    """Test the iso_date_approx function."""
    dt1 = "2023-10-01T12:00:00"
    dt2 = "2023-10-01T12:00:05"  # 5 seconds apart
    tol = 10
    assert atu.iso_date_approx(dt1, dt2, tolerance=tol), \
          f"'{dt1}' not approx equal to '{dt2}', tolerance: {tol} seconds"
    assert not atu.iso_date_approx(dt1, dt2), \
          f"'{dt1}' not approx equal to '{dt2}', default tolerance"
    

    dt1 = atu.now_iso_date_string()  # Current time
    dt2 = atu.now_iso_date_string()  # Current time
    assert atu.iso_date_approx(dt1, dt2), \
          f"'{dt1}' not approx equal to '{dt2}', default tolerance"

    # Test with None values, should default to current time
    assert atu.iso_date_approx(None, atu.now_iso_date_string())
    assert atu.iso_date_approx(atu.now_iso_date_string(), None)
    assert atu.iso_date_approx(None, None)
    with pytest.raises(TypeError):
        assert atu.iso_date_approx(atu.now_iso_date_string(), \
                                atu.now_iso_date_string(), None)

    # Test with "" values, should default to current time
    assert atu.iso_date_approx("", atu.now_iso_date_string())
    assert atu.iso_date_approx(atu.now_iso_date_string(), "")
    assert atu.iso_date_approx("", "")
    with pytest.raises(TypeError):
        assert atu.iso_date_approx(atu.now_iso_date_string(), \
                                atu.now_iso_date_string(), "")

    # Test with invalid tolerance
    with pytest.raises(TypeError):
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
    assert atu.iso_date_approx(atu.validate_start(None), atu.now_iso_date_string(), 2)

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
    assert atu.validate_iso_date_string(valid_iso_date), \
        f"Valid ISO date '{valid_iso_date}' failed validation"
    with pytest.raises(ValueError):
        atu.validate_iso_date_string(invalid_iso_date)
#endregion



