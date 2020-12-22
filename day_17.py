from lib.aoclib import AOCLib


class NSpace:
    @classmethod
    def nrange(cls, extents):
        if len(extents) == 0:
            yield []
        else:
            for i in range(extents[-1][0], extents[-1][1] + 1):
                for r in cls.nrange(extents[:-1]):
                    yield r + [i]

    def __init__(self, dimensions, initial_state):
        origin = [0] * dimensions
        self.offsets = [offset for offset in self.nrange([[-1, 1]] * dimensions)
                        if offset != origin]
        self.active_cubes = {tuple([x, y] + [0] * (dimensions-2))
                             for y, row in enumerate(initial_state)
                             for x, state in enumerate(row) if state == '#'}
        self.neighbours = {}

    def adjacent_cubes(self, cubes):
        return {tuple([a + b for a, b in zip(cube, offset)])
                for offset in self.offsets
                for cube in cubes}

    def active_neighbours(self, cube):
        return len({tuple([c + o for c, o in zip(cube, offset)])
                     for offset in self.offsets} & self.active_cubes)

    def do_cycle(self):
        cubes_to_remove = {cube for cube in self.active_cubes
                           if not 2 <= self.active_neighbours(cube) <= 3}
        cubes_to_add = {cube for cube in (self.adjacent_cubes(self.active_cubes)
                                          - self.active_cubes)
                        if self.active_neighbours(cube) == 3}

        self.active_cubes -= cubes_to_remove
        self.active_cubes |= cubes_to_add


puzzle = (2020, 17)

# Initialise the helper library

aoc = AOCLib(puzzle[0])

puzzle_input = aoc.get_puzzle_input(puzzle[1], AOCLib.lines_to_list)

for d in [1, 2]:
    pocket_universe = NSpace(d + 2, puzzle_input)

    for cycle in range(6):
        pocket_universe.do_cycle()

    aoc.print_solution(d, len(pocket_universe.active_cubes))
