#-----------------------------------------------------------------------------+
import datetime, pytest, json
from typing import List
import at_utilities.at_utils as atu
from model.ae import ActivityEntry

def test_activity_entry_constructor():
    start_time_parm = "2025-01-20T13:00:00"
    stop_time_parm = "2025-01-20T14:05:00"
    activity = "learning"
    notes = "Place notes here"

    te = ActivityEntry(start=start_time_parm, stop=stop_time_parm, \
                       activity=activity, notes=notes)
    start_time_dt = atu.iso_date(start_time_parm)
    stop_time_dt = atu.iso_date(stop_time_parm)
    start_datetime = atu.iso_date(te.start)
    stop_datetime = atu.iso_date(te.stop)
    assert start_datetime == start_time_dt, \
           f"Start time is not correct: {start_datetime} vs {start_time_dt}"
    assert stop_datetime >= stop_time_dt, \
           f"Stop time is not correct: {stop_datetime} vs {stop_time_dt}"
    assert te.activity == activity
    assert te.notes == notes
    assert te.duration == \
        ActivityEntry.calculate_duration(start_time_parm, stop_time_parm), \
        f"Duration is not correct as: {str(te.duration)}"

def test_activity_entry_constructor_with_empty_string_start_in_future():
    ''' Test empty string start time, default to now, with stop time in the future'''
    start_time_parm = ""
    # use stop time default_duration() minutes in the future
    stop_time_dt = datetime.datetime.now() + ActivityEntry.default_duration()
    stop_time_parm = stop_time_dt.isoformat() # 30 minutes in the future
    activity = "learning"
    notes = "Place notes here"

    te = ActivityEntry(start=start_time_parm, stop=stop_time_parm, \
                       activity=activity, notes=notes)

    # Expect positive duration, start is now, stop is 30 minutes later
    assert te.duration >= 0.0, \
        f"Duration is not correct as: te.duration({str(te.duration)})"

def test_activity_entry_constructor_with_empty_string_start_in_past():
    ''' Test empty string start time, default to now, with stop time in the past'''
    start_time_parm = ""
    # use stop time default_duration() minutes in the past
    stop_time_dt = datetime.datetime.now() - ActivityEntry.default_duration()
    stop_time_parm = stop_time_dt.isoformat() # 30 minutes in the future
    activity = "learning"
    notes = "Place notes here"

    te = ActivityEntry(start=start_time_parm, stop=stop_time_parm, \
                       activity=activity, notes=notes)

    # Expect negative duration, start is now, stop is 30 minutes in past
    assert te.duration <= 0.0, \
        f"Duration is not correct as: te.duration({str(te.duration)})"

def test_activity_entry_constructor_with_empty_string_stop_in_past():
    ''' Test empty string as stop time'''
    # use start time 30 minutes in the future
    # Expect constructor to set stop time to start time plus default_duration() minutes
    default_duration = ActivityEntry.default_duration_hours()
    start_time_dt = datetime.datetime.now() + ActivityEntry.default_duration()
    start_time_parm = start_time_dt.isoformat() # 30 minutes in the future
    # empty string for stop time, should be set to start time plus default_duration() minutes
    stop_time_parm = "" 
    activity = "learning"
    notes = "Place notes here"

    te = ActivityEntry(start=start_time_parm, stop=stop_time_parm, \
                       activity=activity, notes=notes)

    # Expect negpositive duration, stop is start + default_duration
    assert te.duration >= 0.0, \
        f"Duration is not correct as: te.duration({str(te.duration)})"
    assert te.duration == ActivityEntry.default_duration_hours(), \
        f"Duration is not correct as: te.duration({str(te.duration)})"


def test_activity_entry_constructor_with_invalid_iso_string_start():
    # Test invalid ISO format for start time
    start_time = "invalid-date-format"
    stop_time = datetime.datetime(2025, 1, 20, 14, 5)
    activity = "learning"
    notes = "Place notes here"
    duration = 0.0

    with pytest.raises(ValueError):
        ActivityEntry(start=start_time, stop=stop_time, activity=activity, notes=notes)

    # Test invalid ISO format for stop time
    start_time = datetime.datetime(2025, 1, 20, 14, 5)
    stop_time = "invalid-date-format"

    with pytest.raises(ValueError):
        ActivityEntry(start=start_time, stop=stop_time, activity=activity, notes=notes)

def test_activity_entry_default_constructor():
    te = ActivityEntry()

    assert isinstance(te.start, datetime.datetime), "Start time is not a datetime object"
    assert isinstance(te.stop, datetime.datetime), "Stop time is not a datetime object"
    assert te.activity == '', "Default activity is not empty"
    assert te.notes == '', "Default notes are not empty"
    #assert te.duration == te.default_duration(), "Default duration is not correct"

def test_validate_start():
    # Assuming validate_start is a static method of ActivityEntry class
    valid_start = "2025-01-20T13:00:00"
    invalid_start = "invalid-date-format"

    # Test valid start time
    assert ActivityEntry.validate_start(valid_start) == datetime.datetime.fromisoformat(valid_start), "Valid start time failed validation"

    # Test invalid start time
    with pytest.raises(ValueError):
        ActivityEntry.validate_start(invalid_start)

    # Test invalid start time
    with pytest.raises(ValueError):
        ActivityEntry.validate_start((1,2))

