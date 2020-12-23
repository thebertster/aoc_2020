from lib.aoclib import AOCLib


def evaluate_expression(expression, precedence):
    # Converts each problem into a Reverse Polish stack!
    #
    # e.g. for "normal" operator precedence, converts:
    # ((1 + (2 * 3 + (4 - 1 + (8 * (6 - 1) + 5 + 2)) ^ 2)) + 5)
    #
    # to:
    #
    # 1 2 3 * 4 1 - 8 6 1 - * 5 + 2 + + 2 ^ + + 5 +
    #
    # Operator precedence can be set arbitrarily with the precedence dict
    #
    # Made it general purpose even though the puzzle only deals with addition
    # and multiplication of integers!

    rp_stack = []
    operator_stack = []
    operators = []
    for part in expression.split(' '):
        if part in precedence:
            # Keep track of operators within this level of bracketing

            operators.append(part)
        else:
            # Before adding this number to the RP stack, if there are previous
            # operators that have a higher precedence than the most recent
            # operator, then add those operators to the RP stack now.

            while (len(operators) >= 2 and
                   precedence[operators[-2]] >= precedence[operators[-1]]):
                rp_stack.append(operators.pop(-2))

            # If this part introduces one or more brackets then save the current
            # operator history to operator_stack and start a new operator
            # history for each nested bracket level.

            while part[0] == '(':
                part = part[1:]
                operator_stack.append(operators)
                operators = []

            # Add the operand to the RP stack.

            num_brackets = part.count(')')
            rp_stack.append(float(part if num_brackets == 0
                                else part[:-num_brackets]))

            # If this part is closing one or more brackets then append any
            # remaining operators in the history to the RP stack for each
            # bracket level that is closed, restoring the operator history.

            while num_brackets:
                while operators:
                    rp_stack.append(operators.pop())
                operators = operator_stack.pop()
                num_brackets -= 1

    # Append any remaining operators in the history to the RP stack.

    while operators:
        rp_stack.append(operators.pop())

    # Return the result of processing the Reverse Polish stack.

    return evaluate_rp(rp_stack)


def evaluate_rp(stack):
    # Evaluates a Reverse Polish stack.

    values = []
    for item in stack:
        if isinstance(item, str):
            rhs = values.pop()
            lhs = values.pop()
            if item == '+':
                values.append(lhs + rhs)
            elif item == '*':
                values.append(lhs * rhs)
            elif item == '-':
                values.append(lhs - rhs)
            elif item == '/':
                values.append(lhs / rhs)
            elif item == '^':
                values.append(lhs ** rhs)
        else:
            values.append(item)
    return values[0]


puzzle = (2020, 18)

# Initialise the helper library

aoc = AOCLib(puzzle[0])

puzzle_input = aoc.get_puzzle_input(puzzle[1], AOCLib.lines_to_list)

equal_prec = {'+': 0, '*': 0}
weird_prec = {'+': 1, '*': 0}
# normal_prec = {'^': 2, '*': 1, '/': 1, '+': 0, '-': 0}

aoc.print_solution(1, int(sum(evaluate_expression(expr, equal_prec)
                              for expr in puzzle_input)))

aoc.print_solution(2, int(sum(evaluate_expression(expr, weird_prec)
                              for expr in puzzle_input)))
