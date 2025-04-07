#-----------------------------------------------------------------------------+
import pytest, os, threading, re, logging
from typing import List
from atconstants import *
import at_utilities.at_utils as atu
from at_logging.at_logging import atlogging_setup
# Setup logging for AT compaitble with pytest and other modules
logger = atlogging_setup(AT_APP_NAME)
if logger is None:
    logger = logging.getLogger(AT_APP_NAME)  # fallback to default logger if setup failed
    if logger is None:
        logger = logging.getLogger()  # fallback to the root logger if all else fails
if logger is not None:
    logger.debug(f"Imported module: {__name__}")
    logger.debug(f" Logging initialized.")

#------------------------------------------------------------------------------+
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
    with pytest.raises(ValueError) : atu.validate_iso_date_string("")
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
#------------------------------------------------------------------------------+

#------------------------------------------------------------------------------+
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
    with pytest.raises(ValueError):
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
    with pytest.raises(ValueError):
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
def test_calculate_duration():
    """Test the calculate_duration function."""
    start = "2023-10-01T12:00:00"
    stop = "2023-10-01T14:30:00"  # 2 hours and 30 minutes later

    # Test duration in hours
    assert atu.calculate_duration(start, stop, unit="hours") == 2.5, \
        f"Expected 2.5 hours but got {atu.calculate_duration(start, stop, unit='hours')}"

    # Test duration in minutes
    assert atu.calculate_duration(start, stop, unit="minutes") == 150, \
        f"Expected 150 minutes but got {atu.calculate_duration(start, stop, unit='minutes')}"

    # Test duration in seconds
    assert atu.calculate_duration(start, stop, unit="seconds") == 9000, \
        f"Expected 9000 seconds but got {atu.calculate_duration(start, stop, unit='seconds')}"

    # Test with invalid unit
    with pytest.raises(ValueError):
        atu.calculate_duration(start, stop, unit="invalid")

    # Test with stop time before start time
    assert atu.calculate_duration(stop, start, unit="hours") == -2.5, \
        f"Expected -2.5 hours but got {atu.calculate_duration(stop, start, unit='hours')}"

    # Test with None values
    with pytest.raises(TypeError):
        atu.calculate_duration(None, stop)

    # Test with empty strings
    with pytest.raises(ValueError):
        atu.calculate_duration("", "")

    # Test with invalid ISO date strings
    with pytest.raises(ValueError):
        atu.calculate_duration("invalid-date", stop)
    with pytest.raises(ValueError):
        atu.calculate_duration(start, "invalid-date")
#endregion test_calculate_duration()

#region test_default_duration()
def test_default_duration():
    """Test the default_duration function."""
    # Test default duration in hours
    assert atu.default_duration(unit="hours") == 0.5, \
        f"Expected 0.5 hours but got {atu.default_duration(unit='hours')}"

    # Test default duration in minutes
    assert atu.default_duration(unit="minutes") == 30.0, \
        f"Expected 30.0 minutes but got {atu.default_duration(unit='minutes')}"

    # Test default duration in seconds
    assert atu.default_duration(unit="seconds") == 1800.0, \
        f"Expected 1800.0 seconds but got {atu.default_duration(unit='seconds')}"

    # Test with invalid unit
    assert atu.default_duration(unit="invalid") == 0.0, \
        f"Expected 0.0 for invalid unit but got {atu.default_duration(unit='invalid')}"
#endregion test_default_duration()

#region test_default_start_time()
def test_default_start_time():
    """Test the default_start_time function."""
    start_time = atu.default_start_time()
    assert atu.validate_iso_date_string(start_time), \
        f"default_start_time() did not return a valid ISO date string: {start_time}"
    assert atu.iso_date_approx(start_time, atu.now_iso_date_string(), tolerance=2), \
        f"default_start_time() is not approximately equal to the current time"
#endregion test_default_start_time()

