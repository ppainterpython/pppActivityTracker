#-----------------------------------------------------------------------------+
from view import atview 
from viewmodel import atviewmodel
class Application():
    """ Activity Tracker Main Application """
    atv: atview.ATView = None
    atvm: atviewmodel.ATViewModel = None
    def __init__(self):
        self.atv = atview.ATView() # create the ATView object
        self.atvm = atviewmodel.ATViewModel(self.atv) # create the ATViewModel object

if __name__ == "__main__":
    app = Application()
    app.atv.mainloop()

#-----------------------------------------------------------------------------+pip