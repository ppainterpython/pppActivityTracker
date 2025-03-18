#-----------------------------------------------------------------------------+
import datetime, pytest, json
from typing import List
from pytest import approx
import at_utilities.at_utils as atu
from model.ae import ActivityEntry

#region test_activity_entry_constructor()
def test_activity_entry_constructor():
    """Basic test for ActivityEntry object with valid input values"""
    try:
        start_time_parm = ActivityEntry.default_start_time() 
        stop_time_parm = ActivityEntry.default_stop_time(start_time_parm)
        activity = "learning"
        notes = "Place notes here"
    except:
        pytest.fail("Setup failed for start and stop time parameters")
    te : ActivityEntry = ActivityEntry(start=start_time_parm, stop=stop_time_parm, \
                       activity=activity, notes=notes)
    # Expect the input dates to match the created dates
    assert atu.iso_date_approx(te.start, start_time_parm,2), \
           f"Start time is not correct: {te.start} vs {start_time_parm}"
    assert atu.iso_date_approx(te.stop,stop_time_parm,2), \
           f"Stop time is not correct: {te.stop} vs {stop_time_parm}"
    assert te.activity == activity
    assert te.notes == notes
    assert te.duration == \
        ActivityEntry.calculate_duration(start_time_parm, stop_time_parm), \
        f"Duration is not correct as: {str(te.duration)}"
    # Verify the __str__() method returns the activity string
    assert str(te) == activity, \
        f"String representation of ActivityEntry is not correct: {str(te)}"
#endregion

#region test_activity_entry_constructor_recoverable_input_value_variety()
def test_activity_entry_constructor_recoverable_input_value_variety():
    ''' Test other edge cases for ActivityEntry() input values'''

    #region Test empty string for start time, expect conversion to default of now()
    try:
        # set stop time to now() plus default_duration() minutes
        stop_time_parm = ActivityEntry.default_stop_time(None)
        stop_time_dt = atu.iso_date(stop_time_parm)
        activity = "learning"
        notes = "Place notes here"
    except Exception as e:
        pytest.fail(f"Setup failed for empty string start with stop in future: {e}")

    te = ActivityEntry(start="", stop=stop_time_parm, \
                       activity=activity, notes=notes)

    # Expect positive duration, start is now, stop is 30 minutes later
    assert te.duration >= 0.0, \
        f"Incorrect duration for stop time in future: te.duration({str(te.duration)})"
    del te
    #endregion

    #region Test empty string for start time, expect conversion to default of now()
    try:
        # use stop time default_duration() minutes in the past from now
        stop_time_dt = atu.iso_date_now() - ActivityEntry.default_duration()
        stop_time_parm = stop_time_dt.isoformat() # 30 minutes in the future
        activity = "learning"
        notes = "Place notes here"
    except Exception as e:
        pytest.fail(f"Setup failed for empty string start with stop in past: {e}")

    te = ActivityEntry(start="", stop=stop_time_parm, \
                       activity=activity, notes=notes)

    # Expect negative duration, start is now(), stop is defaul_duration() minutes later
    assert te.duration <= 0.0, \
        f"Incorrect duration for stop time in past: te.duration({str(te.duration)})"
    del te
    #endregion

    #region Test None for start time, expect conversion to default of now()
    try:
        # use stop time default_duration() minutes in the future from now
        stop_time_dt = atu.iso_date_now() + ActivityEntry.default_duration()
        stop_time_parm = stop_time_dt.isoformat() # 30 minutes in the future
        activity = "learning"
        notes = "Place notes here"
    except Exception as e:
        pytest.fail(f"Setup failed for None start with stop in future: {e}")

    te = ActivityEntry(start=None, stop=stop_time_parm, activity=activity, notes=notes)

    # Expect positive duration, start is before stop by default_duration() minutes
    assert te.duration >= 0.0, \
        f"Duration is not correct as: te.duration({str(te.duration)})"
    assert te.duration == approx(ActivityEntry.default_duration_hours(),rel=0.001), \
        f"Duration is not correct as: te.duration({str(te.duration)})"
    del te
    #endregion

    #region Test empty string for start time, expect conversion to default of now()
    try:
        # use stop time default_duration() minutes in the future from now
        stop_time_dt = atu.iso_date_now() - ActivityEntry.default_duration()
        stop_time_parm = stop_time_dt.isoformat() # 30 minutes in the future
        activity = "learning"
        notes = "Place notes here"
    except Exception as e:
        pytest.fail(f"Setup failed for None start with stop in future: {e}")

    te = ActivityEntry(start="", stop=stop_time_parm, activity=activity, notes=notes)

    # Expect negative duration, start is after stop by default_duration() minutes
    assert te.duration <= 0.0, \
        f"Duration is not correct as: te.duration({str(te.duration)})"
    assert abs(te.duration) == approx(ActivityEntry.default_duration_hours(),rel=0.001), \
        f"Duration is not correct as: te.duration({str(te.duration)})"
    del te
    #endregion