#region test_default_stop_time()
def test_default_stop_time():
    """Test the default_stop_time function."""
    start_time = atu.default_start_time()
    stop_time = atu.default_stop_time(start_time)
    
    assert atu.validate_iso_date_string(stop_time), \
        f"default_stop_time() did not return a valid ISO date string: {stop_time}"
    assert atu.iso_date_approx(stop_time, atu.increase_time(start_time, minutes=30), tolerance=2), \
        f"default_stop_time() is not approximately equal to the start time plus default duration"
    
    # Test with None start time
    stop_time = atu.default_stop_time(None)
    assert atu.validate_iso_date_string(stop_time), \
        f"default_stop_time(None) did not return a valid ISO date string: {stop_time}"
    assert atu.iso_date_approx(stop_time, atu.increase_time(atu.now_iso_date_string(), minutes=30), tolerance=2), \
        f"default_stop_time(None) is not approximately equal to the current time plus default duration"
    
    # Test with empty string start time
    stop_time = atu.default_stop_time("")
    assert atu.validate_iso_date_string(stop_time), \
        f"default_stop_time('') did not return a valid ISO date string: {stop_time}"
    assert atu.iso_date_approx(stop_time, atu.increase_time(atu.now_iso_date_string(), minutes=30), tolerance=2), \
        f"default_stop_time('') is not approximately equal to the current time plus default duration"
#endregion test_default_stop_time()

#region test_current_timestamp()
def test_current_timestamp():
    """Test the current_timestamp function."""
    timestamp = atu.current_timestamp()
    assert atu.validate_iso_date_string(timestamp), \
        f"current_timestamp() did not return a valid ISO date string: {timestamp}"
    assert atu.iso_date_approx(timestamp, atu.now_iso_date_string(), tolerance=2), \
        f"current_timestamp() is not approximately equal to the current time"
#endregion test_current_timestamp()

#endregion Timestamp Helper Functions
#------------------------------------------------------------------------------+

#------------------------------------------------------------------------------+
#region parameter validation function tests
#------------------------------------------------------------------------------+
#region test_notempty()
def test_str_notempty():
    """Test the str_notempty function."""
    # Test with valid non-empty string
    assert atu.str_notempty("valid string"), \
        "str_notempty() failed for valid non-empty string"
    
    # Test with empty string
    assert not atu.str_notempty(""), \
        "str_notempty() failed for empty string"

    # Test with None value
    assert not atu.str_notempty(None), \
        "str_notempty() failed for None value"

    # Test with whitespace string
    assert atu.str_notempty("   "), \
        "str_notempty() failed for whitespace string"

    # Test with invalid type (e.g., int, list, dict)
    assert not atu.str_notempty(123), \
        "str_notempty() failed for integer value"
    assert not atu.str_notempty([]), \
        "str_notempty() failed for empty list"
    assert not atu.str_notempty({}), \
        "str_notempty() failed for empty dictionary"
#endregion test_notempty()
#-------------------------------------------
#region test_is_obj_or_none()
def test_is_object_or_none():  
    """Test the is_obj_or_none function."""
    # Test with valid object
    class TestClass:
        pass

    obj = TestClass()
    assert atu.is_object_or_none(obj), \
        "is_obj_or_none() failed for valid name obj_value parameters"

    # Test with valid name value and None obj_value
    assert atu.is_object_or_none(None), \
        "is_obj_or_none() failed for valid name and None obj_value parameters"
    assert atu.is_object_or_none(), \
        "is_obj_or_none() failed for valid name and None obj_value parameters"
    # Test with invalid type (e.g., int, list, dict)
    assert not atu.is_object_or_none(123), \
        "is_obj_or_none() failed for integer value"
    assert atu.is_not_object_or_none(123), \
        "is_obj_or_none() failed for integer value"
    assert not atu.is_object_or_none([]), \
        "is_obj_or_none() failed for empty list"
    assert not atu.is_object_or_none({}), \
        "is_obj_or_none() failed for empty dictionary"
