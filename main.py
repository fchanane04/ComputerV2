import signal
import sys
import re

typ = "None"

def variable_parser(variable):
    print(f"this is the name of the variable {variable}")
    if re.fullmatch(r'fun[A-Z]\([a-z]\)', variable):
        typ = "function"
        print("its a function")
    else:
        typ = "variable"
        print("its a variable")

while True:
    line = input(">").strip()
    sides = line.split("=")
    if len(sides) != 2:
        sys.exit("its not good")
    if not sides[0]:
        sys.exit("its not good")
    if not sides[1]:
        sys.exit("its not good")
    sides[0] = sides[0].strip()
    sides[1] = sides[1].strip()
    variable_parser(sides[0])
    