#-----------------------------------------------------------------------------+
# at_utils.py
import datetime, json

def iso_date_string(dt: datetime.datetime) -> str:
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