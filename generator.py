import itertools
from abc import ABC
from typing import List

from expression import BaseExpression, RPNExpression

"""
We receive all the numbers to operate with and the expected result.
As only binary operations are allowed and we're use Reverse Polish Notation,
we can generate an expression concatenating K operators to the numbers.
This K operators will be N - 1, where N is the total number of numbers in 
the expression.
All possible operators can be calculated with a cartesian product using
itertools
"""


def all_possible_operators_for(numbers: List):
    return itertools.product(BaseExpression.OPS.keys(), repeat=len(numbers) - 1)


class BaseGenerator(ABC):
    def __init__(self, numbers, expected):
        self.numbers = numbers
        self.expected = expected

    def generate_expressions(self):
        pass

    def _all_number_permutations(self):
        pass


class RPNExpressionGenerator(BaseGenerator):

    def __init__(self, numbers, expected):
        super().__init__(numbers, expected)
        self.operators = list(all_possible_operators_for(numbers))

    def _all_number_permutations(self):
        # there are 3 awards that rely on numbers order
        yield self.numbers
        self.numbers.sort(reverse=True)
        yield self.numbers
        self.numbers.sort()
        yield self.numbers
        # now return all permutations
        for permutation in itertools.permutations(self.numbers):
            yield permutation

    def generate_expressions(self):
        for permutation in self._all_number_permutations():
            for o in self.operators:
                expr_tokens = list(permutation)
                expr_tokens.extend(o)
                yield RPNExpression(rpn_token_list=expr_tokens,
                                    expected=self.expected)
