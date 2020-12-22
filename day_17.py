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

    @classmethod
    def points_in_hypercube(cls, extents):
        for p in cls.nrange(extents):
            yield tuple(p)

    def __init__(self, dimensions, initial_state):
        origin = (0,) * dimensions
        self.offsets = [offset for offset in
                        self.points_in_hypercube([[-1, 1]] * dimensions)
                        if offset != origin]
        self.active_cubes = {tuple([x, y] + [0] * (dimensions-2))
                             for y, row in enumerate(initial_state)
                             for x, state in enumerate(row) if state == '#'}

        self.extents = [[-1, len(initial_state[0])],
                        [-1, len(initial_state)]] + [[-1, 1]] * (dimensions-2)

    def count_neighbours(self, cube):
        return len([neighbour for neighbour in
                    [tuple([a + b for a, b in zip(cube, offset)])
                     for offset in self.offsets]
                    if neighbour in self.active_cubes])

    def do_cycle(self):
        cubes_to_remove = {cube for cube in self.active_cubes
                           if not 2 <= self.count_neighbours(cube) <= 3}
        cubes_to_add = {cube for cube in self.points_in_hypercube(self.extents)
                        if (cube not in self.active_cubes and
                            self.count_neighbours(cube) == 3)}
        if cubes_to_add:
            self.extents = [[min(old_extent[0], min(new_extent) - 1),
                             max(old_extent[1], max(new_extent) + 1)]
                            for new_extent, old_extent in
                            zip(zip(*cubes_to_add), self.extents)]
        self.active_cubes.difference_update(cubes_to_remove)
        self.active_cubes.update(cubes_to_add)


puzzle = (2020, 17)

# Initialise the helper library1

aoc = AOCLib(puzzle[0])

puzzle_input = aoc.get_puzzle_input(puzzle[1], AOCLib.lines_to_list)

for d in [1, 2]:
    pocket_universe = NSpace(d + 2, puzzle_input)

    for cycle in range(6):
        pocket_universe.do_cycle()

    aoc.print_solution(d, len(pocket_universe.active_cubes))
