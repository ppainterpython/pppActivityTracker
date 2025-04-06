#------------------------------------------------------------------------------+
# at_utils.py
import datetime,threading, os, inspect, sys, debugpy
from logging import Logger
from typing import List, Optional
from atconstants import *
#------------------------------------------------------------------------------+
#region ISO 8601 Timestamp functional interface
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
#------------------------------------------------------------------------------+
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
    # If strt is None or empty string, default to time now
    if str_empty(strt): return default_start_time()
    # If strt is a valid ISO string, return it, else raise ValueError
    if validate_iso_date_string(strt): return strt
    #endregion

#region validate_stop()
def validate_stop(strt: str, stp: str) -> str:
    """Validate stop time for ActivityEntry constructor."""
    # Returns a valid ISO format date string for the stop time
    # Uses strt to determine the default stop time if stp is None or invalid
    # If either strt or stp are not type str or None, raise TypeError
    # If strt or stp are type str but not valid ISO strings, raise ValueError
    # If stp is not type None or str, raise TypeError
    typenames = (type(None), str)
    s = validate_start(strt) # ValueError raised if invalid strt
    # If stp is None or empty string, default to time now
    if isinstance(stp, typenames):
        if str_empty(stp): return default_stop_time(s) 
        # If stp is valid ISO string, return it
        if validate_iso_date_string(stp): return stp 
    else:
        raise TypeError(f"type:str required for stp, not type: {type(stp).__name__}")
#endregion

#region increase_time()
def increase_time(tval : str=now_iso_date_string(), hours : int = 0, \
                  minutes : int = 0, seconds : int = 0) -> str:
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
                  minutes : int = 0, seconds : int = 0) -> str:
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

#region timestamp_str_or_default()
def timestamp_str_or_default(value: str) -> str:
    """Return value if non-empty str, else return current timestamp."""
    # Check if the value is a string and not empty
    # If not, return the current timestamp as an ISO string
    return value if str_notempty(value) and validate_iso_date_string(value) \
        else now_iso_date_string()
#endregion timestamp_str_or_default()

#region stop_str_or_default()
def stop_str_or_default(stop: str = None, start: str = None) -> str:
    '''Goal is to bless the stop value as a valid stop timestamp string.
    If it is a string that validates as an ISO timestamp, Return stop value.
    If it is None or empty, return the default stop time based on the 
    start time. The start timestamp is also validated and defaulted.
    If stop value is not type str or None, raise TypeError.
    Same for start, if start is None or empty, it defaults to now().
    If either stop or start are validated as strings but not valid ISO strings,
    raise ValueError.'''
    if is_not_str_or_none(stop):
        t = type(stop).__name__
        raise TypeError(f"stop must be type:str or None, not type: {t}")
    if is_not_str_or_none(start):
        t = type(start).__name__
        raise TypeError(f"start must be type:str or None, not type: {t}")
    # Return the stop if a non-empty, valid ISO timestamp string.
    if str_notempty(stop) and validate_iso_date_string(stop): return stop
    # if both timestamp stops are empty or invalid types, default to 
    # current timestamp.
    if str_empty(stop) and str_empty(start): return now_iso_date_string()
    # if stop is empty but start is valid, use start to calculate the 
    # default stop timestamp.
    if str_empty(stop): return default_stop_time(start)
    # Exception must have been raised by now, so we never arrive here.
    #endregion stop_str_or_default()

#endregion Timestamp helper functions
#------------------------------------------------------------------------------+
#region parameter validation functions
# Common validation schemes for parameters to functions and methods.
# In cases where type is unrecoverable, raise TypeError.
def is_object_or_none(value: object = None) -> bool:
    """Positive test for None or type:object, return True, else return false."""
    if value is None: return True # None is acceptable
    # Reject primitive types (int, str, float, etc.)
    if isinstance(value, (int, str, float, bool, list, tuple, dict, set)):
        return False  # Primitive types should fail
    # Ensure value is an instance of a class
    if isinstance(value, object) and type(value).__module__ != "builtins":
        return True  # Accept user-defined class instances

def is_not_object_or_none(value: object = None) -> bool:
    """Negative test for None or type:object."""
    return not is_object_or_none(value)

def is_obj_of_type(name:str, obj_value: object, 
                   obj_type:type, 
                   raise_TypeError:bool=False) -> bool:
    """Positive test for object of type: type, return True, or raise TypeError."""
    # name parameter is the name of the parameter being validated.
    # Ensure name is a string, converting None to default string
    if name is None or isinstance(name,str) and len(name) == 0: 
        name = "default_name" 
    if not isinstance(name, str): 
        if raise_TypeError:
            raise TypeError(f"name parameter must be type:'str', " + \
                            f"not type:'{type(name).__name__}'")
        else: return False
    # Ensure obj_type is a type object
    if obj_type is None or not isinstance(obj_type, type):
        if raise_TypeError:
            raise TypeError(f"obj_type parameter must be a type, " + \
                            f"not type:'{type(name).__name__}'")
        else: return False
    # Check if the class name provided in 'type' matches the value's type
    if not isinstance(obj_value, obj_type):
        if raise_TypeError:
            raise TypeError(f"'{name}'parameter value:'{obj_value}' " + \
                            f"must be of type:'{obj_type}', " + \
                            f"not type:'{type(obj_value).__name__}'")
        else:
            return False
    # If all checks pass, return True
    return True

