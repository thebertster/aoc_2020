from lib.aoclib import AOCLib

def egcd(x, y):
    # Extended GCD algorithm; compute GCD and Bézout coefficients

    x0, x1, y0, y1 = 1, 0, 0, 1
    while y != 0:
        q, x, y = x // y, y, x % y
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return x, x0, y0

puzzle = (2020, 13)

# Initialise the helper library1

aoc = AOCLib(puzzle[0])

puzzle_input = aoc.get_puzzle_input(puzzle[1], AOCLib.lines_to_list)

estimate = int(puzzle_input[0])
running_buses = [int(bus) for bus in puzzle_input[1].split(',') if bus != 'x']

first_departure = estimate

while True:
    for bus in running_buses:
        if first_departure % bus == 0:
            aoc.print_solution(1, bus * (first_departure - estimate))
            break
    else:
        first_departure += 1
        continue
    break

# Solving a set of linear simultaneous congruences, i.e.:
# 7,13,x,x,59,x,31,19
#
# t = 0 mod 7       => t = 0 mod 7
# t + 1 = 0 mod 13  => t = 12 mod 13
# t + 4 = 0 mod 59  => t = 55 mod 59
# t + 6 = 0 mod 31  => t = 25 mod 31
# t + 7 = 0 mod 19  => t = 12 mod 19
#
# Checking that all the moduli are pairwise coprime, we can apply the
# Chinese Remainder Theorem to calculate a solution for t
#
# t = a_i mod n_i

N = 1
a = []
n = []

for i, bus in enumerate(puzzle_input[1].split(',')):
    if bus != 'x':
        n_i = int(bus)
        N *= n_i
        a.append(-i % n_i)
        n.append(n_i)

answer = 0

for i, n_i in enumerate(n):
    c_i = N // n_i
    a_i = a[i]
    g, m1, m2 = egcd(c_i, n_i)
    assert (g == 1), 'Moduli do not appear to be co-prime!'
    # m1 = (1 / c_i) mod n_i
    # (a_i * c_i * m1) mod n_i = (a_i * c_i * (1 / c_i)) mod n_i = a_i mod n_i
    # (a_i * c_i * m1) mod c_i = 0 mod N/n_i = 0 mod n_x (when x != i)

    answer += a_i * c_i * m1

aoc.print_solution(2, answer % N)
