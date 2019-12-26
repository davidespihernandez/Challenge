import math
from abc import ABC
from typing import List


class WrongExpression(Exception):
    pass


class NotIntegerSubexpression(Exception):
    pass


class WrongPowerExpressionArgs(Exception):
    pass


class IntegerNotInRange(Exception):
    pass


class BaseExpression(ABC):
    OPS = {
        "+": (lambda a, b: a + b),
        "-": (lambda a, b: a - b),
        "*": (lambda a, b: a * b),
        "/": (lambda a, b: a / b),
        "^": (lambda a, b: math.pow(a, b)),
    }

    def evaluate(self):
        pass

    def is_solution(self):
        pass


class RPNExpression(BaseExpression):
    def __init__(self, rpn_token_list: List, expected: int):
        self.rpn_token_list = rpn_token_list
        self.exception = None
        self.expected = expected
        self.expr_as_string = ""
        self.evaluated = None
        self.evaluate()

    def _eval_tokens(self, tokens):
        stack = []
        string_stack = []

        def check_power_exp_args(x, y):
            if abs(x) > 1 and abs(y) > 6:
                raise WrongPowerExpressionArgs(f"Wrong power expr: {x}^{y}")
            if abs(y) > 1 and abs(x) > 100:
                raise WrongPowerExpressionArgs(f"Wrong power expr: {x}^{y}")

        for token in tokens:
            if token in self.OPS:
                arg2 = stack.pop()
                arg1 = stack.pop()
                if token == "^":
                    check_power_exp_args(arg1, arg2)

                result = self.OPS[token](arg1, arg2)
                str_arg2 = string_stack.pop()
                str_arg1 = string_stack.pop()
                string_result = f"({str_arg1} {token} {str_arg2})"
                if result % 1 != 0:
                    raise NotIntegerSubexpression(f"Not integer result: {arg1}{token}{arg2}")
                stack.append(int(result))
                string_stack.append(string_result)
            else:
                if token < 1 or token > 10:
                    raise IntegerNotInRange(f"Integer not in range: {token}")
                stack.append(token)
                string_stack.append(str(token))

        if len(stack) > 1:
            raise WrongExpression("Wrong RPN expression")
        self.expr_as_string = string_stack.pop()
        return stack.pop()

    def evaluate(self):
        try:
            self.evaluated = self._eval_tokens(self.rpn_token_list)
        except Exception as e:
            self.exception = e
        return self.evaluated

    def is_solution(self):
        return self.evaluated == self.expected and not self.exception

    def __str__(self):
        return self.expr_as_string

    # TODO: add a method to rate how good is a solution, can be calculated while evaluating...
