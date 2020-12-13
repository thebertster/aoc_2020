from lib.aoclib import AOCLib


def run_automaton(empty_seats: set, neighbours: dict, max_neighbours):
    empty_seats = empty_seats.copy()
    occupied_seats = set()

    while True:
        filled_seats = set()
        vacated_seats = set()
        for seat in empty_seats:
            if neighbours[seat].isdisjoint(occupied_seats):
                filled_seats.add(seat)
        for seat in occupied_seats:
            if (len(neighbours[seat].intersection(occupied_seats)) >=
                    max_neighbours):
                vacated_seats.add(seat)

        if not filled_seats and not vacated_seats:
            return len(occupied_seats)

        occupied_seats.update(filled_seats)
        empty_seats.update(vacated_seats)
        occupied_seats -= vacated_seats
        empty_seats -= filled_seats


puzzle = (2020, 11)

# Initialise the helper library1

aoc = AOCLib(puzzle[0])

puzzle_input = aoc.get_puzzle_input(puzzle[1], AOCLib.lines_to_list)

height = len(puzzle_input)
width = len(puzzle_input[0])

initially_empty_seats = {(x, y) for x in range(width) for y in range(height)
                         if puzzle_input[y][x] == 'L'}

directions = [(dx, dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1]
              if dx != 0 or dy != 0]

direct_neighbours = {(seat[0], seat[1]): {(seat[0] + d[0], seat[1] + d[1])
                                          for d in directions
                                          if ((seat[0] + d[0], seat[1] + d[1])
                                              in initially_empty_seats)}
                     for seat in initially_empty_seats}

aoc.print_solution(1, run_automaton(initially_empty_seats,
                                    direct_neighbours, 4))

los_neighbours = {}

for empty_seat in initially_empty_seats:
    los_neighbours[empty_seat] = set()
    for d in directions:
        x, y = empty_seat[0], empty_seat[1]
        while True:
            x += d[0]
            y += d[1]
            if x < 0 or x > width or y < 0 or y > height:
                break
            if (x, y) in initially_empty_seats:
                los_neighbours[empty_seat].add((x, y))
                break

aoc.print_solution(2, run_automaton(initially_empty_seats,
                                    los_neighbours, 5))
