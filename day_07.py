from lib.aoclib import AOCLib

puzzle = (2020, 7)

# Initialise the helper library

aoc = AOCLib(puzzle[0])

puzzle_input = aoc.get_puzzle_input(puzzle[1], AOCLib.lines_to_list)

rules = {}

for rule in puzzle_input:
    rule_elements = rule.split(' bags contain ')
    container = rule_elements[0]
    contents = rule_elements[1].split(', ')
    content_rules = []
    for content in contents:
        content_elements = content.split(' ')
        if content_elements[0] != 'no':
            content_rules.append((int(content_elements[0]),
                                ' '.join(content_elements[1:3])))
    rules[container] = content_rules

contained_in = {}

for k, v in rules.items():
    for content_rule in v:
        contained_in.setdefault(content_rule[1], []).append(k)

stack = ['shiny gold']

parent_bags = set()

while stack:
    bag = stack.pop()
    if bag in contained_in:
        parent_bags.update(contained_in[bag])
        stack.extend(contained_in[bag])

aoc.print_solution(1, len(parent_bags))

stack = [(1, 'shiny gold')]

total_bags = 0

while stack:
    parents, bag = stack.pop()
    total_bags += parents
    for rule in rules[bag]:
        stack.append((parents * rule[0], rule[1]))

aoc.print_solution(2, total_bags - 1)
