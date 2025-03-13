#-----------------------------------------------------------------------------+
import tkinter as tk
class ATView(tk.Tk):
    """ Activity Tracker View class.
        The ATView class is a subclass of the tkinter.Tk class and implements 
        the entire user interface for the Activity Tracker application.
    """
    def __init__(self):
        super().__init__()
        self.title("PP Python Activity Tracker")
        self.geometry("800x500")
        self.create_widgets()

    def create_widgets(self):
        frm = tk.Frame(self)
        frm.grid()
        tk.Label(frm, text="Hello World!").grid(column=0, row=0)
        tk.Button(frm, text="Quit", command=self.destroy).grid(column=1, row=0)

#-----------------------------------------------------------------------------+