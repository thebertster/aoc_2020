from lib.aoclib import AOCLib

puzzle = (2020, 9)

# Initialise the helper library

aoc = AOCLib(puzzle[0])

puzzle_input = aoc.get_puzzle_input(puzzle[1], AOCLib.lines_to_list_int)

preamble_size = 25

pair_table = {}

for i in range(preamble_size):
    for j in range(preamble_size):
        if i != j:
            pair_table.setdefault(puzzle_input[i], []).append(puzzle_input[i] +
                                                              puzzle_input[j])

index = preamble_size

invalid_number = None

while index < len(puzzle_input):
    next_number = puzzle_input[index]
    for i, p in pair_table.items():
        if next_number in p:
            break
    else:
        invalid_number = next_number
        aoc.print_solution(1, invalid_number)
        break
    pair_table.pop(puzzle_input[index - preamble_size])
    index += 1
    pair_table[next_number] = []
    for j in range(index - preamble_size, index - 1):
        pair_table[next_number].append(next_number + puzzle_input[j])

for i in range(len(puzzle_input) - 1):
    j = i + 1
    total = puzzle_input[i]
    while total < invalid_number:
        total += puzzle_input[j]
        if total == invalid_number:
            break
        j += 1
    else:
        continue
    aoc.print_solution(2, min(puzzle_input[i:j+1]) + max(puzzle_input[i:j+1]))
    break
