#! /usr/bin/env python
# File: gui.py
"""A Tkinter implemention of an EDITOR using the Jakme framework"""
from Tkinter import END, SEL_FIRST, SEL_LAST, TclError, INSERT
from Tkinter import LEFT, BOTTOM, Tk, Frame, ALL
from Tkinter import Entry, Button, Text, Label
from backend import Backend
from os.path import splitext

__author__ = "Joseph Hallett & Kiri Baildon-Smith"
__version__ = '1.0'

#Put all your function definitions up here!
#Functions are marked by indentation!


def globalcommand(path):
    """Deals with button presses relating to global commands

    Args:
    path -- path to the command to run

    Returns:
    Output of the command
    """
    return run_command(path, "@0,0", END)



def regional(path):
    """Deals with button presses relating to regional commands

    Args:
    path -- path to the command to run

    Returns:
    Output of the command
    """
    return run_command(path, SEL_FIRST, SEL_LAST)



def run_command(path, start_sel, end_sel):
    """
    Runs a command on a region of the EDITOR

    Args:
    path -- what to run
    start -- where to start
    end -- where to end
    """
    # If we haven't actually got any text selected then, treat the text_in as
    # being empty.  Delete any text we have selected
    try:
        text_in = EDITOR.get(start_sel, end_sel)
        EDITOR.delete(start_sel, end_sel)
    except TclError:
        text_in = ''

    text_out, _ = BACKEND.send_text(path, text_in)

    EDITOR.insert(INSERT, text_out)



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



def get_filetype():
    """Gets the filetype and sets in the backend any changes relating to this"""

    fln = FILENAME.get()
    _, ext = splitext(fln)
    ext = ext.strip('.')
    BACKEND.set_environment({'FILENAME':fln, 'FILETYPE':ext})
    #print ("FUNCTION: get_filetype: " + fln + "  " + ext)

    create_buttons()   

    return True


def create_buttons():
    """Creates the buttons for the global and regional commands.
    Global commands are filetype dependent"""

    #BUTTON_FRAME.pack_forget()
    #GLOBAL_FRAME.pack_forget()
    #REGIONAL_FRAME.pack_forget()

    global_children = GLOBAL_FRAME.pack_slaves()
    for child in global_children:
        child.pack_forget()

    regional_children = REGIONAL_FRAME.pack_slaves()
    for child in regional_children:
        child.pack_forget()

    ROOT.update()
	
    GLOBAL_FRAME.pack()
    REGIONAL_FRAME.pack() 

    # create the buttons
    buttons = []
    globalcommands = BACKEND.get_global_commands()
    regionalcommands = BACKEND.get_regional_commands()
    #print str(globalcommands)

    for text, path in globalcommands.iteritems():
        #print "Creating button: "+text+" with path "+path
        button = Button(GLOBAL_FRAME, text=text, 
                        command=make_global_command(path))
        buttons.append(button)
        button.pack(side=LEFT)

    for text, path in regionalcommands.iteritems():
        #print "Creating button: "+text+" with path "+path
        button = Button(REGIONAL_FRAME, text=text, 
                        command=make_regional_command(path))
        buttons.append(button)
        button.pack(side=LEFT)

    BUTTON_FRAME.pack(side=BOTTOM)




if __name__ == "__main__":
    #Will implement a gui using the Jakme backend
    ROOT = Tk()
    FRAME = Frame(ROOT)
    FRAME.pack()
    BUTTON_FRAME = Frame(FRAME)
    GLOBAL_FRAME = Frame(BUTTON_FRAME)
    REGIONAL_FRAME = Frame(BUTTON_FRAME)


    BACKEND = Backend()


    create_buttons()


    FILENAME = Entry(FRAME, width=100, validatecommand=get_filetype, 
                     validate=ALL)
    EDITOR = Text(FRAME, height=40, width=150)
    FEEDBACK = Label(FRAME, textvariable = '', width=100, fg="red")


    FILENAME.pack()
    EDITOR.pack()
    FEEDBACK.pack()

    FILENAME.insert(0, "No filename selected")


    EDITOR.bind("<Button-3>", regional)


    ROOT.mainloop()
