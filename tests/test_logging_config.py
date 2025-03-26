#-----------------------------------------------------------------------------+
import getpass, pathlib, logging, pytest
from constants import AT_APP_NAME # PPPACTIVITYTRACKER.constants for App

#region test_logging_config()
def test_logging_config(caplog):
    '''Test the logging configuration of the PPPAcitivityTracker application'''
    '''Import main.py and test the setup_logging() function'''
    import main as m

    # prefix string for the test function (tf) name
    tf = f"{__name__}.setup_logging(): " 

    # Test the setup_logging() function
    test_logger = m.setup_logging(AT_APP_NAME)
    assert test_logger is not None, f"{tf}failed to return a logger"
    assert test_logger.name == AT_APP_NAME, \
        f"{tf}returned incorrect logger name: '{test_logger.name}'"

    # Our test strategy requires the log messages to propagate
    # and show up in caplog.text.
    assert test_logger.propagate, \
        f"{tf}test_logger({test_logger.name}).propagate is False, " + \
        "cannot test log messages without propagage True."

    # Test the logger functions: debug, info, warning, error, critical
    tf = f"{__name__}.setup_logging(): " 
    msg = f"{tf}logging.debug() test."
    test_logger.debug(msg)
    # This assert will fail if the test_logger.propagate is False
    assert msg in caplog.text, \
        f"{tf}: failed to log a message"

    msg = f"{tf}logging.info() test."
    test_logger.info(msg)
    assert msg in caplog.text, \
        f"{tf}: failed to log a message"

    msg = f"{tf}logging.warning() test."
    test_logger.warning(msg)
    assert msg in caplog.text, \
        f"{tf}: failed to log a message"
    
    msg = f"{tf}logging.error() test."
    test_logger.error(msg)
    assert msg in caplog.text, \
        f"{tf}: failed to log a message"
    
    msg = f"{tf}logging.critical() test."
    test_logger.critical(msg)
    assert msg in caplog.text, \
        f"{tf}: failed to log a message"
    
#endregion
