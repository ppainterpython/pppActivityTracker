#-----------------------------------------------------------------------------+
# at_utils.py
import datetime, json

#region ISO Date Utilities
def iso_date_string(dt: str) -> str:
    """Convert a datetime object to an ISO format string."""
    if dt is None:
        raise ValueError("Cannot convert None to ISO date string")
    return dt.isoformat()

def iso_date(dt_str: str) -> datetime.datetime:
    """Convert an ISO format string to a datetime object."""
    if dt_str is None or len(dt_str) == 0: return iso_date_now()
    return datetime.datetime.fromisoformat(dt_str)

def iso_date_now() -> datetime.datetime:
    """Return the current date and time."""
    return datetime.datetime.now()

def iso_date_now_string() -> str:
    """Return the current date and time in ISO format."""
    return datetime.datetime.now().isoformat()

def iso_date_approx(dt1:str, dt2:str, tolerance = 1) -> bool:
    """ Compare two ISO date strings for approximate equality within a tolerance (in seconds). """
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
def increase_time(tval : str, hours : int = 0, minutes : int = 0, seconds : int = 0) -> str:
    """Increase the time by a given number of hours, minutes and seconds."""
    if tval is None or not isinstance(tval, str) or len(tval) == 0:
        raise ValueError("Cannot increase time for None or empty string")
    dt = iso_date(tval)
    delta = datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)
    new_dt = dt + delta
    return iso_date_string(new_dt)
#endregion
#-----------------------------------------------------------------------------+
