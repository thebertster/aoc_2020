from lib.aoclib import AOCLib
from game_console import GameConsole

puzzle = (2020, 8)

# Initialise the helper library

aoc = AOCLib(puzzle[0])

puzzle_input = aoc.get_puzzle_input(puzzle[1], AOCLib.lines_to_list)

console = GameConsole(puzzle_input)

aoc.print_solution(1, console.check_for_loop()[1])

mutator = {'nop': 'jmp', 'jmp': 'nop'}

for i in range(len(console.program)):
    loops, acc = console.check_for_loop((i, mutator))
    if not loops:
        aoc.print_solution(2, acc)
        break
