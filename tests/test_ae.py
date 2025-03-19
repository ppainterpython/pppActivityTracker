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
        start_time_parm = atu.default_start_time() 
        stop_time_parm = atu.default_stop_time(start_time_parm)
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
        atu.calculate_duration(start_time_parm, stop_time_parm), \
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
        stop_time_parm = atu.default_stop_time(None)
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
        stop_time_dt = atu.iso_date_now() - atu.default_duration()
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
        stop_time_dt = atu.iso_date_now() + atu.default_duration()
        stop_time_parm = stop_time_dt.isoformat() # 30 minutes in the future
        activity = "learning"
        notes = "Place notes here"
    except Exception as e:
        pytest.fail(f"Setup failed for None start with stop in future: {e}")

    te = ActivityEntry(start=None, stop=stop_time_parm, activity=activity, notes=notes)

    # Expect positive duration, start is before stop by default_duration() minutes
    assert te.duration >= 0.0, \
        f"Duration is not correct as: te.duration({str(te.duration)})"
    assert te.duration == approx(atu.default_duration_hours(),rel=0.001), \
        f"Duration is not correct as: te.duration({str(te.duration)})"
    del te
    #endregion

    #region Test empty string for start time, expect conversion to default of now()
    try:
        # use stop time default_duration() minutes in the future from now
        stop_time_dt = atu.iso_date_now() - atu.default_duration()
        stop_time_parm = stop_time_dt.isoformat() # 30 minutes in the future
        activity = "learning"
        notes = "Place notes here"
    except Exception as e:
        pytest.fail(f"Setup failed for None start with stop in future: {e}")

    te = ActivityEntry(start="", stop=stop_time_parm, activity=activity, notes=notes)

    # Expect negative duration, start is after stop by default_duration() minutes
    assert te.duration <= 0.0, \
        f"Duration is not correct as: te.duration({str(te.duration)})"
    assert abs(te.duration) == approx(atu.default_duration_hours(),rel=0.001), \
        f"Duration is not correct as: te.duration({str(te.duration)})"
    del te
    #endregion
#endregion

#region test_activity_entry_constructor_with_invalid_iso_string_start()
def test_activity_entry_constructor_with_invalid_iso_string_start():
    # Test invalid ISO format for start time
    start_time = "invalid-date-format"
    stop_time = atu.default_stop_time()  # Use default stop time
    activity = "learning"
    notes = "Place notes here"

    with pytest.raises(ValueError):
        ActivityEntry(start=start_time, stop=stop_time, activity=activity, notes=notes)

    # Test invalid ISO format for stop time
    start_time = atu.default_start_time()  # Use default start time
    stop_time = "invalid-date-format"

    with pytest.raises(ValueError):
        ActivityEntry(start=start_time, stop=stop_time, activity=activity, notes=notes)
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
    start_time = atu.default_start_time()
    activity = "Partial parameters"
    te = ActivityEntry(start=start_time, activity=activity)

    assert te.start == start_time, "Start time is not correct"
    assert atu.validate_iso_date_string(te.stop), \
        "Stop time is not a valid ISO date string"
    assert te.activity == activity, "Activity string is not correct"
    assert te.notes == '', "Notes string is not empty"
    assert te.duration == atu.calculate_duration(te.start, te.stop), \
        "Duration is not correct"
#endregion

