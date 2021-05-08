from unicurses import unicurses as curses
import time

stdscr= curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(True)

for i in range(10):
    stdscr.addch(0, i, "*")
    stdscr.refresh()
    time.sleep(1)
    stdscr.addch(0, i, " ")
    stdscr.refresh()

stdscr.addstr(0, 10, "position: ", curses.A_BOLD)
stdscr.clear()
curses.nocbreak()
stdscr.keypad(False)
curses.echo()
