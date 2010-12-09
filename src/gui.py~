#! /usr/bin/env python
# File: gui.py
"""A Tkinter implemention of an editor using the Jakme framework"""
from Tkinter import *
from backend import *

__author__ = "Joseph Hallett & Kiri Baildon-Smith"
__version__ = '0.1'

#Put all your function definitions up here!
#Functions are marked by indentation!

def open_file():
	"""Opens the file specified in Filename"""
	label_text.set("File opened")
	


def save_file():
	"""Saves the file"""
	label_text.set("File saved")


def close_editor():
	"""Closes the editor"""




def copy_selected():
	"""Copies the selected text"""
	label_text.set("Selected text copied")



def cut_selected():
	"""Cuts the selected text, and saves it to the clipboard"""
	label_text.set("Selected text cut")



def refresh_window():
	"""Refreshes the window"""
	label_text.set("Window refreshed")
	root.refresh()




if __name__ == "__main__":
	"""Will implement a gui using the Jakme backend"""
	root = Tk()

	label_text = StringVar()

	filename = Entry(root, width=100)
	Open = Button(root, text="Open", command = open_file)
	save = Button(root, text="Save", command = save_file)
	close = Button(root, text="Close", command = close_editor)
	copy = Button(root, text="Copy", command = copy_selected)
	cut = Button(root, text="Cut", command = cut_selected)
	refresh = Button(root, text="Refresh", command = refresh_window)
	editor = Text(root, height=40, width=150)
	feedback = Label(root, textvariable = label_text, width=100, fg="red")


	filename.grid(column=0, row=0)
	Open.grid(column=1, row=0)
	save.grid(column=2, row=0)
	close.grid(column=3, row=0)
	copy.grid(column=4, row=0)
	cut.grid(column=5, row=0)
	refresh.grid(column=6, row=0)
	editor.grid(column=0, row=1, columnspan=7)
	feedback.grid(column=0, row=2)

	filename.insert(0, "No filename selected")

	fn = filename.get()
	editor.insert(1.10, fn)


	root.mainloop()
