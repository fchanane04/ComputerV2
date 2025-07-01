import signal
import sys
import re

typ = "None"

variables = {}
functions = {}


def evaluate_expression(expr, context=None):
    if context is None:
        context = {}
    
    # Handle simple cases first
    if expr.isdigit():
        return int(expr)
    
    # Handle variables
    if expr in variables:
        return variables[expr]
    
    # Handle basic operations
    for op in ['+', '-', '*', '/']:
        if op in expr:
            left, right = expr.split(op, 1)
            left_val = evaluate_expression(left.strip(), context)
            right_val = evaluate_expression(right.strip(), context)
            
            if op == '+':
                return left_val + right_val
            elif op == '-':
                return left_val - right_val
            elif op == '*':
                return left_val * right_val
            elif op == '/':
                return left_val / right_val
    
    return expr  # Fallback

def solve_equation(equation):
    # Simple quadratic solver for ax^2 + bx + c = 0
    if 'x^2' in equation:
        parts = equation.split('x^2')
        a = evaluate_expression(parts[0] or '1')
        
        remaining = parts[1].split('x')
        b = evaluate_expression(remaining[0] or '1')
        c = evaluate_expression(remaining[1].split('=')[0])
        
        discriminant = b**2 - 4*a*c
        if discriminant > 0:
            root1 = (-b + discriminant**0.5)/(2*a)
            root2 = (-b - discriminant**0.5)/(2*a)
            return [root1, root2]
        elif discriminant == 0:
            return [-b/(2*a)]
        else:
            real = -b/(2*a)
            imag = (-discriminant)**0.5/(2*a)
            return [MyComplex(real, imag), MyComplex(real, -imag)]
    
    # Linear equation case
    elif 'x' in equation:
        # Implement similar logic for bx + c = 0
        pass

def function_syntax_parser(function):
    #need to add check if all variables are the same
    print("function says yee")
    function = re.sub(r'\s+', '', function)
    pattern = r'^[-+*/%^()0-9a-zA-Z]+$'
    if re.match(pattern, function):
        print("it's a valid function syntax")
    else:
        sys.exit("Invalid function syntax")

def variable_parser(variable):
    #print(f"this is the name of the variable {variable}")
    if re.fullmatch(r'fun[A-Z]\([a-z]\)', variable):
        typ = "function"
        #print("its a function")
    else:
        typ = "variable"
        #print("its a variable")
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
        print(expr)
        content = expr[2:-2]
        print(content)
        rows = content.split("];[")
        matrix = []
        for row in rows:
            matrix.append([float(x.strip()) for x in row.split(',')])
        return matrix
    except:
        return None

def parse_value(expr):
    # Handle matrices first
    if expr.startswith('[['):
        return parse_matrix(expr)
    
    # Handle complex numbers
    if 'i' in expr:
        parts = expr.replace(' ', '').split('+')
        real = float(parts[0]) if parts[0] else 0
        imag = float(parts[1].replace('i', '')) if len(parts) > 1 else 0
        return MyComplex(real, imag)
    
    # Handle fractions
    if '/' in expr:
        num, den = map(int, expr.split('/'))
        return Rational(num, den)
    
    # Handle regular numbers
    try:
        if '.' in expr:
            return float(expr)
        return int(expr)
    except ValueError:
        return expr  # Return as string if not a number

def shorten_function(function):
    #not working good on all examples
    vars = re.findall(r'[+-]?\s*[a-zA-Z_]\w*', function)
    nums = re.sub(r'[+-]?\s*[a-zA-Z_]\w*', '', function)
    try: val = eval(nums)
    except: val = nums.strip()
    return str(val) + ''.join(' ' + v.strip() for v in vars)

def handle_assignment(left, right):
    if is_function_definition(left):
        fname = left[:left.index('(')].lower()
        param = left[left.index('(') + 1 : left.index(')')]
        right = shorten_function(right)
        functions[fname] = {"param": param, "expression": right}
        print(f"[Function] {fname}({param}) = {right}")
    else:
        #varA is not handled as vara : need to fix this
        name = left.lower()
        val = parse_value(right)
        variables[name] = val
        print(f"[Variable] {name} = {val}")

def handle_expression(expr):
    expr = expr.replace('i', 'j')  #complex format
    try:
        context = {**functions, **variables}
        result = eval(expr, {}, context)
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error evaluating expression: {e}")

print("EXIT : exit the program")
while True:
    try:
        line = input("> ").strip()
        if not line:
            continue
            
        if line.lower() == 'exit':
            break
            
        if '=' in line:
            if '?' in line:  # Equation solving
                equation = line.split('=')[0].strip()
                solutions = solve_equation(equation)
                print("Solutions:", solutions)
            else:  # Normal assignment
                left, right = line.split('=', 1)
                left = left.strip().lower()
                
                if '(' in left:  # Function
                    func_name = left.split('(')[0]
                    param = left.split('(')[1].split(')')[0]
                    functions[func_name] = {'param': param, 'expr': right.strip()}
                    print(f"Function {func_name}({param}) defined")
                else:  # Variable
                    value = evaluate_expression(right.strip())
                    variables[left] = value
                    print(f"{left} = {value}")
        else:
            result = evaluate_expression(line)
            print(result)
            
    except Exception as e:
        print(f"Error: {e}")

#when assigning to a variable a value with another variable the uppercase is conidered new variable
#need to work on when to calculate a variable using a function
#also in function : when using a variable stored it should be replaced by value