#endregion test_is_obj_or_none()
#-------------------------------------------
#region is_obj_of_type()
def test_is_obj_of_type():
    """Test the is_obj_of_type function."""
    vn = "valid_name"; vs = "valid_string"
    # Test with valid object
    class TestClass:
        pass

    obj = TestClass()
    obj_type = type(obj)
    assert atu.is_obj_of_type(vn,obj,TestClass), \
        "is_obj_of_type() failed for valid object and class parameters"
    assert atu.is_not_obj_of_type(vn,obj,logging.Logger), \
        "is_obj_not_of_type() failed for incorrect object_type parameters"

    # Test with no values
    with pytest.raises(TypeError):
        atu.is_obj_of_type()
    with pytest.raises(TypeError):
        atu.is_obj_of_type(vn)
    with pytest.raises(TypeError):
        atu.is_obj_of_type(vn,obj)
    
    # Test with some None parameters
    assert atu.is_obj_of_type(None,obj,TestClass), \
        "is_not_obj_or_none() failed for None value"
    assert not atu.is_obj_of_type(vn,None,TestClass), \
        "is_not_obj_or_none() failed for None value"

    # Test with invalid type (e.g., int, list, dict)
    assert not atu.is_obj_of_type(123,obj,TestClass), \
        "is_obj_of_type() failed for integer value"
    assert not atu.is_obj_of_type([],obj,TestClass), \
        "is_obj_of_type() failed for empty list"
    assert not atu.is_obj_of_type({},obj,TestClass), \
        "is_obj_of_type() failed for empty dictionary"
    assert not atu.is_obj_of_type(vn,123,TestClass), \
        "is_obj_of_type() failed for empty dictionary"
    assert not atu.is_obj_of_type(vn,obj,123), \
        "is_obj_of_type() failed for empty dictionary"
    
    # Test with invalid type with raise_TypeError=True
    with pytest.raises(TypeError):
        atu.is_obj_of_type(123,123,TestClass,True), \
            "is_obj_of_type() failed for integer name parameter"
    with pytest.raises(TypeError):
        atu.is_obj_of_type(vn,123,TestClass,True), \
            "is_obj_of_type() failed for integer value"
    with pytest.raises(TypeError):
        atu.is_obj_of_type(vn,obj,123,True), \
            "is_obj_of_type() failed for empty dictionary"
    with pytest.raises(TypeError):  
        atu.is_obj_of_type(vn,[],TestClass,True), \
            "is_obj_of_type() failed for empty list"
    with pytest.raises(TypeError):
        atu.is_obj_of_type(vn,obj,[],True), \
            "is_obj_of_type() failed for empty list"
    with pytest.raises(TypeError):
        atu.is_obj_of_type(vn,obj,{},True), \
            "is_obj_of_type() failed for empty dictionary"
    with pytest.raises(TypeError):
        atu.is_obj_of_type(vn,None,TestClass,True), \
            "is_obj_of_type() failed for None obj_value parameter"
    with pytest.raises(TypeError):
        atu.is_obj_of_type(vn,obj,None,True), \
            "is_obj_of_type() failed for None obj_type parameter"
#endregion is_obj_of_type()
#-------------------------------------------
#region test_is_str_or_none()
def test_is_str_or_none():
    """Test the is_str_or_none function."""
    # Test with valid string name and value
    vn = "valid_name"; vs = "valid_string"
    assert atu.is_str_or_none(vn, vs, False), \
        "is_str_or_none() failed for valid string value parameter"
    # Test with no parameters
    assert atu.is_str_or_none(), \
        "is_str_or_none() failed for valid string value parameter"

    # Test with valid string name and None value
    assert atu.is_str_or_none(vn, None, False), \
        "is_str_or_none() failed for None value parameter"

    # Test with valid string name and empty string value
    assert atu.is_str_or_none(vn, ""), \
        "is_str_or_none() failed for empty string value parameter"

    # Test with invalid value type (e.g., int, list, dict)
    with pytest.raises(TypeError):
        atu.is_str_or_none(vn, 123, True), \
            "is_str_or_none() failed for integer value parameter"
    with pytest.raises(TypeError):
        atu.is_str_or_none(123, vs, True), \
            "is_str_or_none() failed for integer name parameter"
    with pytest.raises(TypeError):
        atu.is_str_or_none(123, 123, True), \
            "is_str_or_none() failed for integer name and value parameters"
    assert not atu.is_str_or_none(vn,123), \
        "is_str_or_none() failed for integer value parameter"
    assert atu.is_not_str_or_none(vn,123), \
        "is_str_or_none() failed for integer value parameter"
    with pytest.raises(TypeError):
        atu.is_str_or_none(vn, [], True), \
            "is_str_or_none() failed for list value parameter"
    assert not atu.is_str_or_none(vn, []), \
        "is_str_or_none() failed for empty list value parameter"
    assert atu.is_not_str_or_none(vn,[]), \
        "is_str_or_none() failed for empty list value parameter"
    with pytest.raises(TypeError):
        atu.is_str_or_none(vn, {}, True), \
            "is_str_or_none() failed for dict value parameter"
    assert not atu.is_str_or_none({}), \
        "is_str_or_none() failed for empty dictionary value parameter"
    with pytest.raises(TypeError):
        atu.is_str_or_none(vn, 123, True), \
            "is_str_or_none() failed for integer value parameter"
