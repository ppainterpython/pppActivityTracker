#------------------------------------------------------------------------------+
import getpass, pathlib, logging, pytest
from typing import List
import at_utilities.at_utils as atu
from model.ae import ActivityEntry
from model.base_atmodel.atmodel import ATModel
from model.file_atmodel import FileATModel
from model.atmodelconstants import TE_DEFAULT_DURATION, \
    TE_DEFAULT_DURATION_SECONDS, FATM_DEFAULT_ACTIVITY_STORE_URI

FATM_TEMPDATA_DIR = "tests/tempdata"
FATM_TEMPDATA_FILENAME = FATM_DEFAULT_ACTIVITY_STORE_URI  # temp data filename
FATM_TESTDATA_DIR = "tests/testdata"
FATM_TESTDATA_FILENAME = "test_activity.json"  # test data filename

#region test_atmodel_constructor() with no formal parameterer
def test_atmodel_constructor_with_no_formal_parameters():
    """Test FileATModel constructor with no formal parameters, using the
    internal default values."""
    fatm = FileATModel()
    un = getpass.getuser()
    assert fatm.activityname == None, \
        f"activity name was not None, but '{fatm.activityname}' instead. "
    assert isinstance(fatm.activities, List), \
        f"activities is not a List, got type:'{type(fatm.activities).__name__}'"
    assert len(fatm.activities) == 0, "activities should be empty list"
    assert atu.validate_iso_date_string(fatm.created_date), \
        f"created_date is not a valid ISO date string:{fatm.created_date}"
    assert atu.validate_iso_date_string(fatm.last_modified_date), \
        f"last_modified_date is not a valid ISO date string:{fatm.last_modified_date}"
    assert fatm.modified_by == getpass.getuser(), \
        "modified_by should be the current user"
    assert fatm.activity_store_uri == FATM_DEFAULT_ACTIVITY_STORE_URI, \
        f"activity_store_uri should be default '{FATM_DEFAULT_ACTIVITY_STORE_URI}', " + \
        f"but got '{fatm.activity_store_uri}' instead."
    cd = fatm.created_date; lmd = fatm.last_modified_date    
    strval = f"FileATModel(activityname='None', activities=[], created_date='{cd}', last_modified_date='{lmd}', modified_by='ppain', activity_store_uri='activity.json')"
    reprval = f"FileATModel(activityname='None', activities=[], created_date='{cd}', last_modified_date='{lmd}', modified_by='ppain', activity_store_uri='activity.json')"
    assert fatm.__str__() == strval, \
        "String representation of FileATModel is incorrect"
    assert fatm.__repr__() == reprval, \
        "String representation of FileATModel is incorrect"
#endregion

#region test_atmodel_constructor() with ALL formal parameters
def test_atmodel_constructor_with_all_formal_paramaters():
    """Test FileATModel constructor with ALL formal parameters, using none of 
    the internal default values."""
    an = "painterActivity"
    un = getpass.getuser()  # get the current user for modified_by
    al = []
    cd = atu.now_iso_date_string()  # created_date, now()
    lmd = cd  # last_modified_date, now()
    mb = un  # modified_by, current user
    asu = "foobar.json"  # activity_store_uri, arbitrary for this test
    fatm = FileATModel(activityname=an,activities=al,
                     created_date=cd, last_modified_date=lmd, 
                     activity_store_uri=asu,)
    assert fatm.activityname == an
    assert isinstance(fatm.activities, List), \
        f"activities is not a List, got type:'{type(fatm.activities).__name__}'"
    assert len(fatm.activities) == 0, "activities should be empty list"
    assert fatm.created_date == cd, \
        f"created_date is incorrect: '{fatm.created_date}', expected: '{cd}'"
    assert fatm.last_modified_date == lmd, \
        f"last_modified_date is incorrect: '{fatm.last_modified_date}', expected: '{lmd}'"
    assert fatm.modified_by == mb, \
        f"modified_by is incorrect: '{fatm.modified_by}', expected: '{mb}'"
    assert fatm.activity_store_uri == asu, \
        f"activity_store_uri is incorrect: '{fatm.activity_store_uri}', expected: '{asu}' "
    cd = fatm.created_date; lmd = fatm.last_modified_date    
    strval = f"FileATModel(activityname='painterActivity', activities=[], created_date='{cd}', last_modified_date='{lmd}', modified_by='ppain', activity_store_uri='foobar.json')"
    reprval = f"FileATModel(activityname='painterActivity', activities=[], created_date='{cd}', last_modified_date='{lmd}', modified_by='ppain', activity_store_uri='foobar.json')"
    assert fatm.__str__() == strval, \
        "String representation of FileATModel is incorrect"
    assert fatm.__repr__() == reprval, \
        "String representation of FileATModel is incorrect"
