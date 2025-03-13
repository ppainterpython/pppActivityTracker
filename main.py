#-----------------------------------------------------------------------------+
import tkinter as tk
from view import atview 
class Application():
    """ Activity Tracker Main Application"""
    atv: tk.Tk = None
    def __init__(self,root: tk.Tk):
        self.atv = atview.ATView(root)

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    root.mainloop()

#-----------------------------------------------------------------------------+