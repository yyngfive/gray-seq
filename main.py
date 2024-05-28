import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from select_lane import App
root = ttk.Window(size=(600, 250),title='Main')
App(root)
root.mainloop()