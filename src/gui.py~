#! /usr/bin/env python
# File: gui.py
"""A Tkinter implemention of an editor using the Jakme framework"""
from Tkinter import *
from backend import *

__author__ = "Joseph Hallett & Kiri Baildon-Smith"
__version__ = '0.1'

#Put all your function definitions up here!
#Functions are marked by indentation!


def globalcommand(path):
	"""Deals with button presses relating to global commands"""



def regional(path):
	"""Deals with button presses relating to regional commands"""
	start_sel = SEL_FIRST
	end_sel = SEL_LAST	
	text_in = str(editor.get(start_sel, end_sel))


	print text_in
	editor.delete(start_sel, end_sel)
	#editor.tag_remove(SEL, start_sel, end_sel)

	print "PATH IS "+path
	text_out, info = backend.send_text(path, text_in)

	print "OUTPUT IS:"
	print text_out
	label_text = info

	editor.insert(INSERT, text_out)


if __name__ == "__main__":
	"""Will implement a gui using the Jakme backend"""
	root = Tk()

	label_text = StringVar()
	backend = Backend()


	# create the buttons
	buttons = []
	globalcommands = backend.get_global_commands()
	regionalcommands = backend.get_regional_commands()
	print str(globalcommands)

	for text, path in globalcommands.iteritems():
		print "Creating button: "+text
		button = Button(root, text=text, command=(lambda: globalcommand(path)))
		buttons.append(button)

	for text, path in regionalcommands.iteritems():
		print "Creating button: "+text
		button = Button(root, text=text, command=(lambda: regional(path)))
		buttons.append(button)


	filename = Entry(root, width=100)
	editor = Text(root, height=40, width=150)
	feedback = Label(root, textvariable = label_text, width=100, fg="red")

	
	#place the buttons
	i = 1
	for button in buttons:
		button.grid(column=i, row=0)
		i = i+1

	filename.grid(column=0, row=0)
	editor.grid(column=0, row=1, columnspan=7)
	feedback.grid(column=0, row=2)

	filename.insert(0, "No filename selected")

	fn = filename.get()
	editor.insert(1.10, fn)

	editor.bind("<Button-3>", regional)


	root.mainloop()
