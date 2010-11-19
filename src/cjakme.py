#! /usr/bin/env python
"""A curses implementation of an editor using the Jakme framework"""
import curses
import curses.textpad
import backend

__author__ = "Joseph Hallett & Kiri Baildon-Smith"
__version__ = '0.1'

class Gui():
    """Implements a gui using the Jakme backend"""

    def __init__(self, screen):
        """Create a new gui object
        
        Arguments:
        screen -- the screen to draw on
        """
        self.screen = screen
        self.backend = backend.Backend({'FILENAME':'hello.txt'})
        self.screen.keypad(1)
        self.refresh()

        self.gcommands = self.backend.get_global_commands()
        self.maxx = 0
        self.maxy = 0

    def __del__(self):
        """When destroying the gui make sure to set back the keyboard to
           normal
        """
        self.screen.keypad(0)

    def refresh(self):
        """Refresh the screen"""
        maxy, maxx = self.screen.getmaxyx()
        self.maxy = maxy
        self.maxx = maxx
        self.screen.hline(1, 0, curses.ACS_HLINE, self.maxx)
        self.screen.refresh()

    def main(self):
        """Start the editor"""
        self.refresh()
        self.draw_global_commands()
        self.draw_filename()
        self.refresh()
        self.screen.getch()

    def draw_global_commands(self):
        """Add the global commands menubar"""
        xcoord = 0
        for key, _ in self.gcommands.iteritems():
            self.screen.addstr(0, xcoord, key, curses.A_BOLD)
            xcoord = len(key) + 1
            
        self.refresh()

    def runcommand(self, path, text=""):
        """Run a command through the backend

        Arguments:
        path -- the command to run
        text -- the text to pass it (defaults to the empty string)
        """
        output, extra = self.backend.send_text(path, text)
        
        self.displaymessage(extra)
        

      

    def displaymessage(self, text):
        """Display a message to the user
        
        Arguments:
        text -- the text to display
        """
        height = self.maxx - 2
        width = self.maxy - 2
        popup = curses.newwin(height, width, 1, 1)
        popup.box()

        i = 1
        for line in text.splitlines():
            popup.addstr(i, 1, line)
        
        popup.refresh()
        self.screen.refresh()
        popup.refresh()
        popup.getch()

        popup.endwin()

    def draw_filename(self):
        """Say which file we're editing"""
        func = self.backend.get_environment('FILENAME')
        xcoord = self.maxx - len(func)
        self.screen.addstr(0, xcoord, func, curses.A_UNDERLINE)
        self.refresh()

if __name__ == '__main__':
    try:
        __screen__ = curses.initscr()
        curses.noecho()
        curses.cbreak()

        __gui__ = Gui(__screen__)
        __gui__.main()

        curses.echo()
        curses.nocbreak()
        curses.endwin()

    # If anything has gone wrong we haven't handled yet reset the terminal and
    # print the error message
    except Exception as e:
        curses.echo()
        curses.nocbreak()
        curses.endwin()
        print(type(e))
        print(e.args)
        print e


