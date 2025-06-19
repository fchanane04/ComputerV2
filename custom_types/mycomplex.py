class MyComplex:
    def __init__(self, real=0, imag=0):
        self.real = float(real)
        self.imag = float(imag)

    def __add__(self, other):
        return MyComplex(self.real + other.real, self.imag + other.imag)

    def __sub__(self, other):
        return MyComplex(self.real - other.real, self.imag - other.imag)

    def __mul__(self, other):
        real = self.real * other.real - self.imag * other.imag
        imag = self.real * other.imag + self.imag * other.real
        return MyComplex(real, imag)

    def __truediv__(self, other):
        denom = other.real**2 + other.imag**2
        real = (self.real * other.real + self.imag * other.imag) / denom
        imag = (self.imag * other.real - self.real * other.imag) / denom
        return MyComplex(real, imag)

    def __eq__(self, other):
        return self.real == other.real and self.imag == other.imag

    def __str__(self):
        if self.imag == 0:
            return f"{self.real}"
        if self.real == 0:
            return f"{self.imag}i"
        sign = '+' if self.imag >= 0 else '-'
        return f"{self.real} {sign} {abs(self.imag)}i"
