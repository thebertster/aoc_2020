from lib.aoclib import AOCLib

puzzle = (2020, 10)

# Initialise the helper library1

aoc = AOCLib(puzzle[0])

puzzle_input = aoc.get_puzzle_input(puzzle[1], AOCLib.lines_to_list_int)

adaptors = [0]
adaptors.extend(sorted(puzzle_input))
adaptors.append(adaptors[-1] + 3)

differences = [adaptors[i + 1] - adaptors[i]
               for i in range(len(adaptors) - 1)]

aoc.print_solution(1, differences.count(1) * differences.count(3))

ways_to_get_to = {0: 1}

for adaptor in adaptors[1:]:
    ways_to_get_to[adaptor] = sum([ways_to_get_to.get(previous_adaptor, 0)
                                   for previous_adaptor in
                                   range(adaptor - 3, adaptor)])

aoc.print_solution(2, ways_to_get_to[adaptors[-1]])
