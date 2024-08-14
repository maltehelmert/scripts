#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import heapq
import itertools
import time


VARIABLES = ["a", "b", "c", "d"]

TRUTH_TABLE_SIZE = 1 << len(VARIABLES)
TRUTH_TABLE_MASK = (1 << TRUTH_TABLE_SIZE) - 1


def log(text):
    print(f"[{time.process_time():.2f} sec] {text}")


class Formula:
    def __init__(self):
        self.size = self.compute_size()
        # Truth tables are represented as a single integer
        # implementing a bitmask for efficiency.
        self.truth_table = self.compute_truth_table()


class Atom(Formula):
    def __init__(self, variable):
        self.variable = variable
        self.truth_table = None
        Formula.__init__(self)

    def compute_size(self):
        return 1

    def compute_truth_table(self):
        # Slow implementation, to be overridden in derived classes
        # where we have a better way to compute the whole truth table
        # at once.
        power = 1
        result = 0
        for interpretation in all_interpretations():
            if interpretation[self.variable]:
                result += power
            power <<= 1
        return result


    def __repr__(self):
        return self.variable


class Negation(Formula):
    def __init__(self, subformula):
        self.subformula = subformula
        Formula.__init__(self)

    def compute_truth_table(self):
        return ~self.subformula.truth_table & TRUTH_TABLE_MASK

    def compute_size(self):
        return self.subformula.size + 1

    def __repr__(self):
        return f"\\neg {self.subformula}"


class BinaryConnective(Formula):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs
        Formula.__init__(self)

    def compute_truth_table(self):
        return self.combine(self.lhs.truth_table, self.rhs.truth_table)

    def compute_size(self):
        return self.lhs.size + self.rhs.size + 3

    def __repr__(self):
        return f"({self.lhs} {self.symbol} {self.rhs})"


class Conjunction(BinaryConnective):
    symbol = "\\land"

    def combine(self, left, right):
        return left & right


class Disjunction(BinaryConnective):
    symbol = "\\lor"

    def combine(self, left, right):
        return left | right


class Implication(BinaryConnective):
    symbol = "\\rightarrow"

    def combine(self, left, right):
        return (~left | right) & TRUTH_TABLE_MASK


class Biimplication(BinaryConnective):
    symbol = "\\leftrightarrow"

    def combine(self, left, right):
        return (~(left ^ right)) & TRUTH_TABLE_MASK


def generate_atoms():
    for var in VARIABLES:
        yield Atom(var)


def combine_with(new_formula, other_formulas):
    yield Negation(new_formula)

    # Note: because of commutativity, we only generate one of the two
    # symmetric conjunctions/disjunctions/biimplications that we could.
    for other in other_formulas:
        yield Conjunction(new_formula, other)
        yield Disjunction(new_formula, other)
        yield Biimplication(new_formula, other)
        yield Implication(new_formula, other)
        yield Implication(other, new_formula)


def all_interpretations():
    for values in itertools.product([False, True], repeat=len(VARIABLES)):
        yield dict(zip(VARIABLES, values))


def find_all_shortest():
    def try_push(formula):
        size = formula.size
        tt = formula.truth_table
        old_formula = truth_table_to_formula.get(tt)
        if old_formula is None or size < old_formula.size:
            truth_table_to_formula[tt] = formula
            heapq.heappush(heap, (size, tt))
    def pop():
        return heapq.heappop(heap)
    def log_formula(tt, formula):
        tt_string = f"{tt:>0{TRUTH_TABLE_SIZE}b}"
        size = formula.size
        log(f"best for {tt_string}: size {size}: {formula}")
    heap = []
    truth_table_to_formula = {}
    best_formulas = set()
    for atom in generate_atoms():
        try_push(atom)

    while heap:
        size, tt = pop()
        formula = truth_table_to_formula[tt]
        if size == formula.size:
            assert truth_table_to_formula[tt] == formula
            best_formulas.add(formula)
            log_formula(tt, formula)
            for succ_formula in combine_with(formula, best_formulas):
                try_push(succ_formula)
    assert len(best_formulas) == (1 << TRUTH_TABLE_SIZE)

    sum_of_sizes = sum(formula.size for formula in best_formulas)
    log(f"sum of sizes: {sum_of_sizes}")


if __name__ == "__main__":
    find_all_shortest()
