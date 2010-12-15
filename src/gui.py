#! /usr/bin/env python
# File: gui.py
"""A Tkinter implemention of an editor using the Jakme framework"""
from Tkinter import *
from backend import *
from copy import *

__author__ = "Joseph Hallett & Kiri Baildon-Smith"
__version__ = '0.2'

#Put all your function definitions up here!
#Functions are marked by indentation!


def globalcommand(path):
    """Deals with button presses relating to global commands"""
    return run_command(path, "@0,0", END)


def regional(path):
    """Deals with button presses relating to regional commands"""
    return run_command(path, SEL_FIRST, SEL_LAST)

def run_command(path, start_sel, end_sel):
    """
    Runs a command on a region of the editor

    Args:
    path -- what to run
    start -- where to start
    end -- where to end
    """
    # If we haven't actually got any text selected then, treat the text_in as
    # being empty.  Delete any text we have selected
    try:
        text_in = editor.get(start_sel, end_sel)
        editor.delete(start_sel, end_sel)
    except TclError:
        text_in = ''

    text_out, info = backend.send_text(path, text_in)
    label_text = info

    editor.insert(INSERT, text_out)


def make_global_command(path):
    """Makes a global command to be run

    Args:
    path -- what to run

    Returns:
    a function to be called
    """
    return (lambda: globalcommand(path))

def make_regional_command(path):
    """Makes a regional command to be run
    
    Args:
    path -- what to run

    Returns:
    a function to be called
    """
    return (lambda: regional(path))

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
        print "Creating button: "+text+" with path "+path
        button = Button(root, text=text, command=make_global_command(path))
        buttons.append(button)

    for text, path in regionalcommands.iteritems():
        print "Creating button: "+text+" with path "+path
        button = Button(root, text=text, command=make_regional_command(path))
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
