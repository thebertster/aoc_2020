from lib.aoclib import AOCLib

puzzle = (2020, 2)

# Initialise the helper library

aoc = AOCLib(puzzle[0])

puzzle_input = aoc.get_puzzle_input(puzzle[1], AOCLib.lines_to_list)

valid_passwords_1 = 0
valid_passwords_2 = 0

for entry in puzzle_input:
    split_1 = entry.split(': ')
    password = split_1[1]
    split_2 = split_1[0].split(' ')
    letter = split_2[1]
    split_3 = split_2[0].split('-')
    p1 = int(split_3[0])
    p2 = int(split_3[1])
    if p1 <= password.count(letter) <= p2:
        valid_passwords_1 += 1
    if (password[p1 - 1] == letter) != (password[p2 - 1] == letter):
        valid_passwords_2 += 1

aoc.print_solution(1, valid_passwords_1)
aoc.print_solution(1, valid_passwords_2)
