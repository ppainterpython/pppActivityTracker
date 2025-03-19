#-----------------------------------------------------------------------------+
# at_utils.py
import datetime
#-----------------------------------------------------------------------------+
# Often when working with dates and times, where calculating time interval 
# durations with a start and stop time, the units of the duration value will
# be useful in hours, minutes or seconds. Applications using at_utils will
# often need to initialiize start, stop and duration time values. These
# constants are to help with that process.
ATU_DEFAULT_DURATION = 0.5 # Default in hours for an activity entry
ATU_DEFAULT_DURATION_MINUTES = ATU_DEFAULT_DURATION * 60.0 # Default in minutes
ATU_DEFAULT_DURATION_SECONDS = ATU_DEFAULT_DURATION * 3600.0 # Default in seconds
#-----------------------------------------------------------------------------+

#region ISO Date Utilities
def iso_date_string(dt: datetime.datetime) -> str:
    """Convert a datetime object to an ISO format string."""
    if not isinstance(dt, datetime.datetime):
        raise TypeError("Cannot convert None to ISO date string")
    return dt.isoformat()

def iso_date(dt_str: str) -> datetime.datetime:
    """Convert an ISO format string to a datetime object."""
    if dt_str is None or len(dt_str) == 0: return iso_date_now()
    return datetime.datetime.fromisoformat(dt_str)

def confirm_iso_date(dt : datetime.datetime) -> bool:
    """Confirm that the input is a datetime object."""
    if isinstance(dt, datetime.datetime): return True
    return False

def validate_iso_date_string(dt_str: str) -> bool:
    """Validate ISO format date string."""
    # Return True if valid
    # otherwise raise ValueError
    try:
        # parameter type validation
        if not isinstance(dt_str, (type(None),str)):
            t = type(dt_str).__name__
            raise TypeError(f"Type:str required for dt_str, not Type: {t}")
        # check for None or empty string
        if not isinstance(dt_str, str) or dt_str is None or len(dt_str) == 0: 
            raise ValueError(f"Type:str required for dt_str, not Type: {t}")
        datetime.datetime.fromisoformat(dt_str) # return value
    except ValueError:
        raise ValueError(f"Invalid ISO datetime str value: '{dt_str}'")

def iso_date_now() -> datetime.datetime:
    """Return the current date and time."""
    return datetime.datetime.now()

def iso_date_now_string() -> str:
    """Return the current date and time in ISO format."""
    return datetime.datetime.now().isoformat()

def iso_date_approx(dt1:str, dt2:str, tolerance = 1) -> bool:
    """ Compare two ISO date strings for approximate equality within a tolerance 
    (in seconds). """
    if dt1 is None or dt2 is None:
        raise ValueError("Cannot compare None values")
    if not isinstance(tolerance, (int, float)):
        raise ValueError("Tolerance must be an integer or float")
    try:
        d1 = iso_date(dt1)
        d2 = iso_date(dt2)
        delta = abs((d2 - d1).total_seconds())
    except:
        raise ValueError("Error during calculation of date difference")

    return delta <= tolerance
#endregion

#region Timestamp Utilities

#region validate_start()
def validate_start(strt: str) -> str:
    """Validate start time for ActivityEntry constructor."""
    # Returns a valid ISO format date string for the start time
    # If dt is not type str, raise TypeError
    # If dt is None or empty string, default to time now
    # If dt is valid ISO string, return it, else raise ValueError
    if isinstance(strt, (type(None), str)):
        if (strt is None) or (len(strt) == 0): return default_start_time()
        if not isinstance(strt, str):
            raise TypeError(f"Input strt: str required, not Type: {type(dt).__name__}")
        if validate_iso_date_string(strt): return strt
        else:
            raise ValueError(f"Type:str required for stp, not Type: {type(strt).__name__}")
    raise TypeError(f"Invalid type for strt input value: Type:'{strt}' = {strt}")
#endregion

#region validate_stop()
def validate_stop(strt: str, stp: str) -> str:
    """Validate stop time for ActivityEntry constructor."""
    # Returns a valid ISO format date string for the stop time
    # Uses strt to determine the default stop time if stp is None or invalid
    # If stp is not type str, raise TypeError
    # If stp is None or empty string, default to time now
    # If stp is valid ISO string, return it
    # If either strt or stp are not type str}None, raise TypeError
    # If strt or stp are type str but not valid ISO strings, raise ValueError
    typenames = (None, str)
    if isinstance(strt, (type(None), str)):
        s = validate_start(strt) # ValueError raised if invalid strt
    else:
        raise TypeError(f"Type:str required for strt, not Type: {type(strt).__name__}")
    if isinstance(stp, (type(None), str)):
        if (stp is None) or (len(stp) == 0): return default_stop_time(s)
        if validate_iso_date_string(stp):
            return datetime.datetime.fromisoformat(stp).isoformat()
    else:
        raise TypeError(f"Type:str required for stp, not Type: {type(stp).__name__}")