#endregion

#region test_atmodel_add_activity()
def test_atmodel_add_activity():
    """Test the add_activity method for FileATModel class"""
    """This test creates three ActivityEntry objects, adds them to the 
    FileATModel instance, saves to a temp data file, and then reads
    the file back for comparison. Temporary files are placed in the 
    folder tests/tempdata"""
    logging.debug("Starting test_atmodel_add_activity()")
    un = getpass.getuser()
    an = un + "_activity"
    # TODO: ae1.duration is float hours, but dur is minutes.
    default_dur_hours : float = atu.default_duration() # hours
    int_dur_minutes : int = int(default_dur_hours * 60) # convert to minutes
    start1 = atu.now_iso_date_string()
    start2 = atu.increase_time(start1, minutes=(int_dur_minutes + 1)) # duration + 1 min later
    start3 = atu.increase_time(start2, minutes=(int_dur_minutes + 1)) # duration + 1 min later
    stop1 = atu.increase_time(start1, minutes=int_dur_minutes)
    stop2 = atu.increase_time(start2, minutes=int_dur_minutes)
    stop3 = atu.increase_time(start3, minutes=int_dur_minutes)
    activity1 = "ae1 activity"
    activity2 = "ae2 activity"
    activity3 = "ae3 activity"

    ae1 = ActivityEntry(start=start1, stop=stop1, activity=activity1)
    assert ae1 is not None, "create activity ae1 __init__ failed!"
    assert ae1.start == start1, "ae1.start value is incorrect"
    assert ae1.duration == default_dur_hours, "ae1 duration is incorrect"

    ae2 = ActivityEntry(start=start2, stop=stop2, activity=activity2)
    assert ae2 != None, "create activity entry start2 failed!"
    assert ae2.start == start2, "ae2.start value is incorrect"
    assert ae2.duration == default_dur_hours, "ae2 duration is incorrect"

    ae3 = ActivityEntry(start=start3, stop=stop3, activity=activity3)
    assert ae3 != None, "create activity entry start3 failed!"
    assert ae3.start == start3, "ae3.start value is incorrect"
    assert ae3.duration == default_dur_hours, "ae3 duration is incorrect"

    assert (atm := FileATModel(an)) is not None, \
        "creating FileATModel instance failed"
    assert isinstance(atm, FileATModel), \
        f"FileATModel() returned type:'{type(atm).__name__}' "
    assert isinstance(atm, ATModel), \
        f"FileATModel() returned type:'{type(atm).__name__}' "

    assert atm.add_activity(ae1) is not None
    assert len(atm.activities) == 1, \
        "add_activity() failed to add 1st ActivityEntry instance to activites"
    assert atm.add_activity(ae2) is not None
    assert len(atm.activities) == 2, \
        "add_activity() failed to add 2nd ActivityEntry instance to activites"
    assert atm.add_activity(ae3) is not None
    assert len(atm.activities) == 3, \
        "add_activity() failed to add 3rd ActivityEntry instance to activites"

    # Save the created FATM object with 3 activities to a file using FileATModel.
    folder_path = pathlib.Path(FATM_TEMPDATA_DIR)
    file_name = FATM_TEMPDATA_FILENAME
    full_path = folder_path / file_name
    full_path.parent.mkdir(parents=True, exist_ok=True)
    assert atm.put_atmodel(full_path) is True, \
        f"put_atmodel failed to save to file {full_path}"

    # Read the file back into a new FileATModel instance
    new_atm = FileATModel(activityname=an, activity_store_uri=full_path)
    assert new_atm is not None, "creating FileATModel instance failed"
    assert new_atm.get_atmodel(full_path) is None, \
        f"get_atmodel failed to load from file {full_path}"
    
    # Validate the new_atm object
    assert new_atm.activityname == an, \
        f"get_atmodel activityname is incorrect: {new_atm.activityname}"
    assert len(new_atm.activities) == 3, \
        f"get_atmodel activities length is incorrect: {len(new_atm.activities)}"
    assert new_atm.activities[0].activity == ae1.activity, \
        f"get_atmodel activities[0] activity is incorrect: {new_atm.activities[0].activity}"
    assert new_atm.activities[1].activity == ae2.activity, \
        f"get_atmodel activities[1] activity is incorrect: {new_atm.activities[1].activity}"
    assert new_atm.activities[2].activity == ae3.activity, \
        f"get_atmodel activities[2] activity is incorrect: {new_atm.activities[2].activity}"
    assert new_atm.activities[0].start == ae1.start, \
        f"get_atmodel activities[0] start time is incorrect: {new_atm.activities[0].start}" 
    assert new_atm.activities[1].start == ae2.start, \
        f"get_atmodel activities[1] start time is incorrect: {new_atm.activities[1].start}"
    assert new_atm.activities[2].start == ae3.start, \
        f"get_atmodel activities[2] start time is incorrect: {new_atm.activities[2].start}"
    assert new_atm.activities[0].stop == ae1.stop, \
        f"get_atmodel activities[0] stop time is incorrect: {new_atm.activities[0].stop}"
    assert new_atm.activities[1].stop == ae2.stop, \
        f"get_atmodel activities[1] stop time is incorrect: {new_atm.activities[1].stop}"
    assert new_atm.activities[2].stop == ae3.stop, \
        f"get_atmodel activities[2] stop time is incorrect: {new_atm.activities[2].stop}"
    assert new_atm.activities[0].duration == ae1.duration, \
        f"get_atmodel activities[0] duration is incorrect: {new_atm.activities[0].duration}"
    assert new_atm.activities[1].duration == ae2.duration, \
        f"get_atmodel activities[1] duration is incorrect: {new_atm.activities[1].duration}"
    assert new_atm.activities[2].duration == ae3.duration, \
        f"get_atmodel activities[2] duration is incorrect: {new_atm.activities[2].duration}"
    assert new_atm.created_date == atm.created_date, \
        f"get_atmodel created_date is incorrect: {new_atm.created_date}"
    assert new_atm.last_modified_date == atm.last_modified_date, \
        f"get_atmodel last_modified_date is incorrect: {new_atm.last_modified_date}"
    assert new_atm.modified_by == atm.modified_by, \
        f"get_atmodel modified_by is incorrect: {new_atm.modified_by}"
    assert new_atm.modified_by == un, \
        f"get_atmodel modified_by is incorrect: {new_atm.modified_by}"
    strval = str(new_atm)  # get the string representation of the new_atm
    # assert new_atm.__str__() == atm.__str__(), \
    #     f"get_atmodel __str__() representation is incorrect: {new_atm.__str__()}"
    # assert new_atm.__repr__() == atm.__repr__(), \
    #     f"get_atmodel __repr__() representation is incorrect: {new_atm.__str__()}"
    # Clean up the temporary file
    try:
        full_path.unlink()
    except Exception as e:
        logging.error(f"Failed to delete file {full_path}: {e}")
        raise
    logging.debug("Completed test_atmodel_add_activity()")
