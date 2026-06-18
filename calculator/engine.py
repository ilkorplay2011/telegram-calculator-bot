from simpleeval import simple_eval
from calculator.normalize import normalize
import re

def check_brackets(expr):
    stack = []
    for c in expr:
        if c == "(":
            stack.append(c)
        elif c == ")":
            if not stack:
                return False
            stack.pop()
    return len(stack) == 0

def implicit_multiplication(expr):
    expr = re.sub(r"(\d)\(", r"\1*(", expr)
    expr = re.sub(r"\)(\d)", r")*\1", expr)
    expr = re.sub(r"\)\(", r")*(", expr)

    return expr

def fix_brackets(expr):
    open_b = expr.count("(")
    close_b = expr.count(")")

    if close_b > open_b:
        return None

    return expr + ")" * (open_b - close_b)

def prepare(expr):
    expr = normalize(expr)
    expr = implicit_multiplication(expr)

    if not re.search(r"\d", expr):
        return None

    expr = fix_brackets(expr)
    if expr is None:
        return None

    if not check_brackets(expr):
        return None

    return expr

def calculate(expr):
    return simple_eval(expr)