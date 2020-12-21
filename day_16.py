from lib.aoclib import AOCLib

puzzle = (2020, 16)

# Initialise the helper library1

aoc = AOCLib(puzzle[0])

puzzle_input = aoc.get_puzzle_input(puzzle[1])

puzzle_parts = puzzle_input.split('\n\n')

field_match = {}

for fields in puzzle_parts[0].split('\n'):
    field_parts = fields.split(': ')
    field_name = field_parts[0]
    field_value_ranges = field_parts[1].split(' or ')
    field_match[field_name] = [[int(v) for v in field_value_range.split('-')]
                               for field_value_range in field_value_ranges]

my_ticket = tuple({'value': int(v),
                   'possible_names': set(field_match.keys()),
                   'final_name': ''}
                  for v in puzzle_parts[1].split('\n')[1].split(','))

nearby_tickets = [tuple((int(v) for v in nearby_ticket.split(',')))
                  for nearby_ticket in puzzle_parts[2].split('\n')[1:]]

invalid_values = []

for nearby_ticket in nearby_tickets:
    valid_fields = []
    for i, field_value in enumerate(nearby_ticket):
        valid_field_names = set()
        for field_name, valid_value in field_match.items():
            if (valid_value[0][0] <= field_value <= valid_value[0][1] or
                valid_value[1][0] <= field_value <= valid_value[1][1]):
                valid_field_names.add(field_name)
        if valid_field_names:
            valid_fields.append(valid_field_names)
        else:
            invalid_values.append(field_value)
            break
    else:
        for field, valid_field_names in zip(my_ticket, valid_fields):
            field['possible_names'].intersection_update(valid_field_names)

aoc.print_solution(1, sum(invalid_values))

fields_resolved = 0

while fields_resolved < len(my_ticket):
    for field in my_ticket:
        if len(field['possible_names']) == 1:
            field_name = field['final_name'] = field['possible_names'].pop()
            for o_field in my_ticket:
                if o_field['possible_names']:
                    o_field['possible_names'].discard(field_name)
            fields_resolved += 1
            break
    else:
        raise RuntimeError('Unable to resolve all the fields!')

answer_2 = 1

for field in my_ticket:
    if field['final_name'].startswith('departure'):
        answer_2 *= field['value']

aoc.print_solution(2, answer_2)