#endregion test_is_str_or_none()
#-------------------------------------------
#region test_str_or_none()
def test_str_or_none():
    """Test the str_or_none function."""
    # Test with valid string
    assert atu.str_or_none("valid string") == "valid string", \
        "str_or_none() failed for valid string"

    # Test with None value
    assert atu.str_or_none(None) is None, \
        "str_or_none() failed for None value"

    # Test with empty string
    assert atu.str_or_none("") is None, \
        "str_or_none() failed for empty string"

    # Test with invalid type (e.g., int, list, dict)
    assert atu.str_or_none(123) is None, \
        "str_or_none() failed for integer value"
    assert atu.str_or_none([]) is None, \
        "str_or_none() failed for empty list"
    assert atu.str_or_none({}) is None, \
        "str_or_none() failed for empty dictionary"
#endregion test_str_or_none()
#-------------------------------------------
#region test_stop_str_or_default()
def test_stop_str_or_default():
    """Test the stop_str_or_default function."""
    tn = atu.now_iso_date_string()
    defduration = atu.default_duration("minutes")
    validstop = tn
    validstart = atu.decrease_time(validstop, minutes=defduration)
    # Test with valid string
    assert atu.stop_str_or_default(validstop) == validstop, \
        "stop_str_or_default() failed for valid stop timestamp:'{validstop}'"
    # Test with None value
    assert (v := atu.stop_str_or_default(None)) and \
            atu.iso_date_approx(v,tn,120), \
        f"stop_str_or_default(stop=None, start=None " + \
        f"returned incorrect stop='{v}'"
    # Test with "" value
    assert (v := atu.stop_str_or_default("")) and \
            atu.iso_date_approx(v,tn,120), \
        f"stop_str_or_default(stop=\"\", start=None " + \
        f"returned incorrect stop='{v}'"
    assert (v := atu.stop_str_or_default(None, None)) and \
            atu.iso_date_approx(v,tn,120), \
        f"stop_str_or_default(stop=None, start='{validstart}' " + \
        f"returned incorrect stop='{v}'"
    d = (defduration + 3) * 60 # value in seconds
    assert (v := atu.stop_str_or_default(None, validstart)) and \
            atu.iso_date_approx(validstart, validstop,d), \
        f"stop_str_or_default(stop=None, start='{validstart}' " + \
        f"returned incorrect stop='{v}'"
    # Test with invalid ISO date strings
    with pytest.raises(ValueError):
        atu.stop_str_or_default("invalid-date")
    with pytest.raises(ValueError):
        atu.stop_str_or_default(None, "invalid-date")

    # Test with invalid type (e.g., int, list, dict)
    with pytest.raises(TypeError):
        atu.stop_str_or_default(123)
    with pytest.raises(TypeError):
        atu.stop_str_or_default([])
    with pytest.raises(TypeError):
        atu.stop_str_or_default(None, 123)
    with pytest.raises(TypeError):
        atu.stop_str_or_default(None, [])
#endregion test_stop_str_or_default()
#-------------------------------------------
#region test_timestamp_str_or_default()
def test_timestamp_str_or_default():
    """Test the timestamp_str_or_default function."""
    tn = atu.now_iso_date_string()
    # Test with valid string
    assert atu.timestamp_str_or_default(tn) == tn, \
        "timestamp_str_or_default() failed for valid timestamp:'{tn}'"

    # Test with None value, should return now()
    assert (v := atu.timestamp_str_or_default(None)) and \
            atu.iso_date_approx(v, tn, 120), \
        f"timestamp_str_or_default(None) returned incorrect timestamp='{v}'"

    # Test with "" value, should return now()
    assert (v := atu.timestamp_str_or_default("")) and \
            atu.iso_date_approx(v, tn, 120), \
        f"timestamp_str_or_default(\"\") returned incorrect timestamp='{v}'"

    # Test with invalid ISO date strings
    with pytest.raises(ValueError):
        atu.timestamp_str_or_default("invalid-date")

    # Test with invalid type (e.g., int, list, dict)
    assert (v := atu.timestamp_str_or_default(123)) and \
            atu.iso_date_approx(tn, v,2), \
        f"atu.timestamp_str_or_default(123) " + \
        f"returned incorrect timestamp='{v}'"
        
    assert (v := atu.timestamp_str_or_default([])) and \
            atu.iso_date_approx(tn, v,2), \
        f"atu.timestamp_str_or_default([]) " + \
        f"returned incorrect timestamp='{v}'"
        