#endregion

#region test_validate_activity_store_uri()
def test_validate_activity_store_uri():
    """Test the validate_activity_store_uri method for FileATModel class"""
    logging.debug("Starting test_validate_activity_store_uri()")

    valid_uris = [
        "valid_path.json",
        "another_valid_path.json",
        FATM_DEFAULT_ACTIVITY_STORE_URI
    ]

    recoverable_uris = [
        None,  # None value
        ""     # empty string
    ]

    invalid_uris = [
        123,  # not a string
        [],  # list instead of string
        {},  # dict instead of string
    ]

    for uri in valid_uris:
        try:
            result = FileATModel().validate_activity_store_uri(uri)
            assert isinstance(result, pathlib.Path), \
                f"Valid uir:'{uri}' did not return expected pathlib.Path, " + \
                    f"got type:'{type(result)}'"
            logging.debug(f"Valid URI '{uri}' passed validation.")
        except Exception as e:
            assert False, f"Valid URI '{uri}' raised an exception: {e}"

    for uri in recoverable_uris:
        try:
            result = FileATModel().validate_activity_store_uri(uri)
            assert isinstance(result, pathlib.Path), \
                f"Recoverable uir:'{uri}' did not return expected pathlib.Path, " + \
                    f"got type:'{type(result)}'"
            logging.debug(f"Recoverable URI '{uri}' passed validation.")
        except Exception as e:
            assert False, f"Recoverable URI '{uri}' raised an exception: {e}"

    for uri in invalid_uris:
        try:
            with pytest.raises(TypeError):
                FileATModel().validate_activity_store_uri(uri)
            logging.debug(f"Invalid URI '{uri}' passed TypeError validation.")
        except Exception as e:
            assert False, f"Invalid URI '{uri}' raised an unexpected exception: {e}"

    logging.debug("Completed test_validate_activity_store_uri()")
#endregion