#endregion

#region test_activity_entry_constructor_with_invalid_iso_string_start()
def test_activity_entry_constructor_with_invalid_iso_string_start():
    # Test invalid ISO format for start time
    start_time = "invalid-date-format"
    stop_time = ActivityEntry.default_stop_time()  # Use default stop time
    activity = "learning"
    notes = "Place notes here"

    with pytest.raises(ValueError):
        ActivityEntry(start=start_time, stop=stop_time, activity=activity, notes=notes)

    # Test invalid ISO format for stop time
    start_time = ActivityEntry.default_start_time()  # Use default start time
    stop_time = "invalid-date-format"

    with pytest.raises(ValueError):
        ActivityEntry(start=start_time, stop=stop_time, activity=activity, notes=notes)
#endregion

#region test_validate_start()
def test_validate_start():
    """Test None, "", invalid ISO, and tuple as input to AE.validate_start()"""
    # Assuming validate_start is a static method of ActivityEntry class
    try:
        valid_start = ActivityEntry.default_start_time()
        invalid_start = "invalid-date-format"
    except:
        pytest.fail("Setup failed for valid|invalid start time parameters")

    # Test valid start time
    assert ActivityEntry.validate_start(valid_start) == valid_start

    # Test empty string for start time, expect conversion to default of now()

    # Test invalid start time string value, not valid ISO value
    with pytest.raises(ValueError):
        ActivityEntry.validate_start(invalid_start)

    # Test invalid input type None start time, expect validate_start() to 
    # return now(), so the comparison should be within 2 seconcds.
    assert atu.iso_date_approx(ActivityEntry.validate_start(None), atu.iso_date_now_string(), 2)

    # Test invalid input type tuple start time
    with pytest.raises(TypeError):
        ActivityEntry.validate_start((1,2))
#endregion

#region test_validate_stop()
def test_validate_stop():
    # Assuming validate_stop is a static method of ActivityEntry class
    valid_start = ActivityEntry.default_start_time() 
    valid_stop = ActivityEntry.default_stop_time(valid_start)
    invalid_stop = "invalid-date-format"

    # Test valid stop time 
    assert ActivityEntry.validate_stop(valid_start, valid_stop) == valid_stop, \
        "Valid stop time failed validation"

    # Test invalid stop time string value
    with pytest.raises(ValueError):
        ActivityEntry.validate_stop(valid_start, invalid_stop)

    # Test invalid input type None stop time
    # Expect validate_stop() to return default_stop_time()
    assert ActivityEntry.validate_stop(valid_start, None), "stop time of None failed validation"

    # Test invalid input type tuple stop time
    with pytest.raises(TypeError):
        ActivityEntry.validate_stop(valid_start, (1,2))
#endregion

#region test_activity_entry_constructor_with_default_values()
def test_activity_entry_constructor_with_default_values():
    te = ActivityEntry()

    assert isinstance(te.start, str), "Start time is not a type: str"
    assert isinstance(te.stop, str), "Stop time is not a type: str"
    assert te.activity == '', "Default activity is not empty"
    assert te.notes == '', "Default notes are not empty"
#endregion

#region test_activity_entry_constructor_with_partial_parameters()
def test_activity_entry_constructor_with_partial_parameters():
    start_time = ActivityEntry.default_start_time()
    activity = "Partial parameters"
    te = ActivityEntry(start=start_time, activity=activity)

    assert te.start == start_time, "Start time is not correct"
    assert ActivityEntry.validate_iso_date_string(te.stop), \
        "Stop time is not a valid ISO date string"
    assert te.activity == activity, "Activity string is not correct"
    assert te.notes == '', "Notes string is not empty"
    assert te.duration == ActivityEntry.calculate_duration(te.start, te.stop), \
        "Duration is not correct"
#endregion

#region test_validate_iso_date_string()
def test_validate_iso_date_string():
    valid_iso_date = "2025-01-20T13:00:00"
    invalid_iso_date = "invalid-date-format"
    assert ActivityEntry.validate_iso_date_string(valid_iso_date) == True, \
        "Valid ISO date string failed validation"
    with pytest.raises(ValueError):
        ActivityEntry.validate_iso_date_string(invalid_iso_date)
#endregion