def test_validate_stop():
    # Assuming validate_stop is a static method of ActivityEntry class
    valid_start = datetime.datetime.fromisoformat("2025-01-20T14:00:00")
    valid_stop = "2025-01-20T14:30:00"
    invalid_stop = "invalid-date-format"

    # Test valid stop time
    assert ActivityEntry.validate_stop(valid_start, valid_stop) == datetime.datetime.fromisoformat(valid_stop), "Valid stop time failed validation"

    # Test invalid stop time
    with pytest.raises(ValueError):
        ActivityEntry.validate_stop(valid_start, invalid_stop)

    # Test invalid stop time
    with pytest.raises(ValueError):
        ActivityEntry.validate_stop(valid_start, (1,2))

def test_activity_entry_constructor_with_none_start():
    stop_time = datetime.datetime(2025, 1, 20, 14, 5)
    activity = "Testing None start time"
    notes = "Testing"

    te = ActivityEntry(start=None, stop=stop_time, activity=activity, notes=notes)

    assert isinstance(te.start, datetime.datetime), "Start time is not a datetime object"
    assert te.stop == stop_time, "Stop time is not correct"
    assert te.activity == activity, "Activity string is not correct"
    assert te.notes == notes, "Notes string is not correct"
    assert te.duration == te.stop - te.start, "Duration is not correct"

def test_activity_entry_constructor_with_none_stop():
    start_time = datetime.datetime(2025, 1, 20, 14, 5)
    activity = "Testing None stop time"
    notes = "Testing"

    te = ActivityEntry(start=start_time, stop=None, activity=activity, notes=notes)

    assert te.start == start_time, "Start time is not correct"
    assert isinstance(te.stop, datetime.datetime), "Stop time is not a datetime object"
    assert te.stop == start_time + datetime.timedelta(minutes=30), "Stop time is not 30 minutes after start time"
    assert te.activity == activity, "Activity string is not correct"
    assert te.notes == notes, "Notes string is not correct"
    assert te.duration == te.stop - te.start, "Duration is not correct"

def test_activity_entry_constructor_with_negative_duration():
    start_time = datetime.datetime(2025, 1, 20, 14, 5)
    stop_time = datetime.datetime(2025, 1, 20, 13, 5)
    activity = "Testing negative duration"
    notes = "Testing"

    te = ActivityEntry(start=start_time, stop=stop_time, activity=activity, notes=notes)

    assert te.start == start_time, "Start time is not correct"
    assert te.stop == stop_time, "Stop time is not correct"
    assert te.activity == activity, "Activity string is not correct"
    assert te.notes == notes, "Notes string is not correct"
    assert te.duration == te.stop - te.start, "Duration is not correct"
    assert te.duration.total_seconds() < 0, "Duration is not negative"

def test_activity_entry_constructor_with_default_values():
    te = ActivityEntry()

    assert isinstance(te.start, datetime.datetime), "Start time is not a datetime object"
    assert isinstance(te.stop, datetime.datetime), "Stop time is not a datetime object"
    assert te.activity == '', "Default activity is not empty"
    assert te.notes == '', "Default notes are not empty"
    #assert te.duration == te.default_duration(), "Default duration is not correct"

def test_activity_entry_constructor_with_partial_parameters():
    start_time = datetime.datetime(2025, 1, 20, 13)
    activity = "Partial parameters"
    te = ActivityEntry(start=start_time, activity=activity)

    assert te.start == start_time, "Start time is not correct"
    assert isinstance(te.stop, datetime.datetime), "Stop time is not a datetime object"
    assert te.activity == activity, "Activity string is not correct"
    assert te.notes == '', "Notes string is not empty"
    assert te.duration == te.stop - te.start, "Duration is not correct"

def test_activity_entry_str():
    start_time = datetime.datetime(2025, 1, 20, 13)
    activity = "Partial parameters"
    te = ActivityEntry(start=start_time, activity=activity)

    assert str(te) == activity, "String representation of ActivityEntry is not correct"

# def test_activity_entry_constructor_with_string_start():
#     start_time_param = "2025-01-20T13:00:00"
#     stop_time_param = "2025-01-20T14:05:00"
#     activity = "learning"
#     notes = "Testing ISO string input for start time"

#     te = ActivityEntry(start=start_time_param, stop=stop_time_param, \
#                        activity=activity, notes=notes)

#     assert te.start == datetime.datetime.fromisoformat(start_time), f"Start time is not correct ISO conversion: {start_time} vs {te.start}"
#     assert te.stop == stop_time, "Stop time is not correct"
#     assert te.stop >= te.start, "Stop time is before start time"
#     assert te.activity == activity, "Activity string is not correct"
#     assert te.notes == notes, "Notes string is not correct"

# def test_activity_entry_constructor_with_string_stop():
#     start_time = datetime.datetime(2025, 1, 20, 13, 5)
#     stop_time = "2025-01-20T14:00:00"
#     activity = "learning"
#     notes = "Testing ISO string input for stop time"

#     te = ActivityEntry(start=start_time, stop=stop_time, activity=activity, notes=notes)

#     assert te.start == start_time, "Start time is not correct"
#     assert te.stop == datetime.datetime.fromisoformat(stop_time), f"Stop time is not correct ISO conversion: {stop_time} vs {te.stop}"
#     assert te.activity == activity, "Activity string is not correct"
#     assert te.notes == notes, "Notes string is not correct"
#     assert te.duration == te.stop - te.start, "Duration is not correct"