def is_not_obj_of_type(name:str, object_value: object, 
                       obj_type:type, raise_TypeError:bool=False) -> bool:
    """Negative test for None or obj."""
    return not is_obj_of_type(name, object_value, obj_type, raise_TypeError)

def is_str_or_none(name:str="not-provided", value:str=None, 
                   raise_TypeError:bool=False) -> bool:
    """Positive test for None or type: str, return True, return False, 
    or raise TypeError or ValueError."""
    # name parameter is the name of the parameter being validated.
    if name is None: name = "converted_to_not-provided" 
    if not isinstance(name, str): 
        if raise_TypeError:
            raise TypeError(f"name parameter must be type:'str', " + \
                            f"not type:'{type(name).__name__}'")
        else: return False
    # value parameter is the value being validated.
    if value is None: return True # None is acceptable
    if isinstance(value, str): return True # type: str is acceptable
    if(raise_TypeError):
        raise TypeError(f"'{name}'parameter value:'{value}' must be " + \
                        f"type:'str' or None, " + \
                        f"not type:'{type(value).__name__}'")
    return False # other types are False

def is_not_str_or_none(name:str="not-provided", value: str = None) -> bool:
    """Negative test for None or type: str, return True, return False, 
    or raise TypeError or ValueError."""
    return not is_str_or_none(name, value)

def str_empty(value: str) -> bool:
    """Check if a string is not empty."""
    # Check if the value is a string and not empty. Treat None as empty.
    if value is None or not isinstance(value, str) or len(value) == 0:
        return True
    return False

def str_notempty(value: str) -> bool:
    """Check if a string is not empty."""
    # Check if the value is a string and not empty
    return not str_empty(value)

def str_or_none(value: str) -> str:
    """Return value if non-empty str, else return None."""
    # Check if the value is a string and not empty
    return value if str_notempty(value) else None

def str_or_default(value: str, default:str) -> str:
    """Return value if non-empty str, else return default."""
    # Check if the value is a string and not empty
    return value if str_notempty(value) else default

#region is_folder_in_path()
def is_folder_in_path(foldername:str="",pathstr:str="") -> bool:
    '''Check if the folder is in the system path.'''
    if is_not_str_or_none(foldername) or \
        is_not_str_or_none(pathstr): return False 
    if (str_empty(foldername) or str_empty(pathstr)): return False
    return True if foldername in pathstr.split(os.path.sep) else False
#endregion is_folder_in_path()

#endregion parameter validation functions
#------------------------------------------------------------------------------+
#region basic utility functions
#------------------------------------------------------------------------------+
#region ptid()
def get_pid() -> int:
    """Return the current process ID."""
    return os.getpid()
def get_tid() -> int:
    """Return the current thread ID."""
    return threading.get_native_id()
def ptid()->str:
    """Return the current [processID:threadID]."""
    return f"[{get_pid()}:{get_tid()}]"
#endregion

