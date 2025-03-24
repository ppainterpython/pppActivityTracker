#------------------------------------------------------------------------------+
from view import atview 
from viewmodel import atviewmodel

DEFAULT_CONFIG_FILE = "atconfig.ini" # default config file for the application
class Application():
    """ Activity Tracker Main Application """
    atv: atview.ATView = None
    atvm: atviewmodel.ATViewModel = None
    def __init__(self):
        # Load the configuration file
        # TODO: Implement configuration file loading logic
        # config = atconfig.ATConfig(DEFAULT_CONFIG_FILE)
        # Create the ATView for a UX
        self.atv = atview.ATView()
        # If configured, create an ATViewModel
        self.atvm = atviewmodel.ATViewModel(self.atv)
        # Which subclass(es) of ATModel are used is determined by the
        # configuration file. The ATViewModel is responsible to load the
        # configuration file and create the appropriate ATModel subclass.

    def run(self):
        """ Run the ATView application loop """
        self.atv.mainloop()

if __name__ == "__main__":
    app = Application()
    app.run()

#------------------------------------------------------------------------------+