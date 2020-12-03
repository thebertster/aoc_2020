from lib.aoclib import AOCLib

def count_the_trees(forest, vector):
    height = len(forest)
    width = len(forest[0])

    position = (0, 0)

    number_of_trees = 0

    while True:
        position = (position[0] + vector[0], position[1] + vector[1])
        if position[1] >= height:
            return number_of_trees
        if forest[position[1]][position[0] % width] == '#':
            number_of_trees += 1


puzzle = (2020, 3)

# Initialise the helper library

aoc = AOCLib(puzzle[0])

puzzle_input = aoc.get_puzzle_input(puzzle[1], AOCLib.lines_to_list)

solution_1 = count_the_trees(puzzle_input, (3, 1))

aoc.print_solution(1, solution_1)

solution_2 = (solution_1 *
              count_the_trees(puzzle_input, (1, 1)) *
              count_the_trees(puzzle_input, (5, 1)) *
              count_the_trees(puzzle_input, (7, 1)) *
              count_the_trees(puzzle_input, (1, 2)))

aoc.print_solution(2, solution_2)
