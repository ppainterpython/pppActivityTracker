#-----------------------------------------------------------------------------+
import tkinter as tk
class ATView:
    """ Activity Tracker View """
    root: tk.Tk = None  # root window from tkinter.Tk
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("PP Python Activity Tracker")
        root.geometry("800x500")
        self.create_widgets()

    def create_widgets(self):
        frm = tk.Frame(self.root)
        frm.grid()
        tk.Label(frm, text="Hello World!").grid(column=0, row=0)
        tk.Button(frm, text="Quit", command=self.root.destroy).grid(column=1, row=0)

#-----------------------------------------------------------------------------+