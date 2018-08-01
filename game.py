__author__ = 'rubi'



#
# # Initialize the grid with the 'standard' opening
import abalone.config as config

import abalone.tk as abaloneTk
import abalone
from Tkinter import Tk, Canvas, Frame, Button
tk=abaloneTk.Game()
tk.start(config.Players.Black.positions,config.Players.White.positions)
tk.mainloop()
