from lib.aoclib import AOCLib


class Grammar:
    def __init__(self):
        self.terminals = {}
        self.rules = {}

    def add_production(self, symbol, production):
        self.rules.setdefault(symbol, []).append(production)
        if isinstance(production[0], str):
            self.terminals[production[0]] = []

    def remove_production(self, symbol, production):
        if symbol in self.rules:
            self.rules[symbol].remove(production)
            if not self.rules[symbol]:
                self.rules.pop(symbol)

    def productions(self, for_symbol=None):
        if for_symbol:
            for production in self.rules[for_symbol]:
                yield for_symbol, production
        else:
            for symbol, rules in self.rules.items():
                for production in rules:
                    yield symbol, production

    def normalize(self):
        # Remove unit productions

        while True:
            rules_to_remove = []
            rules_to_add = []
            for symbol, production in self.productions():
                if len(production) == 1:
                    if production[0] in self.terminals:
                        self.terminals[production[0]].append(symbol)
                    else:
                        rules_to_add.extend([(symbol, production_2)
                                             for symbol_2, production_2 in
                                             self.productions(production[0])])
                        rules_to_remove.append((symbol, production))
            if rules_to_remove:
                for symbol, production in rules_to_remove:
                    self.remove_production(symbol, production)
                for symbol, production in rules_to_add:
                    self.add_production(symbol, production)
            else:
                break

        # Normalize to Chomsky form

        new_symbol = max(self.rules.keys()) + 1

        while True:
            rules_to_remove = []
            rules_to_add = []
            for symbol, production in self.productions():
                if len(production) > 2:
                    rules_to_add.append((symbol, [production[0], new_symbol]))
                    rules_to_add.append((new_symbol, production[1:]))
                    rules_to_remove.append((symbol, production))
                    new_symbol += 1
            if rules_to_remove:
                for symbol, production in rules_to_remove:
                    self.remove_production(symbol, production)
                for symbol, production in rules_to_add:
                    self.add_production(symbol, production)
            else:
                break

    def parse(self, sentence):
        n = len(sentence)
        P = set()
        for i, c in enumerate(sentence):
            for production, symbols in self.terminals.items():
                if production == c:
                    for symbol in symbols:
                        P.add((1, i + 1, symbol))
        for l in range(2, n + 1):
            for s in range(1, n - l + 2):
                for p in range(1, l):
                    for symbol, production in self.productions():
                        if ((p, s, production[0]) in P and
                                (l - p, s + p, production[1]) in P):
                            P.add((l, s, symbol))

        return (n, 1, 0) in P


puzzle = (2020, 19)

# Initialise the helper library

aoc = AOCLib(puzzle[0])

puzzle_input = aoc.get_puzzle_input(puzzle[1])

parts = puzzle_input.split('\n\n')
part_1 = parts[0].split('\n')
part_2 = parts[1].split('\n')

grammar = Grammar()

for r in part_1:
    sym, prds = r.split(': ')
    for prd in prds.split(' | '):
        grammar.add_production(int(sym), [prd[1]] if prd[0] == '"'
                               else [int(p) for p in prd.split(' ')])

grammar.normalize()

valid_sentences = [sen for sen in part_2 if grammar.parse(sen)]

aoc.print_solution(1, len(valid_sentences))

part_1.remove('8: 42')
part_1.remove('11: 42 31')
part_1.append('8: 42 | 42 8')
part_1.append('11: 42 31 | 42 11 31')

grammar = Grammar()

for r in part_1:
    sym, prds = r.split(': ')
    for prd in prds.split(' | '):
        grammar.add_production(int(sym), [prd[1]] if prd[0] == '"'
                               else [int(p) for p in prd.split(' ')])

grammar.normalize()

valid_sentences = [sen for sen in part_2 if grammar.parse(sen)]

aoc.print_solution(2, len(valid_sentences))
