from lib.aoclib import AOCLib

puzzle = (2020, 6)

# Initialise the helper library

aoc = AOCLib(puzzle[0])

puzzle_input = aoc.get_puzzle_input(puzzle[1])

answers_1 = 0
answers_2 = 0

for group in puzzle_input.split('\n\n'):
    group_answers_1 = set()
    group_answers_2 = set('abcdefghijklmnopqrstuvwxyz')
    for answer in group.split('\n'):
        group_answers_1 |= set(answer)
        group_answers_2 &= set(answer)
    answers_1 += len(group_answers_1)
    answers_2 += len(group_answers_2)

aoc.print_solution(1, answers_1)
aoc.print_solution(1, answers_2)
