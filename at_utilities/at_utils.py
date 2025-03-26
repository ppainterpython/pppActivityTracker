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

#region ISO 8601 Timestamp functional interface
def iso_date_string(dt: datetime.datetime) -> str:
    """Convert a datetime object to an ISO format string."""
    if not isinstance(dt, datetime.datetime):
        t = type(dt).__name__
        raise TypeError("Cannot convert type:'{t}' to ISO date string")
    return dt.isoformat()

def iso_date(dt_str: str) -> datetime.datetime:
    """Convert an ISO format string to a datetime object."""
    # parameter type validation
    if not isinstance(dt_str, (type(None),str)):
        t = type(dt_str).__name__
        raise TypeError(f"type:str required for dt_str, not type: {t}")
    # check for None or empty string, default to current time
    if dt_str is None or len(dt_str) == 0: return now_iso_date()
    # .fromisoformat() raises ValueError if invalid
    return datetime.datetime.fromisoformat(dt_str)

def confirm_iso_date(dt : datetime.datetime) -> bool:
    """Confirm that the input is a datetime object."""
    if isinstance(dt, datetime.datetime): return True
    return False

def validate_iso_date_string(dt_str: str) -> bool:
    """Validate ISO format date string."""
    # Return True if valid
    # Otherwise raises TypeError or ValueError
    # parameter type validation, only nonzero length string is valid
    if not isinstance(dt_str, str): 
        t = type(dt_str).__name__
        m = f"Requires str with valid ISO timestamp, not type: {t}"
        raise TypeError(m)
    if len(dt_str) < len("2023-10-01T12:00:00"):
        m = f"Requires valid ISO format timestamp, not '{dt_str}'"
        raise ValueError(m)
    try:
        # check for valid ISO date & time format string
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
        raise TypeError(f"dt1, dt2 must be type:str or None, not type: {t}")
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
    except (ValueError, TypeError) as e:
        e.add_note(f"{type(e).__name__}: Cannot convert '{value}' to int")
        raise 

def to_float(value) -> float:
    """Convert int value to an float, if float, return it."""
    try:
        if(type(value) == int): return float(value)
        if(type(value) == float): return value
        return float(value)
    except (ValueError, TypeError) as e:
        e.add_note(f"{type(e).__name__}: Cannot convert '{value}' to int")
        raise
#endregion ISO 8601 Timestamp functional interface

#region Timestamp helper functions

#region validate_start()
def validate_start(strt: str) -> str:
    """Validate start time for ActivityEntry constructor."""
    # Validate strt is a valid ISO format date string for the start time
    # If dt is not type None or str, raise TypeError
    if not isinstance(strt, (type(None), str)):
        t = type(strt).__name__
        m = f"Invalid type for strt input value: type:'{t}' = {strt}"
        raise TypeError(m)
    # If dt is None or empty string, default to time now
    if (strt is None) or (len(strt) == 0): return default_start_time()
    # If dt is a valid ISO string, return it, else raise ValueError
    if validate_iso_date_string(strt): return strt
    #endregion

#region validate_stop()
def validate_stop(strt: str, stp: str) -> str:
    """Validate stop time for ActivityEntry constructor."""
    # Returns a valid ISO format date string for the stop time
    # Uses strt to determine the default stop time if stp is None or invalid
    # If either strt or stp are not type str}None, raise TypeError
    # If strt or stp are type str but not valid ISO strings, raise ValueError
    # If stp is not type None or str, raise TypeError
    typenames = (type(None), str)
    s = validate_start(strt) # ValueError raised if invalid strt
    # If stp is None or empty string, default to time now
    if isinstance(stp, typenames):
        if (stp is None) or (len(stp) == 0): return default_stop_time(s)
        # If stp is valid ISO string, return it
        if validate_iso_date_string(stp): return stp
    else:
        raise TypeError(f"type:str required for stp, not type: {type(stp).__name__}")
#endregion

#region increase_time()
def increase_time(tval : str=now_iso_date_string(), hours : int = 0, \
                  minutes : int = 0, seconds : int = 0) -> float:
    """Increase the time by a given number of hours, minutes and seconds."""
    # TODO: handle leap year offset
    if not isinstance(tval, str):
        t = type(tval).__name__
        raise TypeError(f"type:str required for tval, not type: {t}")
    validate_iso_date_string(tval) # raises ValueError if invalid
    try:
        dt = iso_date(tval)
        delta = datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)
        new_dt = dt + delta
        return iso_date_string(new_dt)
    except TypeError:
        raise
#endregion

#region decrease_time()
def decrease_time(tval : str=now_iso_date_string(), hours : int = 0, \
                  minutes : int = 0, seconds : int = 0) -> float:
    """Decrease the time by a given number of hours, minutes and seconds."""
    # TODO: handle leap year offset
    if not isinstance(tval, str):
        t = type(tval).__name__
        raise TypeError(f"type:str required for tval, not type: {t}")
    validate_iso_date_string(tval) # raises ValueError if invalid
    # hours = to_int(hours) # convert to int
    # minutes = to_int(minutes)
    # seconds = to_int(seconds)
    try:
        dt = iso_date(tval)
        delta = datetime.timedelta(hours=abs(hours), minutes=abs(minutes), \
                                   seconds=abs(seconds))
        new_dt = dt - delta
        return iso_date_string(new_dt)
    except TypeError:
        raise
#endregion

#region calculate_duration()
def calculate_duration(start: str, stop: str, unit : str = "hours") -> float:
    """Calculate duration in hours, minutes or seconds from start and stop times."""
    # Required parameters start & stop must be valid ISO 8601 date time strings.
    # Return the duration as a float specified by units for hours, minutes or 
    # seconds.
    # Return negative value if stop is before start.
    # Raises TypeError or ValueError as appropriate.
    valid_units = ("hours", "minutes", "seconds")
    # check for TypeError if start or stop are not type None or str
    if not isinstance(start, str) or not isinstance(stop, str):
        t = type(start).__name__ + " or " + type(stop).__name__
        m = f"start, stop must both be type:str, not type: {t}"
        raise TypeError(m)
    # check for ValueError with empty strings
    if len(start) == 0 or len(stop) == 0:
        m = "Neither start or stop can be empty strings"
        raise ValueError(m)
    if unit not in valid_units:
        m = f"unit must be one of {valid_units}, not '{unit}'"
        raise ValueError(m)
    # Validate the start and stop strings are valid ISO format date strings
    # Raises ValueError if invalid
    validate_iso_date_string(start) and validate_iso_date_string(stop)
    start_dt = iso_date(start) # iso_date() raises ValueError if invalid
    stop_dt = iso_date(stop)
    td = stop_dt - start_dt
    seconds : float = td.total_seconds() # only method returning float 
    minutes : float = seconds / 60.0
    hours : float = seconds / (60.0 * 60.0)
    if unit == "hours": return hours
    elif unit == "minutes": return minutes
    return seconds 
#endregion

#region default_duration()
def default_duration(unit : str = "hours") -> float:
    """ Default duration for an activity in hours (default), minutes or seconds """
    if unit == "hours":
        return ATU_DEFAULT_DURATION
    elif unit == "minutes":
        return ATU_DEFAULT_DURATION_MINUTES
    elif unit == "seconds":
        return ATU_DEFAULT_DURATION_SECONDS
    else: return 0.0
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

#endregion Timestamp helper functions
#-----------------------------------------------------------------------------+
#region
#endregion

#region
#endregion


#-----------------------------------------------------------------------------+
