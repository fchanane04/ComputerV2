import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from custom_types.mycomplex import MyComplex


from custom_types.mycomplex import MyComplex

a = MyComplex(3, 2)
b = MyComplex(1, -4)

print("a =", a)
print("b =", b)
print("a + b =", a + b)
print("a - b =", a - b)
print("a * b =", a * b)
print("a / b =", a / b)