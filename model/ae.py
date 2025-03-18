#-----------------------------------------------------------------------------+
# ae.py
import datetime, json
import at_utilities.at_utils as atu
from dataclasses import dataclass, field

TE_DEFAULT_DURATION = 30 # minutes

@dataclass(kw_only=True)
class ActivityEntry:
    """
    A class to represent one entry of time spent doing some work.

    Attributes
    ----------
    start : str
        date and time an activity starts as ISO string format. 
    stop : str
        date and time an activity stops as ISO string format
    activity : str
        A unique activity identifier string, perhaps as a dictionary entry
        defining a list of activities that can be aggregated and summarized
    notes : str
        Additional descriptive text describing the particulars of this activity
    duration : float
        Calculated float difference between stop and start times in hours

    Data Validation at Construction
    ------------------------------
    Validate the input types for start and stop times
    and calculate the duration as a datetime.timedelta object.
    If the start or stop time are a string, it is be converted to a 
    datetime object assuming a valid ISO format datetime.
    Empty strings or 'None' values for start or stop are set to the current datetime.
    If no stop time is provided, it defaults to the start time plus 30 minutes.
    The duration is calculated as the difference between the stop and start 
    times in hours. A negative value indicates the stop time is before the start
    time. 
    """
    start: str = field(default=datetime.datetime.now().isoformat())
    stop: str = field(default=datetime.datetime.now().isoformat())
    activity: str = field(default='')
    notes: str = field(default='')
    duration: float = field(default=0.0) # duration in hours as float
    # post init function to validate start, stop and calculate duration
    def __post_init__(self):
        """Full parameters Constructor for class ActivityEntry
        
        Parameters
        ----------
        start : str
            ISO format date and time an activity starts. If none, current time is used
        stop : str
            ISO format date and time an activity stops. If none, current time is used
        activity : str
        notes : str
        """
        self.start = self.validate_start(self.start)
        self.stop = self.validate_stop(self.start, self.stop)
        self.duration = ActivityEntry.calculate_duration(self.start, self.stop)

    def __str__(self):
        return f"{self.activity}"

    # Some static helper methods for input validation
    @staticmethod
    def validate_start(dt: str) -> str:
        """Validate start time for ActivityEntry constructor."""
        # Returns a valid ISO format date string for the start time
        # If dt is not type str, raise TypeError
        # If dt is None or empty string, default to time now
        # If dt is valid ISO string, return it
        # If invalid string, raise ValueError
        if not isinstance(dt, str):
            raise TypeError(f"Input Type: str required, but Type: {type(dt).__name__} was given.")
        if dt is None or len(dt) == 0: return datetime.datetime.now().isoformat()
        if ActivityEntry.validate_iso_date_string(dt): return dt
        raise ValueError(f"Invalid start datetime value: {dt}")
    
    @staticmethod
    def validate_stop(strt: str, stp: str) -> str:
        """Validate stop time for ActivityEntry constructor."""
        # Returns a valid ISO format date string for the stop time
        # Uses strt to determine the default stop time if stp is None or invalid
        # If stp is not type str, raise TypeError
        # If stp is None or empty string, default to time now
        # If stp is valid ISO string, return it
        # If invalid string, raise ValueError
        if not isinstance(stp, str):
            raise TypeError(f"Input Type: str required, but Type: {type(stp).__name__} was given.")
        s = ActivityEntry.validate_start(strt) # exception if invalid start
        strtdt : datetime = atu.iso_date(s) # convert to datetime
        stpdefault : datetime = strtdt + ActivityEntry.default_duration() # default stop time
        if stp is None or len(stp) == 0: return stpdefault.isoformat() # default stop to start + default duration
        if ActivityEntry.validate_iso_date_string(stp):
            return datetime.datetime.fromisoformat(stp).isoformat()
        raise ValueError(f"Invalid stop datetime value: {stp}")
    
    @staticmethod
    def validate_iso_date_string(dt_str: str) -> bool:
        """Validate ISO format date string."""
        # Return True if valid
        # otherwise raise ValueError
        try:
            datetime.datetime.fromisoformat(dt_str)
            return True
        except ValueError as err:
            err.add_note(f"Invalid ISO datetime:'{dt_str}' len=({len(dt_str)})")
            raise
    
    @staticmethod
    def calculate_duration(start: str, stop: str) -> float:
        """Calculate duration in hours from start and stop times."""
        # Convert ISO strings to datetime objects and calculate the duration
        # Return the duration in hours as a float
        # Presumes start and stop are valid ISO strings, returns 0.0 if not
        # Can return negative value if stop is before start
        if start is None or stop is None:
            return 0.0
        if not isinstance(start, str) or not isinstance(stop, str):
            return 0.0
        try:
            if not (ActivityEntry.validate_iso_date_string(start) and 
                    ActivityEntry.validate_iso_date_string(stop)):
                return 0.0
            start_dt = atu.iso_date(start)
            stop_dt = atu.iso_date(stop)
            td = stop_dt - start_dt
            seconds = td.total_seconds()
            return seconds / (60.0 * 60.0)
        except Exception as e:
            print(f"Error calculating duration: {e}")
            return 0.0

    @staticmethod
    def default_duration() -> datetime.timedelta:
        """Return default duration of TE_DEFAULT_DURATION minutes as datetime.timedelta object."""
        return datetime.timedelta(minutes=TE_DEFAULT_DURATION)
    
    @staticmethod
    def default_duration_hours() -> float:
        """Return default duration of TE_DEFAULT_DURATION in hours (float)."""
        td = datetime.timedelta(minutes=TE_DEFAULT_DURATION)
        return float(td.total_seconds() / (60.0 * 60.0)  )
