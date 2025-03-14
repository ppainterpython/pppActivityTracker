#-----------------------------------------------------------------------------+
from viewmodel.interfaces.iatviewmodel import IATViewModel
from view import atview


class ATViewModel(IATViewModel):
    atv: atview.ATView = None # Reference to the View object for AT.
    def __init__(self, atv: atview.ATView):
        self.atv = atv # Associate ViewModel with View

    def get_filepath(self):
        return "activities.json"