#region test_to_dict()
def test_to_dict():
    """Test the to_dict method for FileATModel class"""
    logging.debug("Starting test_to_dict()")
    un = getpass.getuser()
    an = un + "_activity"
    activities = [
        ActivityEntry(start="2025-03-22T14:42:49.298776", \
                      stop="2025-03-22T15:12:49.298776", \
                        activity="ae1 activity"),
        ActivityEntry(start="2025-03-22T15:13:49.298776", \
                      stop="2025-03-22T15:43:49.298776", activity="ae2 activity"),
        ActivityEntry(start="2025-03-22T15:44:49.298776", \
                      stop="2025-03-22T16:14:49.298776", activity="ae3 activity")
    ]
    created_date = "2025-03-22T14:42:49.300051"
    last_modified_date = "2025-03-22T14:42:49.301397"
    modified_by = "ppain"
    activity_store_uri = FATM_DEFAULT_ACTIVITY_STORE_URI

    atm = FileATModel(
        activityname=an,
        activities=activities,
        created_date=created_date,
        last_modified_date=last_modified_date,
        modified_by=modified_by,
        activity_store_uri=activity_store_uri
    )

    expected_dict = {
        "activityname": an,
        "activities": [ ae.to_dict() for ae in activities ],
        "created_date": created_date,
        "last_modified_date": last_modified_date,
        "modified_by": modified_by,
        "activity_store_uri": activity_store_uri
    }

    result_dict = atm.to_dict()
    assert result_dict == expected_dict, f"to_dict() returned {result_dict}, \
        expected {expected_dict}"
    logging.debug("Completed test_to_dict()")
#endregion

#region test_get_atmodel()
def test_get_atmodel():
    """Test the get_atmodel method for FileATModel class"""
    logging.debug("Starting test_get_atmodel()")

    folder_path = pathlib.Path(FATM_TESTDATA_DIR)
    file_name = FATM_TESTDATA_FILENAME
    full_path = folder_path / file_name
    full_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Read the file back into a new FileATModel instance
    assert (new_atm := FileATModel()) is not None, \
        "creating empty FileATModel instance failed"
    assert new_atm.get_atmodel(full_path) is None, \
        f"get_atmodel failed to load from file {full_path}"
    logging.debug(f"get_atmodel() returned: {new_atm}")
    logging.debug(f"Completed test_get_atmodel()")    
#endregion

#region test_default_created_date() 
def test_default_created_date():
    """Test the default_created_date method for FileATModel class"""
    logging.debug("Starting test_default_created_date()")
    expected_date = atu.now_iso_date_string()
    result_date = FileATModel.default_creation_date()
    assert atu.iso_date_approx(result_date, expected_date, 1), \
        f"default_created_date() '{result_date}', " + \
            f"not approx equal to expected_date '{expected_date}'"
    logging.debug("Completed test_default_created_date()")
#endregion 

#region test_validate_activities_list()
def test_validate_activities_list():
    """Test the validate_activities_list method for FileATModel class"""
    logging.debug("Starting test_validate_activities_list()")
    
    # Test with a valid list of ActivityEntry instances
    valid_activities = [
        ActivityEntry(start="2025-03-22T14:42:49.298776", \
                      stop="2025-03-22T15:12:49.298776", \
                      activity="ae1 activity"),
        ActivityEntry(start="2025-03-22T15:13:49.298776", \
                      stop="2025-03-22T15:43:49.298776", 
                      activity="ae2 activity")
    ]

    # If the valid_activities list contains only ActivityEntry instances,
    # it should pass the validation returning the input list itself.
    # Otherwise, it should raise a ValueError or TypeError depending on the 
    # input type.
    l = FileATModel().valid_activities_list(valid_activities)
    assert FileATModel().valid_activities_list(valid_activities) is not None, \
        "validate_activities_list failed for valid activities"

    # Test with an empty list as valid
    assert FileATModel().valid_activities_list([]) is not None, \
        "validate_activities_list failed for empty activities list"

    # Test with an invalid list (non-ActivityEntry)
    invalid_activities = ["not an ActivityEntry"]
    with pytest.raises(ValueError):
        FileATModel().valid_activities_list(invalid_activities), \
        f"validate_activities_list did not raise ValueError for " + \
            f"invalid activities: {invalid_activities}"

    # Test with an invalid non-list value
    invalid_activities = {"foo": "bar"}  # This is a dict, not a list
    with pytest.raises(TypeError):
        FileATModel().valid_activities_list(invalid_activities), \
        f"validate_activities_list did not raise TypeError for " + \
            f"invalid activities input type: {type(invalid_activities).__name__}"

    logging.debug("Completed test_validate_activities_list()")
#endregion test_validate_activities_list()

#------------------------------------------------------------------------------+
