#-----------------------------------------------------------------------------+
# test_at_logging.py
#-----------------------------------------------------------------------------+
import logging, sys
from atconstants import *
from at_utilities.at_logging import atlogging_setup
import at_utilities.at_utils as atu

# Setup logging for AT compaitble with pytest and other modules
p = atu.pfx(mn=__name__)
logger = atlogging_setup(AT_APP_NAME)
if logger is None:
    logger = logging.getLogger(AT_APP_NAME)  # fallback to default logger if setup failed
    if logger is None:
        logger = logging.getLogger()  # fallback to the root logger if all else fails
if logger is not None:
    logger.debug(f"{p}Imported module: {__name__}")
    logger.debug(f"{p} Logging initialized.")

# Conduct the tests
import getpass, pathlib, pytest
from atconstants import AT_APP_NAME # PPPACTIVITYTRACKER.constants for App

#region test_logging_setup()
def test_logging_setup(caplog):
    '''Test the logging configuration of the PPPAcitivityTracker application'''
    '''Import main.py and test the atlogging_setup() function'''
    # import atmain as m

    # prefix string for the test function (tf) name
    tf = atu.pfx(mn=__name__)  # Use the module name for the prefix
    logger.debug(f"{tf}Starting test")
    # Test the atlogging_setup() function
    test_logger = atlogging_setup(AT_APP_NAME)
    assert test_logger is not None, f"{tf}failed to return a logger"
    assert test_logger.name == AT_APP_NAME, \
        f"{tf}returned incorrect logger name: '{test_logger.name}'"

    # Our test strategy requires the log messages to propagate
    # and show up in caplog.text.
    test_logger.propagate = True
    assert test_logger.propagate, \
        f"{tf}test_logger({test_logger.name}).propagate is False, " + \
        "cannot test log messages without propagage True."

    # Test the logger functions: debug, info, warning, error, critical
    msg = f"{tf} logging.debug() test."
    test_logger.debug(msg)
    # This assert will fail if the test_logger.propagate is False
    assert msg in caplog.text, \
        f"{tf}: failed to log a debug message"

    msg = f"{tf} logging.info() test."
    test_logger.info(msg)
    assert msg in caplog.text, \
        f"{tf}: failed to log an info message"

    msg = f"{tf} logging.warning() test."
    test_logger.warning(msg)
    assert msg in caplog.text, \
        f"{tf}: failed to log a warning message"
    
    msg = f"{tf} logging.error() test."
    test_logger.error(msg)
    assert msg in caplog.text, \
        f"{tf}: failed to log an error message"
    
    msg = f"{tf} logging.critical() test."
    test_logger.critical(msg)
    assert msg in caplog.text, \
        f"{tf}: failed to log a critical message"
    del test_logger
    # Test the exception handling of atlogging_setup()
    with pytest.raises(Exception):
        test_logger = atlogging_setup(AT_TEST_EXCEPTION_LOGGER_NAME)

    logger.debug(f"{tf}Completed tests")

#endregion
