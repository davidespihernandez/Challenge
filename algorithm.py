"""
Input:
    - numbers x1 to xn in [1, 10] and n in [5, 8]
    - number y in [1, 100]

The goal: use the numbers x to create a formula that results in y

[1, 5, 3, 6, 8] and 23
5 * 3 + 8 / 1 ^ 6

Constraints:
    The result of 0^0 is 1
    Every xi must be used exactly once! No other numbers are allowed
    The order of numbers and operators does not matter.
    No unary operators!
    Every operation must result in an integer
        Bad: (1 / 3) * 6
        Good: (6 / 3) * 1
    x^y
        if |x| > 1 then |y| <= 6
        if |y| > 1 then |x| <= 100
"""
from abc import ABC
from time import time
from typing import List
from generator import RPNExpressionGenerator


class WrongInputNumbers(Exception):
    pass


class AlgorithmResult(ABC):
    def __init__(self, total_expressions=0, elapsed_time=0):
        self.total_expressions = total_expressions
        self.elapsed_time = elapsed_time

    def verbose(self):
        to_print = [f"Elapsed {self.elapsed_time}ms",
                    f"Total expressions tested {self.total_expressions}"]
        return "\n".join(to_print)


class NoSolutionResult(AlgorithmResult):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __str__(self):
        return ""


class SingleSolutionResult(AlgorithmResult):
    def __init__(self, expression, **kwargs):
        super().__init__(**kwargs)
        self.expression = expression

    def __str__(self):
        return str(self.expression)

    def verbose(self):
        to_print = [super().verbose(),
                    f"Solution: {self.__str__()}"]
        return "\n".join(to_print)


class AllSolutionsResult(AlgorithmResult):
    def __init__(self, expressions: List, **kwargs):
        super().__init__(**kwargs)
        self.expressions = expressions

    def __str__(self):
        all_expressions = '\n'.join(self.expressions)
        return f"{all_expressions}"

    def verbose(self):
        to_print = [super().verbose(),
                    f"{len(self.expressions)} solutions found:",
                    f"{self.__str__()}"]
        return "\n".join(to_print)


class BaseAlgorithm(ABC):
    GENERATOR: None

    def __init__(self, max_execution_time=1000, stop_on_first=True):
        self.max_execution_time = max_execution_time
        self.stop_on_first = stop_on_first

    def solve(self, expression: str):
        pass

    def validate_input_numbers(self, expression: str):
        numbers = [int(v.strip()) for v in expression.split(",")]
        expected: int = int(numbers.pop())
        if len(numbers) < 5 or len(numbers) > 8:
            raise WrongInputNumbers
        if expected < 1 or expected > 100:
            raise WrongInputNumbers
        return numbers, expected


class RPNAlgorithm(BaseAlgorithm):
    GENERATOR = RPNExpressionGenerator

    def solve(self, expression: str):
        tested: int = 0
        try:
            numbers, expected = self.validate_input_numbers(expression)
        except WrongInputNumbers:
            return NoSolutionResult()
        solutions = {}
        generator = self.GENERATOR(numbers, expected)
        start = time()
        result = NoSolutionResult()
        elapsed = 0
        for expression in generator.generate_expressions():
            tested += 1
            elapsed: float = (time() - start) * 1000
            if expression.is_solution():
                if self.stop_on_first:
                    result = SingleSolutionResult(expression)
                    break
                solutions[str(expression)] = expression
            if elapsed > self.max_execution_time:
                break
        if len(solutions) > 0:
            result = AllSolutionsResult(list(solutions.keys()))
        result.elapsed_time = int(elapsed)
        result.total_expressions = tested
        return result
