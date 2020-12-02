from lib.aoclib import AOCLib

def find_sum_pairs(sorted_list, target):
    for entry in sorted_list:
        if entry*2 > target:
            return None
        if target - entry in sorted_list:
            return entry, target - entry
    return None

puzzle = (2020, 1)

# Initialise the helper library

aoc = AOCLib(puzzle[0])

puzzle_input = sorted(aoc.get_puzzle_input(puzzle[1], AOCLib.lines_to_list_int))

target_sum = 2020

print(puzzle_input)

solution_1 = find_sum_pairs(puzzle_input, target_sum)


aoc.print_solution(1, solution_1[0] * solution_1[1])

for i, e in enumerate(puzzle_input):
    solution_2 = find_sum_pairs(puzzle_input[i+1:], target_sum - e)
    if solution_2:
        aoc.print_solution(2, e * solution_2[0] * solution_2[1])
        break
