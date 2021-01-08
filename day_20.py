from lib.aoclib import AOCLib


class Tile:
    _TRANS = str.maketrans({'#': '1', '.': '0'})

    def __init__(self, tile_id, tile_data):
        self.tile_id = tile_id
        self.tile_data = tile_data
        self.width = len(self.tile_data[0])
        self.height = len(self.tile_data)
        self.edges = {}
        self.top = int(self.tile_data[0].translate(Tile._TRANS), 2)
        self.bottom = int(self.tile_data[-1].translate(Tile._TRANS), 2)
        self.left = int(''.join([t[0] for t in
                                 self.tile_data]).translate(Tile._TRANS), 2)
        self.right = int(''.join([t[-1] for t in
                                  self.tile_data]).translate(Tile._TRANS), 2)
        self.top_matches = []
        self.bottom_matches = []
        self.left_matches = []
        self.right_matches = []

    def rotate_right(self):
        return [''.join([self.tile_data[x][y] for x in
                         range(self.height - 1, -1, -1)])
                for y in range(self.width)]

    def flip_vert(self):
        return list(reversed(self.tile_data))


def create_tiles(tiles):
    collection = []
    ids = set()
    for tile_info in tiles:
        tile_lines = tile_info.split('\n')
        tile_id = int(tile_lines[0][5:9])
        ids.add(tile_id)
        tile_data = tile_lines[1:]
        tile_obj = Tile(tile_id, tile_data)
        r90 = Tile(tile_id, tile_obj.rotate_right())
        r180 = Tile(tile_id, r90.rotate_right())
        r270 = Tile(tile_id, r180.rotate_right())
        fv = Tile(tile_id, tile_obj.flip_vert())
        fh = Tile(tile_id, r180.flip_vert())
        fd1 = Tile(tile_id, r90.flip_vert())
        fd2 = Tile(tile_id, fv.rotate_right())
        collection.extend([tile_obj, r90, r180, r270, fv, fh, fd1, fd2])
    return collection, ids


puzzle = (2020, 20)

# Initialise the helper library

aoc = AOCLib(puzzle[0])

puzzle_input = aoc.get_puzzle_input(puzzle[1])

all_tiles = puzzle_input.split('\n\n')

tile_collection, tile_ids = create_tiles(all_tiles)

for tile in tile_collection:
    tile.left_matches = [tile_2 for tile_2 in tile_collection
                         if tile_2.right == tile.left and
                         tile.tile_id != tile_2.tile_id]
    tile.right_matches = [tile_2 for tile_2 in tile_collection
                          if tile_2.left == tile.right and
                          tile.tile_id != tile_2.tile_id]
    tile.top_matches = [tile_2 for tile_2 in tile_collection
                        if tile_2.bottom == tile.top and
                        tile.tile_id != tile_2.tile_id]
    tile.bottom_matches = [tile_2 for tile_2 in tile_collection
                           if tile_2.top == tile.bottom and
                           tile.tile_id != tile_2.tile_id]

size = int(len(all_tiles) ** 0.5)

solutions = []
arrangements = []

for start_tile in tile_collection:
    arrangements.append(([[start_tile]], tile_ids - {start_tile.tile_id}))

while arrangements:
    arrangement, remaining = arrangements.pop()
    next_x = len(arrangement[-1]) % size
    next_y = len(arrangement) - (next_x != 0)
    if next_y == size:
        solutions.append(arrangement)
        continue
    if next_x == 0:
        arrangement.append([])
        valid_tiles = [tile for tile in
                       arrangement[next_y - 1][0].bottom_matches
                       if tile.tile_id in remaining]
    else:
        valid_tiles = [tile for tile in
                       arrangement[next_y][next_x - 1].right_matches
                       if tile.tile_id in remaining and
                       (next_y == 0 or arrangement[next_y - 1][next_x]
                       in tile.top_matches)]
    for tile in valid_tiles:
        new_arrangement = arrangement.copy()
        new_arrangement[-1].append(tile)
        arrangements.append((new_arrangement, remaining - {tile.tile_id}))

aoc.print_solution(1, solutions[0][0][0].tile_id *
                      solutions[0][-1][0].tile_id *
                      solutions[0][0][-1].tile_id *
                      solutions[0][-1][-1].tile_id)

tile_size = tile_collection[0].width
full_size = size * tile_size
real_size = size * (tile_size - 2)

monster = ((0, 1), (1, 2), (4, 2), (5, 1), (6, 1), (7, 2),
           (10, 2), (11, 1), (12, 1), (13, 2), (16, 2), (17, 1),
           (18, 0), (18, 1), (19, 1))

for solution in solutions:
    mega_tile = []
    waves = 0
    for row in range(full_size):
        if row % tile_size in (0, tile_size - 1):
            continue
        mega_tile.append([])
        for col in range(full_size):
            if col % tile_size in (0, tile_size -1):
                continue
            tile = solution[row // tile_size][col // tile_size]
            pixel = tile.tile_data[row % tile_size][col % tile_size]
            mega_tile[-1].append(pixel)
            waves += pixel == '#'
    monsters = 0
    for row in range(real_size - 3):
        for col in range(real_size - 19):
            for pixel in monster:
                if mega_tile[row + pixel[1]][col + pixel[0]] != '#':
                    break
            else:
                monsters += 1
    if monsters:
        aoc.print_solution(2, waves - monsters*len(monster))
        break