#region at_env_info)
# label the tuple elements for clarity
ATU_CALLER_NAME = 0         # 0: callername
ATU_APP_FILE_NAME = 1       # 1: app_file_name
ATU_CALL_MODE = 2           # 2: call_mode
ATU_VSCODE_DEBUG_MODE = 3   # 3: vscode_debug_mode
ATU_VSCODE_PYTEST_MODE = 4  # 4: vscode_pytest_mode
ATU_PYTEST_DEBUG_VSCODE = 5 # 5: pytest_debug_vscode_mode
ATU_PYTEST_MODE = 6         # 6: pytest_mode
ATU_PYTHON_SYS_PATH = 7     # 7: python_sys_path
ATU_APP_FULL_PATH = 8       # 8: app_full_path
ATU_APP_CWD = 9             # 9: app_cwd
def at_env_info(callername:str, logger: Logger,
                consoleprint:bool=False,
                ) -> tuple:
    '''
    Return a tuple with info about runtime environment.
    Content: (callername, app_file_name, call_mode,   
              "vscode_debug", "vscode_pytest", "pytest_debug_vscode",
              "pytest, python_sys_path, app_full_path, app_cwd)")
    '''
    # parameter validation
    if is_not_str_or_none(callername): # raise TypeError if not str or None
        t = type(callername).__name__
        raise TypeError(f"callername must be type:str or None, not type: {t}")
    cn = str_or_default(callername,"not provided") # default to "not provided"
    if not isinstance(consoleprint, bool):
        t = type(consoleprint).__name__
        raise TypeError(f"consoleprint must be type:bool, not type: {t}")
    #
    _ = is_not_obj_of_type(cn, logger, Logger, True) # raises TypeError if not Logger
    argv = sys.argv
    # Full path to the application
    app_full_path = argv[0] if len(argv) >= 1 else "unknown"

    # python filename that was executed
    app_file_name = os.path.basename(app_full_path)

    # caller supplied value, shoule be __name__ of the caller
    call_mode = "direct" if cn == "__main__" else "imported"

    # vscode_debug: Check if the script is running in a VSCode debug environment
    vscode_debug_mode_test: bool = \
        "debugpy" in sys.modules and \
        debugpy.is_client_connected()  
        # app_file_name == "run_pytest_script.py" \
    vscode_debug_mode = "vscode_debug" \
        if vscode_debug_mode_test else "no vcode_debug"

    # vscode_pytest: Running in a pytest environment in vscode non-debug mode
    vscode_pytest_mode_test: bool = "pytest" in sys.modules
    vscode_pytest_mode = "vscode_pytest" if vscode_pytest_mode_test \
        else "no vscode_pytest"

    # vscode_pytest_vscode: Running in a pytest environment in vscode debug mode
    pytest_debug_vscode_mode_test: bool = \
        is_folder_in_path("vscode_pytest", app_full_path) and \
        app_file_name == "run_pytest_script.py" and \
        "pytest" in sys.modules and \
        "debugpy" in sys.modules
    pytest_debug_vscode_mode = "pytest_debug_vscode" \
        if pytest_debug_vscode_mode_test else "no pytest_debug_vscode"

    # pytest: Running in pytest outside of vscode
    pytest_mode = "pytest" if "pytest" in sys.modules else "no pytest"
    temp = "PYTEST_CURRENT_TEST" in os.environ

    # Python sys.path()
    python_sys_path = sys.path

    # Current working directory
    app_cwd = os.getcwd()

    ret: List = [cn]             # 0: ATU_CALLER_NAME
    ret.append(app_file_name)            # 1: ATU_APP_FILE_NAME
    ret.append(call_mode)                # 2: ATU_CALL_MODE
    ret.append(vscode_debug_mode)        # 3: ATU_VSCODE_DEBUG_MODE
    ret.append(vscode_pytest_mode)       # 4: ATU_VSCODE_PYTEST_MODE
    ret.append(pytest_debug_vscode_mode) # 5: ATU_PYTEST_DEBUG_VSCODE
    ret.append(pytest_mode)              # 6: ATU_PYTEST_MODE
    ret.append(python_sys_path)          # 7: ATU_PYTHON_SYS_PATH
    ret.append(app_full_path)            # 8: ATU_APP_FULL_PATH
    ret.append(app_cwd)                  # 9: ATU_APP_CWD

    ret_tuple = (ret)
    if consoleprint:
        print("========================")
        print(f"         Caller __name__: {cn}")
        print(f"   Application file name: {app_file_name}")
        print(f"               Call mode: {call_mode}")
        print(f"       vscode_debug_mode: {vscode_debug_mode}")
        print(f"      vscode_pytest_mode: {vscode_pytest_mode}")
        print(f"pytest_debug_vscode_mode: {pytest_debug_vscode_mode}")
        print(f"             pytest_mode: {pytest_mode}")
        print(f"         python_sys_path: {python_sys_path}")
        print(f"   Application full path: {app_full_path}")
        print(f"                 app_cwd: {app_cwd}")
        print("========================")
    if logger is not None:
        logger.debug(f"at_env_info)={ret_tuple}")
        logger.debug(f"========================")
        logger.debug(f"         Caller __name__: {cn}")
        logger.debug(f"   Application full path: {app_full_path}")
        logger.debug(f"   Application file name: {app_file_name}")
        logger.debug(f"               Call mode: {call_mode}")
        logger.debug(f"       vscode_debug_mode: {vscode_debug_mode}")
        logger.debug(f"      vscode_pytest_mode: {vscode_pytest_mode}")
        logger.debug(f"pytest_debug_vscode_mode: {pytest_debug_vscode_mode}")
        logger.debug(f"             pytest_mode: {pytest_mode}")
        logger.debug(f"         python_sys_path: {python_sys_path}")
        logger.debug(f"                 app_cwd: {app_cwd}")
        logger.debug(f"========================")
    return tuple(ret) # Return a tuple with the values
#endregion at_env_info)

#region is_running_in_pytest()
def is_running_in_pytest(test:int=1) -> bool:
    """Check if the code is running in pytest."""
    # Check if pytest is in the stack trace
    if not isinstance(test, int): return False
    if test == 1 and "PYTEST_CURRENT_TEST" in os.environ:
        return True
    if test == 2 and 'pytest' in sys.modules: return True
    if test == 3:
        for frame in inspect.stack():
            if "pytest" in frame.filename:
                return True
    return False
#endregion is_running_in_pytest()


#endregion basic utility functions
#------------------------------------------------------------------------------+
