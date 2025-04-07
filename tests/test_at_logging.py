#-----------------------------------------------------------------------------+
# test_at_logging.py
#-----------------------------------------------------------------------------+
import logging, pytest
from atconstants import *
from at_logging.at_logging import *

# Setup logging for AT compaitble with pytest and other modules
# logger = atlogging_setup(AT_APP_NAME)
# if logger is None:
#     logger = logging.getLogger(AT_APP_NAME)  # fallback to default logger if setup failed
#     if logger is None:
#         logger = logging.getLogger()  # fallback to the root logger if all else fails
# if logger is not None:
#     logger.debug(f"Imported module: {__name__}")
#     logger.debug(f" Logging initialized.")

# Conduct the tests
#-----------------------------------------------------------------------------+
#region test_at_log_config_json
def test_at_log_config_json():
    '''Test the logging configuration of the PPPAcitivityTracker application'''

    # Test reading the configuration JSON file with logging.config.dictConfig()
    lc = get_at_log_config()
    assert lc is not None, f"failed to load the logging configuration file"
    assert "console" in lc["handlers"], \
        f"failed to find 'console' in the logging configuration file"
    assert "file" in lc["handlers"], \
        f"failed to find 'console' in the logging configuration file"
    assert lc["version"] == 1, \
        f"failed to find 'version' in the logging configuration file"
    assert "module_function" in lc["formatters"], \
        f"failed to find 'module_func' in the logging configuration file"
    assert "class_method" in lc["formatters"], \
        f"failed to find 'class_func' in the logging configuration file"
    logger = logging.getLogger(AT_APP_NAME)
    assert logger is not None, f"failed to create a logger"

    # Test the logging configuration file with a non-existing file
    del lc
    lc = None
    with pytest.raises(FileNotFoundError):
        lc = get_at_log_config("non-existing_file.json"), \
            f"get_at_log_config() should raise FileNotFoundError for non-existing file"
    assert lc is None, f"get_at_log_config() should return None for non-existing file"
#endregion test_at_log_config_json
#-----------------------------------------------------------------------------+
#region test_at_log_config
def test_at_log_config(caplog):
    '''Test logging function after configuration from JSON file'''
    lc = get_at_log_config(AT_LOG_CONFIG_FILE)
    assert lc is not None, f"failed to load the logging configuration file"
    logger = logging.getLogger(AT_APP_NAME)
    assert logger is not None, f"failed to create a logger"
    m1 = f"Test logging function after configuration from JSON file"
    caplog.set_level(logging.DEBUG)
    logger.debug(m1)
    assert "JSON File" in caplog.text, \
        f"failed to log a message after configuration from JSON file"
#endregion test_at_log_config
#-----------------------------------------------------------------------------+
#region test_logging_setup()
def test_logging_setup(caplog):
    '''Test the logging configuration of the PPPAcitivityTracker application'''
    '''Import main.py and test the atlogging_setup() function'''
    # import atmain as m
    logger = logging.getLogger(AT_APP_NAME)

    # prefix string for the test function (tf) name
    logger.debug(f"Starting test")
    # Test the atlogging_setup() function
    test_logger = atlogging_setup(AT_APP_NAME)
    assert test_logger is not None, f"failed to return a logger"
    assert test_logger.name == AT_APP_NAME, \
        f"returned incorrect logger name: '{test_logger.name}'"

    # Our test strategy requires the log messages to propagate
    # and show up in caplog.text.
    test_logger.propagate = True
    assert test_logger.propagate, \
        f"test_logger({test_logger.name}).propagate is False, " + \
        "cannot test log messages without propagage True."

    # Test the logger functions: debug, info, warning, error, critical
    msg = f" logging.debug() test."
    test_logger.debug(msg)
    # This assert will fail if the test_logger.propagate is False
    assert msg in caplog.text, \
        f": failed to log a debug message"

    msg = f" logging.info() test."
    test_logger.info(msg)
    assert msg in caplog.text, \
        f": failed to log an info message"

    msg = f" logging.warning() test."
    test_logger.warning(msg)
    assert msg in caplog.text, \
        f": failed to log a warning message"
    
    msg = f" logging.error() test."
    test_logger.error(msg)
    assert msg in caplog.text, \
        f": failed to log an error message"
    
    msg = f" logging.critical() test."
    test_logger.critical(msg)
    assert msg in caplog.text, \
        f": failed to log a critical message"
    del test_logger
    # Test the exception handling of atlogging_setup()
    with pytest.raises(Exception):
        test_logger = atlogging_setup(AT_TEST_EXCEPTION_LOGGER_NAME)

    logger.debug(f"Completed tests")

#endregion
