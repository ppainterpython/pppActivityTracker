#-----------------------------------------------------------------------------+
# ae.py
import at_utilities.at_utils as atu
from dataclasses import dataclass, field
from model.atmodelconstants import TE_DEFAULT_DURATION, TE_DEFAULT_DURATION_SECONDS

TE_DEFAULT_DURATION = 30 # minutes

#------------------------------------------------------------------------------+
# #region ActivityEntry Class
@dataclass(kw_only=True)
class ActivityEntry:
    """
    A class to represent one entry of time spent doing some work.
    ActivityEntry is a dataclass that contains the start and stop time of an
    activity, the activity name, and any notes about the activity. As
    a @dataclass, the __init__() method is automatically generated, and the class
    is immutable by default. 

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
        Calculated cacluated, read-only property, returns the float difference 
        between stop and start times in hours. Rationale for hours is that time 
        tracking will use fractional hour amounts for line item task work.
    """
    # @dataclass(kw_only=True)
    # class ActivityEntry:
    # @dataclass attributes
    start: str = None
    stop: str = None
    activity: str = None
    notes: str = None
    duration: float = field(init=False)  # computed with @property
    @property
    def duration(self) -> float:
        return atu.calculate_duration(self.start, self.stop)
    @duration.setter
    def duration(self, value: float) -> None:
        self._ = value  # to please the interpreter, has a useless setter
    #--------------------------------------------------------------------------+
    #region ActivyEntery Class __post_init__() method
    # post init function to validate start, stop substituting better defaults
    # for "" and None values, and calculate duration
    def __post_init__(self):
        """
        __post_init__ processing for class ActivityEntry.
        Validate the input types for start and stop times
        and calculate the duration as a datetime.timedelta object.
        If the start or stop time are a string, it is be converted to a 
        datetime object assuming a valid ISO format datetime.
        Empty strings or 'None' values for start or stop are set to the current 
        datetime. If no stop time is provided, it defaults to the start time 
        plus 30 minutes. The duration is calculated as the difference between 
        the stop and start times in hours. A negative value indicates the stop 
        time is before the start time. 
        """
        # for timestamp parameters, if None or empty string, set to now()
        self.start = atu.validate_start(self.start)
        self.stop = atu.validate_stop(self.start, self.stop)
        self.activity = 'unset' if self.activity is None or len(self.activity) == 0  \
            else self.activity
        self.notes: str = 'unset' if self.notes is None or len(self.notes) == 0 \
            else self.notes
    #endregion ActivityEntry Class __post_init__() method 
    #--------------------------------------------------------------------------+
    #endregion ActivityEntry Class
    #--------------------------------------------------------------------------+