#endregion test_timestamp_str_or_default()
#-------------------------------------------
#endregion parameter validation function tests
#------------------------------------------------------------------------------+

#------------------------------------------------------------------------------+
#region basic utility functions
#------------------------------------------------------------------------------+
#region test_ptid()
def test_ptid():
    """Test the ptid function to ensure it returns a valid process/thread ID"""
    pid : int = os.getpid()
    tid : int = threading.get_native_id()
    ptid_value = atu.ptid()
    assert isinstance(ptid_value,str), \
        f"ptid() returned type '{type(ptid_value).__name__}' instead of str"
    # Check if the ptid is in the format [pid:tid] where pid and tid are integers
    pattern = r'^\[(\d+):(\d+)\]$' # test for pattern like "[19283:1234]""
    m = re.compile(pattern)
    # Check if the ptid is correct format and expected value
    match = m.match(ptid_value)
    assert match, "ptid() returned incorrect format."
    assert pid == int(match.group(1)), \
        f"ptid() returned pid '{int(match.group(1))}' does not match '{pid}'"
    assert tid == int(match.group(2)), \
        f"ptid() returned tid '{int(match.group(2))}' does not match '{tid}'"
#endregion  

#region test_is_running_in_pytest()
def test_is_running_in_pytest():
    """Test the is_running_in_pytest function"""
    assert atu.is_running_in_pytest(), f"is_running_in_pytest() returned False"
    assert atu.is_running_in_pytest(1), f"is_running_in_pytest() returned False"
    assert atu.is_running_in_pytest(2), f"is_running_in_pytest() returned False"
    assert atu.is_running_in_pytest(3), f"is_running_in_pytest() returned False"
    assert not atu.is_running_in_pytest(4), f"is_running_in_pytest() returned False"
    assert not atu.is_running_in_pytest('not int'), f"is_running_in_pytest() returned False"

#endregion  test_is_running_in_pytest()

#region test_at_env_info()
def test_at_env_info():
    """Test the env_info function."""
    # Test with valid input
    env_info = atu.at_env_info(__name__,logger,True)
    assert isinstance(env_info, tuple), \
        "env_info(__name__,logger,True) should return a tuple"
    assert "pytest" in env_info, \
        "env_info(__name__,logger,True) should contain 'pytest'"
    env_info = atu.at_env_info(__name__, logger, False)
    assert isinstance(env_info, tuple), \
        "env_info(__name__, logger, False) should return a tuple"
    assert "pytest" in env_info, \
        "env_info(__name__, logger, False) should contain 'pytest'"
    env_info = atu.at_env_info(None, logger, False)
    assert isinstance(env_info, tuple), \
        "env_info(None, logger, False) should return a tuple"
    assert "pytest" in env_info, \
        "env_info(None, logger, False) should contain 'pytest'"
    env_info = atu.at_env_info("", logger, False)
    assert isinstance(env_info, tuple), \
        "env_info("", logger, False) should return a tuple"
    assert "pytest" in env_info, \
        "env_info("", logger, False) should contain 'pytest'"

    # Test with invalid input (e.g., None, [], int, dict)
    with pytest.raises(TypeError):
        atu.at_env_info([],logger), \
            f"env_info([], logger) should raise TypeError"
    with pytest.raises(TypeError):
        atu.at_env_info(None,[]), \
            f"env_info(None,[]) should raise TypeError"
    with pytest.raises(TypeError):
        atu.at_env_info(__name__,logger,[]), \
            f"env_info(__name__,logger,[]) should raise TypeError"
    with pytest.raises(TypeError):
        atu.at_env_info(__name__,logger,123), \
            f"env_info(__name__,logger,123) should raise TypeError"
    with pytest.raises(TypeError):
        atu.at_env_info(__name__,logger,"foo"), \
            f"env_info(__name__,logger,\"foo\") should raise TypeError"
    with pytest.raises(TypeError):
        atu.at_env_info(123,123), \
            f"env_info(None,[]) should raise TypeError"
    with pytest.raises(TypeError):
        atu.at_env_info(__name__,123,[]), \
            f"env_info(__name__,logger,[]) should raise TypeError"

#endregion test_at_env_info()

#endregion basic utility functions
#------------------------------------------------------------------------------+
