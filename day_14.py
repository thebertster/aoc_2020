from lib.aoclib import AOCLib

puzzle = (2020, 14)

# Initialise the helper library1

aoc = AOCLib(puzzle[0])

puzzle_input = aoc.get_puzzle_input(puzzle[1], AOCLib.lines_to_list)

trans = str.maketrans({'X': '0', '0': '1', '1': '0'})

memory_1 = {}
memory_2 = {}
and_bits = 0x111111111111111111111111111111111111
or_bits = 0
and_bits_2 = 0
or_bits_2 = 0
f_bits = []

for line in puzzle_input:
    parts = line.split(' = ')
    if parts[0] == 'mask':
        and_bits = int(parts[1].replace('X', '1'), 2)
        or_bits = int(parts[1].replace('X', '0'), 2)
        and_bits_2 = int(parts[1].translate(trans), 2)
        fb_locations = [i for i in range(0, 36) if parts[1][35-i] == 'X']
        f_bits = []
        for i in range(1 << len(fb_locations)):
            f_or_bits = 0
            for j, fb_location in enumerate(fb_locations):
                if i & (1 << j):
                    f_or_bits |= (1 << fb_location)
            f_bits.append(f_or_bits)
    else:
        mem_loc = int(parts[0][4:-1])
        value = int(parts[1])
        memory_1[mem_loc] = value & and_bits | or_bits
        for f_or_bits in f_bits:
            memory_2[mem_loc & and_bits_2 | or_bits | f_or_bits] = value


aoc.print_solution(1, sum(memory_1.values()))
aoc.print_solution(1, sum(memory_2.values()))
