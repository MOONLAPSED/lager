import curses
import random
import time

def draw_arena(stdscr, width, height, arena):
    stdscr.clear()
    for y in range(height):
        for x in range(width):
            char = arena[y][x]
            stdscr.addch(y, x, char)
    stdscr.refresh()

def allocate_region(arena, width, height, size):
    x = random.randint(0, width - size - 1)
    y = random.randint(0, height - size - 1)
    for i in range(size):
        for j in range(size):
            arena[y + i][x + j] = '#'

def release_region(arena, width, height, size):
    x = random.randint(0, width - size - 1)
    y = random.randint(0, height - size - 1)
    for i in range(size):
        for j in range(size):
            arena[y + i][x + j] = '.'

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)
    height, width = stdscr.getmaxyx()
    height -= 1
    width -= 1

    arena = [['.' for _ in range(width)] for _ in range(height)]
    
    while True:
        draw_arena(stdscr, width, height, arena)
        
        action = random.choice(['allocate', 'release'])
        size = random.randint(1, min(width, height) // 4)

        if action == 'allocate':
            allocate_region(arena, width, height, size)
        else:
            release_region(arena, width, height, size)
        
        time.sleep(0.1)
        
        if stdscr.getch() != -1:
            break

curses.wrapper(main)
