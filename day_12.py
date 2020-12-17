from lib.aoclib import AOCLib

puzzle = (2020, 12)

# Initialise the helper library1

aoc = AOCLib(puzzle[0])

puzzle_input = aoc.get_puzzle_input(puzzle[1], AOCLib.lines_to_list)

position1 = position2 = (0, 0)
direction = 0
increments = ((1, 0), (0, -1), (-1, 0), (0, 1))
waypoint = (10, 1)

for instruction in puzzle_input:
    action = instruction[0]
    value = int(instruction[1:])
    if action in 'ESWN':
        i = 'ESWN'.index(action)
        position1 = (position1[0] + value * increments[i][0],
                     position1[1] + value * increments[i][1])
        waypoint = (waypoint[0] + value * increments[i][0],
                    waypoint[1] + value * increments[i][1])
    elif action == 'F':
        position1 = (position1[0] + value * increments[direction][0],
                     position1[1] + value * increments[direction][1])
        position2 = (position2[0] + value * waypoint[0],
                     position2[1] + value * waypoint[1])
    else:
        if value == 180:
            waypoint = (-waypoint[0], -waypoint[1])
            direction = (direction + 2) % 4
        elif instruction in ('L90', 'R270'):
            waypoint = (-waypoint[1], waypoint[0])
            direction = (direction + 3) % 4
        else:
            waypoint = (waypoint[1], -waypoint[0])
            direction = (direction + 1) % 4

aoc.print_solution(1, abs(position1[0]) + abs(position1[1]))
aoc.print_solution(2, abs(position2[0]) + abs(position2[1]))
