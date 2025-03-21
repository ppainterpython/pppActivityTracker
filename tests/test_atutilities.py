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
    # Test with invalid type of input
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
    assert len(dt_str := atu.current_timestamp()) >= \
        len("2023-10-01T12:00:00"), \
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

    #Test with invalid type of input
    with pytest.raises(TypeError):
        atu.iso_date((2025, 3, 20,10, 30, 0))  # tuple
        atu.iso_date([2025, 3, 20,10, 30, 0])  # tuple
        atu.iso_date(2500.56) # float
#endregion

#region test_validate_iso_date_string()
def test_validate_iso_date_string():
    valid_iso_date = "2025-01-20T13:00:00"
    invalid_iso_date = "invalid-date-format"
    assert atu.validate_iso_date_string(valid_iso_date), \
        f"Valid ISO date '{valid_iso_date}' failed validation"
    with pytest.raises(ValueError):
        atu.validate_iso_date_string(invalid_iso_date)
    # Test with invalid type of input
    with pytest.raises(TypeError) : atu.validate_iso_date_string(None)
    with pytest.raises(TypeError) : atu.validate_iso_date_string("")
    with pytest.raises(TypeError) : atu.validate_iso_date_string(12345)
    with pytest.raises(TypeError) : atu.validate_iso_date_string((1,2,3,4,5))
    with pytest.raises(TypeError) : atu.validate_iso_date_string([1,2,3,4,5])
#endregion

#region test_now_iso_date()
def test_now_iso_date():
    """Test the now_iso_date function."""
    now = atu.now_iso_date()
    assert atu.confirm_iso_date(atu.now_iso_date()), \
        "now_iso_date() returned an invalid internal ISO Date object"
    # Allow for a small delay in the test
    # to ensure the current time is after the recorded 'now'
    assert atu.now_iso_date() >= now, "now_iso_date does not return current datetime"
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

    # Test with invalid Types
    with pytest.raises(TypeError):
        atu.iso_date_approx(dt1, dt2, tolerance="invalid")
    with pytest.raises(TypeError):
        atu.iso_date_approx(1.0, dt2, tolerance="invalid")
    with pytest.raises(TypeError):
        atu.iso_date_approx(2.0, dt2, tolerance="invalid")

    # Test with invalid date strings
    with pytest.raises(ValueError):
        atu.iso_date_approx("invalid-date-string", dt2)
    with pytest.raises(ValueError):
        atu.iso_date_approx(dt1, "invalid-date-string")
#endregion test_iso_date_approx()

#region test_to_int()
def test_to_int():
    assert atu.to_int(1.0) == 1, "to_int(1.0) does not return 1"
    assert atu.to_int(1.5) == 2, "to_int(1.5) does not return 2" 
    assert atu.to_int(1) == 1, "to_int(1) does not return 1"
    assert atu.to_int("1") == 1, "to_int(\"1\") does not return 1"
    with pytest.raises(ValueError):
        atu.to_int("1.8"), "to_int(\"1.8\") does not raise ValueError"
    with pytest.raises(ValueError):
        atu.to_int("quark"), "to_int(\"quark\") does not raise ValueError"
#endregion test_to_int()

#region test_to_float()
def test_to_float():
    assert atu.to_float(1) == 1.0, "to_float(1) does not return 1.0"
    assert atu.to_float("1.5") == 1.5, "to_float(\"1.5\") does not return 1.5" 
    assert atu.to_float("1") == 1.0, "to_float(\"1\") does not return 1.0"
    with pytest.raises(ValueError):
        atu.to_float("quark")
#endregion test_to_float()
#endregion ISO Date Utilities

#region Timestamp Helper Functions

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

    # Test invalid start time string value, not valid ISO value
    excmsg = "Invalid ISO datetime str value:"
    with pytest.raises(ValueError, match=excmsg) as excinfo:
        atu.validate_start(invalid_start)

    # Test invalid input type None start time, expect validate_start() to 
    # return now(), so the comparison should be within 2 seconcds.
    assert atu.iso_date_approx(atu.validate_start(None), \
                               atu.now_iso_date_string(), 2)

    # Test invalid input type "" start time, expect validate_start() to 
    # return now(), so the comparison should be within 2 seconcds.
    assert atu.iso_date_approx(atu.validate_start(""), \
                               atu.now_iso_date_string(), 2)

    # Test invalid input type tuple as start time
    excmsg = "Invalid type for strt input value:"
    with pytest.raises(TypeError,match=excmsg):
        atu.validate_start((1,2))
