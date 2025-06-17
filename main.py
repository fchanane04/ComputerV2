import signal
import sys
import re

typ = "None"

variables = {}
functions = {}


def function_syntax_parser(function):
    #need to add check if all variables are the same
    function = re.sub(r'\s+', '', function)
    pattern = r'^[-+*/%^()0-9a-zA-Z]+$'
    if re.match(pattern, function):
        print("it's a valid function syntax")
    else:
        sys.exit("Invalid function syntax")

def variable_parser(variable):
    print(f"this is the name of the variable {variable}")
    if re.fullmatch(r'fun[A-Z]\([a-z]\)', variable):
        typ = "function"
        print("its a function")
    else:
        typ = "variable"
        print("its a variable")
    return typ

def parse_assignment(line):
    sides = line.split("=")
    if len(sides) != 2:
        sys.exit("Invalid input: expected one '='.")
    left, right = sides[0].strip(), sides[1].strip()
    if not left or not right:
        sys.exit("Invalid input: empty left or right side.")
    return left, right

def is_function_definition(left):
    return re.fullmatch(r'[a-zA-Z]+\([a-zA-Z]\)', left)

def parse_matrix(expr):
    try:
        content = expr[2:-2]
        rows = content.split(';')
        matrix = []
        for row in rows:
            matrix.append([float(x.strip()) for x in row.split(',')])
        return matrix
    except:
        return None

def parse_value(expr):
    expr = expr.replace('i', 'j')  # Convert imaginary i to Python's j
    if expr.startswith('[[') and expr.endswith(']]'):
        matrix = parse_matrix(expr)
        if matrix:
            return matrix
        else:
            print("Invalid matrix syntax.")
            return expr
    try:
        value = eval(expr, {}, variables)
        return value
    except:
        return expr  # return as raw string for now

def handle_assignment(left, right):
    if is_function_definition(left):
        fname = left[:left.index('(')].lower()
        param = left[left.index('(') + 1 : left.index(')')]
        functions[fname] = {"param": param, "expression": right}
        print(f"[Function] {fname}({param}) = {right}")
    else:
        name = left.lower()
        val = parse_value(right)
        variables[name] = val
        print(f"[Variable] {name} = {val}")

def handle_expression(expr):
    expr = expr.replace('i', 'j')  #complex format
    try:
        result = eval(expr, {}, variables)
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error evaluating expression: {e}")

while True:
    try:
        line = input(">").strip()
        if not line:
            continue
        if line.endswith("= ?"):
            #in some cases "?" get stored as value
            expression = line[:-3].strip()
            print(expression)
            handle_expression(expression)
        else:
            left, right = parse_assignment(line)
            typ = variable_parser(left)
            if typ == "function":
                function_syntax_parser(right)
            print(typ)
            print(f"this is the value of the variable : |{right}|")
            handle_assignment(left, right)
    except KeyboardInterrupt:
        print("\nExiting.")
        break