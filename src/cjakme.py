#! /usr/bin/env python
import curses
import curses.textpad
import backend

class gui():
    def __init__(self, screen):
        self.screen = screen
        self.backend = backend.Backend({'FILENAME':'hello.txt'})
        self.screen.keypad(1)
        self.refresh()

    def __del__(self):
        self.screen.keypad(0)

    def refresh(self):
        y, x = self.screen.getmaxyx()
        self.y = y
        self.x = x
        self.screen.refresh()

    def main(self):
        self.screen.box()
        self.screen.hline(2, 1, curses.ACS_HLINE, self.x-2)
        self.draw_global_commands()
        self.draw_filename()
        self.refresh()
        self.screen.getch()

    def draw_global_commands(self):
        self.gcommands = self.backend.get_global_commands()
        x = 2
        for k, v in self.gcommands.iteritems():
            self.screen.addstr(1, x, k, curses.A_BOLD)
            x = len(k) + 3
            
        self.refresh()

    def draw_filename(self):
        fn = self.backend.get_environment('FILENAME')
        x = self.x - 2 - len(fn)
        self.screen.addstr(1, x, fn, curses.A_UNDERLINE)
        self.refresh()

if __name__ == '__main__':
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()

    gui = gui(stdscr)
    gui.main()

    curses.echo()
    curses.nocbreak()
    curses.endwin()