#endregion

#region test_validate_stop()
def test_validate_stop():
    # Assuming validate_stop is a static method of ActivityEntry class
    valid_start : str = atu.default_start_time() 
    valid_stop : str = atu.default_stop_time(valid_start)
    invalid_time = "invalid-date-format"

    # Test valid stop time 
    assert atu.validate_stop(valid_start, valid_stop) == valid_stop, \
        f"Valid stop time: '{valid_stop}' failed validation"

    # Test invalid stop time with invalid ISO format string value
    with pytest.raises(ValueError):
        atu.validate_stop(valid_start, invalid_time)
    # Test invalid start time with invalid ISO format string value
    with pytest.raises(ValueError):
        atu.validate_stop(invalid_time, valid_stop)

    # Test invalid input type None stop time
    # Expect validate_stop() to return default_stop_time()
    assert atu.validate_stop(valid_start, None), \
        "stop time of None failed validation"
    # Test invalid input type None start time
    # Expect validate_stop() to return default_stop_time()
    assert atu.validate_stop(None, valid_stop), \
        "start time of None failed validation"

    # Test invalid input type "" stop time
    # Expect validate_stop() to return default_stop_time()
    assert atu.validate_stop(valid_start, ""), \
        "stop time of \"\" failed validation"
    # Test invalid input type """ start time
    # Expect validate_stop() to return default_stop_time()
    assert atu.validate_stop("", valid_stop), \
        "start time of \"\" failed validation"

    # Test invalid input type tuple stop time
    with pytest.raises(TypeError):
        atu.validate_stop(valid_start, (1,2))
    # Test invalid input type tuple start time
    with pytest.raises(TypeError):
        atu.validate_stop((1,2), valid_stop)
#endregion

#region test_increase_time()
def test_increase_time():
    """Test the increase_time function."""
    # Initially generated by GitHub Copilot, but took some work to complete

    # Test valid increase by hours
    initial_time = "2025-01-20T13:00:00"
    expected_time = "2025-01-20T14:00:00"
    assert atu.increase_time(tval=initial_time, hours=1) == expected_time, \
        f"Expected {expected_time} but got {atu.increase_time(tval=initial_time, hours=1)}"

    # Test increase by minutes
    expected_time = "2025-01-20T13:30:00"
    assert atu.increase_time(tval=initial_time, minutes=30) == expected_time, \
        f"Expected {expected_time} but got {atu.increase_time(tval=initial_time, minutes=30)}"

    # Test increase by seconds
    expected_time = "2025-01-20T13:00:30"
    assert atu.increase_time(tval=initial_time, seconds=30) == expected_time, \
        f"Expected {expected_time} but got {atu.increase_time(tval=initial_time, seconds=30)}"

    # Test invalid time format
    invalid_time = "invalid-time-format"
    with pytest.raises(ValueError):
        atu.increase_time(tval=invalid_time, hours=1)

    # Test invalid time type
    invalid_time = None
    with pytest.raises(TypeError):
        atu.increase_time(tval=invalid_time, hours=1)

    # Test invalid time type
    invalid_time = (2,3,4)
    with pytest.raises(TypeError):
        atu.increase_time(tval=invalid_time, hours=1)

    # Test invalid time format value
    invalid_time = ""
    with pytest.raises(TypeError):
        atu.increase_time(tval=invalid_time, hours=1)

    # Test invalid increase format
    invalid_increase = "invalid-increase-format"
    with pytest.raises(TypeError):
        atu.increase_time(tval=initial_time, hours=invalid_increase)

    # Test increase by negative time
    expected_time = "2025-01-20T12:00:00"
    assert atu.increase_time(tval=initial_time, hours=-1) == expected_time, \
        f"Expected {expected_time} but got {atu.increase_time(tval=initial_time, hours=-1)}"

    # Test increase by zero time
    expected_time = initial_time
    assert atu.increase_time(tval=initial_time, hours=0, minutes=0, seconds=0) == expected_time, \
        f"Expected {expected_time} but got {atu.increase_time(tval=initial_time, hours=0, minutes=0, seconds=0)}"

    # Test increase crossing over to next day
    initial_time = "2025-01-20T23:30:00"
    expected_time = "2025-01-21T00:30:00"
    assert atu.increase_time(tval=initial_time, hours=1) == expected_time, \
        f"Expected {expected_time} but got {atu.increase_time(tval=initial_time, hours=1)}"

    # Test increase crossing over to next month
    initial_time = "2025-01-31T23:30:00"
    expected_time = "2025-02-01T00:30:00"
    assert atu.increase_time(tval=initial_time, hours=1) == expected_time, \
        f"Expected {expected_time} but got {atu.increase_time(tval=initial_time, hours=1)}"

    # Test increase crossing over to next year
    initial_time = "2025-12-31T23:30:00"
    expected_time = "2026-12-31T23:30:00"
    yearhours = 24 * 365
    assert atu.increase_time(tval=initial_time, hours=yearhours) == expected_time, \
        f"Expected {expected_time} but got {atu.increase_time(tval=initial_time, hours=1)}"
