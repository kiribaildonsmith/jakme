#! /usr/bin/env python
"""A curses implementation of an editor using the Jakme framework"""
import curses
import curses.textpad
import backend

class Gui():
    """Implements a gui using the Jakme backend"""

    def __init__(self, screen):
        """Create a new gui object"""
        self.screen = screen
        self.backend = backend.Backend({'FILENAME':'hello.txt'})
        self.screen.keypad(1)
        self.refresh()

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
        self.screen.refresh()

    def main(self):
        """Start the editor"""
        self.screen.box()
        self.screen.hline(2, 1, curses.ACS_HLINE, self.maxx-2)
        self.draw_global_commands()
        self.draw_filename()
        self.refresh()
        self.screen.getch()

    def draw_global_commands(self):
        """Add the global commands menubar"""
        self.gcommands = self.backend.get_global_commands()
        xcoord = 2
        for key, _ in self.gcommands.iteritems():
            self.screen.addstr(1, xcoord, key, curses.A_BOLD)
            xcoord = len(key) + 3
            
        self.refresh()

    def draw_filename(self):
        """Say which file we're editing"""
        fn = self.backend.get_environment('FILENAME')
        xcoord = self.maxx - 2 - len(fn)
        self.screen.addstr(1, xcoord, fn, curses.A_UNDERLINE)
        self.refresh()

if __name__ == '__main__':
    try:
        stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()

        gui = Gui(stdscr)
        gui.main()

        curses.echo()
        curses.nocbreak()
        curses.endwin()
    except (Exception):
        curses.echo()
        curses.nocbreak()
        curses.endwin()
        print e


