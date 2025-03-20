#-----------------------------------------------------------------------------+
# at_utils.py
import datetime
#-----------------------------------------------------------------------------+
# Often when working with dates and times, where calculating time interval 
# durations with a start and stop time, the units of the duration value will
# be useful in hours, minutes or seconds. Applications using at_utils will
# often need to initialiize start, stop and duration time values. These
# constants are to help with that process.
# 
# The iso_date_*() functions are a simple, purely functional interface to
# to an imaginary ISODate object class. It hides the python datetime.datetime
# and datetime.timedelta classes from callers.
ATU_DEFAULT_DURATION = 0.5 # Default in hours for an activity entry
ATU_DEFAULT_DURATION_MINUTES = ATU_DEFAULT_DURATION * 60.0 # Default in minutes
ATU_DEFAULT_DURATION_SECONDS = ATU_DEFAULT_DURATION * 3600.0 # Default in seconds
#-----------------------------------------------------------------------------+

#region ISO Date functional interface
def iso_date_string(dt: datetime.datetime) -> str:
    """Convert a datetime object to an ISO format string."""
    if not isinstance(dt, datetime.datetime):
        raise TypeError("Cannot convert None to ISO date string")
    return dt.isoformat()

def iso_date(dt_str: str) -> datetime.datetime:
    """Convert an ISO format string to a datetime object."""
    # parameter type validation
    if not isinstance(dt_str, (type(None),str)):
        t = type(dt_str).__name__
        raise TypeError(f"type:str required for dt_str, not type: {t}")
    # check for None or empty string, default to current time
    if dt_str is None or len(dt_str) == 0: return now_iso_date()
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
            raise TypeError(f"type:str required for dt_str, not type: {t}")
        # check for None or empty string
        if not isinstance(dt_str, str) or dt_str is None or len(dt_str) == 0: 
            raise ValueError(f"type:str required for dt_str, not type: {t}")
        datetime.datetime.fromisoformat(dt_str)
        return True
    except ValueError:
        raise ValueError(f"Invalid ISO datetime str value: '{dt_str}'")

def now_iso_date() -> datetime.datetime:
    """Return the current date and time."""
    return datetime.datetime.now()

def now_iso_date_string() -> str:
    """Return the current date and time in ISO format."""
    return datetime.datetime.now().isoformat()

def iso_date_approx(dt1:str, dt2:str, tolerance = 1) -> bool:
    """ Compare two ISO date strings for approximate equality within a tolerance 
    (in seconds). """
    if not isinstance(dt1, (type(None),str)) or not isinstance(dt2, (type(None),str)):
        t = type(dt1).__name__ + " or " + type(dt2).__name__
        raise TypeError(f"dt1 and dt2 must be type:str or None, not type: {t}")
    if not isinstance(tolerance, (int, float)):
        t = type(tolerance).__name__
        raise TypeError(f"Tolerance must be type: integer|float, not type:{t}")
    try:
        if dt1 is None or len(dt1) == 0: dt1 = current_timestamp() # default convert
        if dt2 is None or len(dt2) == 0: dt2 = current_timestamp() # default convert
        d1 = iso_date(dt1)
        d2 = iso_date(dt2)
        delta = abs((d2 - d1).total_seconds())
    except:
        raise ValueError(f"Error with dt1:'{dt1}' or dt2:'{dt2}'")
    retval : bool = (to_float(delta) <= to_float(tolerance))
    return retval

def to_int(value) -> int:
    """Convert float value to an int, if int, return it."""
    try:
        if(type(value) == float):
            return round(value)
        return int(value)
    except (ValueError, TypeError):
        raise ValueError(f"Cannot convert {value} to int")

def to_float(value) -> float:
    """Convert int value to an float, if float, return it."""
    try:
        if(type(value) == int): return float(value)
        if(type(value) == float): return value
        return 0.0
    except (ValueError, TypeError):
        raise ValueError(f"Cannot convert {value} to int")
#endregion ISO Date functional interface

#region Timestamp helper functions

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
            raise TypeError(f"Input strt: str required, not type: {type(dt).__name__}")
        if validate_iso_date_string(strt): return strt
        else:
            raise ValueError(f"type:str required for stp, not type: {type(strt).__name__}")
    raise TypeError(f"Invalid type for strt input value: type:'{strt}' = {strt}")
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
        raise TypeError(f"type:str required for strt, not type: {type(strt).__name__}")
    if isinstance(stp, (type(None), str)):
        if (stp is None) or (len(stp) == 0): return default_stop_time(s)
        if validate_iso_date_string(stp):
            return datetime.datetime.fromisoformat(stp).isoformat()
    else:
        raise TypeError(f"type:str required for stp, not type: {type(stp).__name__}")
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
    return now_iso_date_string()
#endregion

#region
#endregion

#region
#endregion


#-----------------------------------------------------------------------------+
