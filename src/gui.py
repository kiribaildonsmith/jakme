#! /usr/bin/env python
# File: gui.py
"""A Tkinter implemention of an editor using the Jakme framework"""
from Tkinter import *

__author__ = "Joseph Hallett & Kiri Baildon-Smith"
__version__ = '0.1'



if __name__ == "__main__":
	"""Will implement a gui using the Jakme backend"""
	root = Tk()

	filename = Entry(root, width=100)
	open = Button(root, text="Open")
	save = Button(root, text="Save")
	close = Button(root, text="Close")
	copy = Button(root, text="Copy")
	cut = Button(root, text="Cut")
	editor = Text(root, height=40, width=150)
	feedback = Label(root, width=100, fg="red")


	filename.grid(column=0, row=0)
	open.grid(column=1, row=0)
	save.grid(column=2, row=0)
	close.grid(column=3, row=0)
	copy.grid(column=4, row=0)
	cut.grid(column=5, row=0)
	editor.grid(column=0, row=1, columnspan=6)
	feedback.grid(column=0, row=2)

	root.mainloop()