#endregion

#region increase_time()
def increase_time(tval : str, hours : int = 0, minutes : int = 0, seconds : int = 0) -> float:
    """Increase the time by a given number of hours, minutes and seconds."""
    if tval is None or not isinstance(tval, str) or len(tval) == 0:
        raise ValueError("Cannot increase time for None or empty string")
    dt = iso_date(tval)
    delta = datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)
    new_dt = dt + delta
    return iso_date_string(new_dt)
#endregion

#region increase_time()
def decrease_time(tval : str, hours : int = 0, minutes : int = 0, seconds : int = 0) -> float:
    """Decrease the time by a given number of hours, minutes and seconds."""
    if tval is None or not isinstance(tval, str) or len(tval) == 0:
        raise ValueError("Cannot decrease time for None or empty string")
    hours = to_int(hours) # convert to int
    minutes = to_int(minutes)
    seconds = to_int(seconds)
    dt = iso_date(tval)
    delta = datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)
    new_dt = dt - delta
    return iso_date_string(new_dt)
#endregion

#region
def to_int(value) -> int:
    """Convert if value is a float, convertto an int, if int, return it."""
    try:
        if(type(value) == float):
            return round(value)
        return int(value)
    except (ValueError, TypeError):
        raise ValueError(f"Cannot convert {value} to int")
#endregion

#region calculate_duration()
def calculate_duration(start: str="", stop: str="", unit : str = "hours") -> float:
    """Calculate duration in hours, minutes or seconds from start and stop times."""
    # Inputs start stop must be valid ISO date time strings
    # Return the duration as a float specified by units for hours, minutes or seconds
    # Return negative value if stop is before start
    # TODO: to raise or not? Returning 0.0 for invalid input is not robust.
    try:
        if not isinstance(start, (type(None), str)) or not isinstance(stop, (type(None), str)) or \
            start is None or len(start) == 0 or stop is None or len(stop) == 0:
            return 0.0 # invalid input, cannot compute duration
        if not (validate_iso_date_string(start) and 
                validate_iso_date_string(stop)):
            return 0.0
        start_dt = iso_date(start)
        stop_dt = iso_date(stop)
        td = stop_dt - start_dt
        seconds : float = td.total_seconds() # the only float method on datetime.timedelta
        minutes : float = seconds / 60.0
        hours : float = seconds / (60.0 * 60.0)
        if unit == "hours": return hours
        elif unit == "minutes": return minutes
        return seconds 
    except Exception as e:
        print(f"Error calculating duration: {e}")
        return 0.0
#endregion

#region
def default_duration(unit : str = "hours") -> float:
    """ Default duration for an activity in hours (default), minutes or seconds """
    if unit == "hours":
        return ATU_DEFAULT_DURATION
    elif unit == "minutes":
        return ATU_DEFAULT_DURATION_MINUTES
    elif unit == "seconds":
        return ATU_DEFAULT_DURATION_SECONDS
    else: return 0
#endregion

#region default_start_time()
def default_start_time() -> str:
    """Return current time as ISO string."""
    # Returns the current time as an ISO string
    return datetime.datetime.now().isoformat()
#endregion

#region default_stop_time()
def default_stop_time(start: str = None) -> str:
    """Return start time plus default duration as ISO string.
    Input of None or empty string converts start time to current time.
    """
    # Uses the start time to calculate the default stop time
    # Returns the stop time as an ISO string
    start_time : str = validate_start(start)
    start_dt : datetime = iso_date(start_time) # convert to datetime
    td : datetime.timedelta = datetime.timedelta(seconds=default_duration("seconds"))
    stop_dt = start_dt + td
    return stop_dt.isoformat()
#endregion

#region current_timestamp()
def current_timestamp() -> str:
    """ Return the current date and time as a ISO format string """
    return iso_date_now_string()
#endregion

#region
#endregion

#region
#endregion


#-----------------------------------------------------------------------------+
