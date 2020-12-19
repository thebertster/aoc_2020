from lib.aoclib import AOCLib

def egcd(x, y):
    # Extended GCD algorithm; compute GCD and Bézout coefficients m1, m2
    # Output o_r = gcd(x, y)
    # Output o_s, o_t = m1, m2
    # x*m1 + y*m2 = gcd(x, y)

    o_r, r, o_s, s, o_t, t = x, y, 1, 0, 0, 1

    while r != 0:
        q = o_r // r
        o_r, r = r, o_r - q*r
        o_s, s = s, o_s - q*s
        o_t, t = t, o_t - q*t
    return o_r, o_s, o_t

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

# Calculate a_i and n_i and N = n_1 * n_2 * n_3 ...

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

    # By Bézout's identity: c_i*m1 + n_i*m2 = g = 1
    # => (c_i*m1 + n_i*m2) mod n_i = 1 mod n_i
    # => c_i*m1 mod n_i = 1 mod n_i
    # => m1 = (1 / c_i) mod n_i
    #
    # (a_i * c_i * m1) mod n_i = (a_i * c_i * (1 / c_i)) mod n_i = a_i mod n_i
    # (a_i * c_i * m1) mod c_i = 0 mod N/n_i = 0 mod n_x (for any x != i)
    #
    # i.e. a_i * c_i * m1 satisfies the ith congruence but contributes 0
    # to every other congruence.
    #
    # Therefore the sum of each of these partial solutions satisfies all
    # the congruences simultaneously.

    answer += a_i * c_i * m1

aoc.print_solution(2, answer % N)
