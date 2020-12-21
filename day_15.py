from lib.aoclib import AOCLib

puzzle = (2020, 15)

# Initialise the helper library1

aoc = AOCLib(puzzle[0])

puzzle_input = aoc.get_puzzle_input(puzzle[1], AOCLib.to_list_int)

for part in (0, 1):
    memory = {number: (i, None) for i, number in enumerate(puzzle_input)}
    last_number = puzzle_input[-1]
    this_number = None
    for i in range(len(memory), [2020, 30000000][part]):
        last_spoken, previous_spoken = memory[last_number]
        this_number = (0 if previous_spoken is None
                       else last_spoken - previous_spoken)
        memory[this_number] = (i, memory[this_number][0]
                               if this_number in memory else None)
        last_number = this_number

    aoc.print_solution(part + 1, this_number)
