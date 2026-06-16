import re

def normalize(expr):
    expr = expr.replace("×", "*")
    expr = expr.replace("÷", "/")
    expr = expr.replace(",", ".")
    expr = expr.replace("^", "**")
    expr = re.sub(r"\+\+", "+", expr)
    expr = re.sub(r"--", "+", expr)
    expr = re.sub(r"\+\-", "-", expr)
    expr = re.sub(r"-\+", "-", expr)
    expr = re.sub(r"^[\+\×\÷]", "", expr)
    expr = re.sub(r"(\d+)k", r"(\1*1000)", expr)
    expr = re.sub(r"(\d+)m", r"(\1*1000000)", expr)
    expr = re.sub(r"(\d+)b", r"(\1*1000000000)", expr)
    return expr