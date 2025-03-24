#------------------------------------------------------------------------------+
import configparser

class ATConfig():
    """
    ATConfig class to handle configuration file reading and writing.
    """

    def __init__(self, config_file='config.ini'):
        """
        Initialize the ATConfig with a configuration file.

        :param config_file: Path to the configuration file (default: 'config.ini').
        """
        self.config = configparser.ConfigParser()
        self.config_file = config_file
        self.load_config()

    def load_config(self):
        """
        Load the configuration from the file.
        """
        self.config.read(self.config_file)

    def get(self, section, option):
        """
        Get a value from the configuration.

        :param section: Section of the configuration.
        :param option: Option within the section.
        :return: Value of the option.
        """
        return self.config.get(section, option)

    def set(self, section, option, value):
        """
        Set a value in the configuration.

        :param section: Section of the configuration.
        :param option: Option within the section.
        :param value: Value to set for the option.
        """
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, option, value)
    
    def save(self):
        """
        Save the current configuration to the file.
        """
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)