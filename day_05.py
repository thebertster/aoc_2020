from lib.aoclib import AOCLib

puzzle = (2020, 5)

# Initialise the helper library

aoc = AOCLib(puzzle[0])

puzzle_input = aoc.get_puzzle_input(puzzle[1], AOCLib.lines_to_list)

translation = str.maketrans('LFBR', '0011')

seats = {int(seat.translate(translation), 2) for seat in puzzle_input}

aoc.print_solution(1, max(seats))

all_seats = set(range(min(seats), max(seats) + 1))

aoc.print_solution(2, all_seats - seats)
