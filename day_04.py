from lib.aoclib import AOCLib

puzzle = (2020, 4)

# Initialise the helper library

aoc = AOCLib(puzzle[0])

puzzle_input = aoc.get_puzzle_input(puzzle[1])

required_fields = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}
valid_fields = required_fields | {'cid'}
valid_hcl = {'a', 'b', 'c', 'd', 'e', 'f',
             '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}
valid_ecl = {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}

passports = [[kv.split(':') for kv in passport.replace('\n', ' ').split(' ')]
             for passport in puzzle_input.split('\n\n')]

def is_valid(keys):
    return keys.issuperset(required_fields) and keys.issubset(valid_fields)

valid_passports = [passport for passport in passports
                   if is_valid({kv[0] for kv in passport})]

aoc.print_solution(1, len(valid_passports))

valid_passports_2 = []

for passport in valid_passports:
    for k, v in passport:
        try:
            if k == 'byr':
                byr = int(v)
                if not 1920 <= byr <= 2002:
                    break
            elif k == 'iyr':
                iyr = int(v)
                if not 2010 <= iyr <= 2020:
                    break
            elif k == 'eyr':
                eyr = int(v)
                if not 2020 <= eyr <= 2030:
                    break
            elif k == 'hgt':
                hgt = int(v[:-2])
                if v[-2:] == 'cm':
                    if not 150 <= hgt <= 193:
                        break
                elif v[-2:] == 'in':
                    if not 59 <= hgt <= 76:
                        break
                else:
                    break
            elif k == 'hcl':
                if v[0] != '#':
                    break
                if not set(v[1:]).issubset(valid_hcl):
                    break
            elif k == 'ecl':
                if v not in valid_ecl:
                    break
            elif k == 'pid':
                if len(v) != 9 or not v.isdigit():
                    break
        except ValueError:
            break
    else:
        valid_passports_2.append(passport)

aoc.print_solution(1, len(valid_passports_2))