#endregion test_increase_time()

#region test_decrease_time()
def test_decrease_time():
    """Test the increase_time function."""
    # Initially generated by GitHub Copilot, but took some work to complete

    # Test valid decrease by hours
    initial_time = "2025-01-20T13:00:00"
    expected_time = "2025-01-20T12:00:00"
    assert atu.decrease_time(tval=initial_time, hours=1) == expected_time, \
        f"Expected {expected_time} but got {atu.decrease_time(tval=initial_time, hours=1)}"

    # Test decrease by minutes
    expected_time = "2025-01-20T12:30:00"
    assert atu.decrease_time(tval=initial_time, minutes=30) == expected_time, \
        f"Expected {expected_time} but got {atu.decrease_time(tval=initial_time, minutes=30)}"

    # Test decrease by seconds
    expected_time = "2025-01-20T12:59:30"
    assert atu.decrease_time(tval=initial_time, seconds=30) == expected_time, \
        f"Expected {expected_time} but got {atu.decrease_time(tval=initial_time, seconds=30)}"

    # Test invalid time format
    invalid_time = "invalid-time-format"
    with pytest.raises(ValueError):
        atu.decrease_time(tval=invalid_time, hours=1)

    # Test invalid time type
    invalid_time = None
    with pytest.raises(TypeError):
        atu.decrease_time(tval=invalid_time, hours=1)

    # Test invalid time type
    invalid_time = (2,3,4)
    with pytest.raises(TypeError):
        atu.decrease_time(tval=invalid_time, hours=1)

    # Test invalid time format value
    invalid_time = ""
    with pytest.raises(TypeError):
        atu.decrease_time(tval=invalid_time, hours=1)

    # Test invalid decrease format
    invalid_increase = "invalid-increase-format"
    with pytest.raises(TypeError):
        atu.decrease_time(tval=initial_time, hours=invalid_increase)

    # Test decrease by negative time
    expected_time = "2025-01-20T12:00:00"
    assert atu.decrease_time(tval=initial_time, hours=-1) == expected_time, \
        f"Expected {expected_time} but got {atu.decrease_time(tval=initial_time, hours=-1)}"

    # Test decrease by zero time
    expected_time = initial_time
    assert atu.decrease_time(tval=initial_time, hours=0, minutes=0, seconds=0) == expected_time, \
        f"Expected {expected_time} but got {atu.decrease_time(tval=initial_time, hours=0, minutes=0, seconds=0)}"

    # Test decrease crossing over to next day
    initial_time = "2025-01-20T00:30:00"
    expected_time = "2025-01-19T23:30:00"
    assert atu.decrease_time(tval=initial_time, hours=1) == expected_time, \
        f"Expected {expected_time} but got {atu.decrease_time(tval=initial_time, hours=1)}"

    # Test decrease crossing over to next month
    initial_time = "2025-02-01T00:30:00"
    expected_time = "2025-01-31T23:30:00"
    assert atu.decrease_time(tval=initial_time, hours=1) == expected_time, \
        f"Expected {expected_time} but got {atu.decrease_time(tval=initial_time, hours=1)}"

    # Test decrease crossing over to next year
    # TODO: Handle leap year offset
    initial_time = "2026-01-01T23:30:00"
    expected_time = "2025-01-01T23:30:00"
    yearhours = 24 * 365
    assert atu.decrease_time(tval=initial_time, hours=yearhours) == expected_time, \
        f"Expected {expected_time} but got {atu.decrease_time(tval=initial_time, hours=1)}"
#endregion test_decrease_time()

#region test_calculate_duration()
#endregion test_calculate_duration()

#region test_default_duration()
#endregion test_default_duration()

#region test_default_start_time()
#endregion test_default_start_time()

#region test_default_stop_time()
#endregion test_default_stop_time()

#region test_current_timestamp()
#endregion test_current_timestamp()

#endregion Timestamp Helper Functions

