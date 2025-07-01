def gcd(a, b):
    return a if b == 0 else gcd(b, a % b)

class Rational:
    def __init__(self, numerator, denominator=1):
        if denominator == 0:
            raise ValueError("Denominator cannot be zero")
        common = gcd(numerator, denominator)
        self.numerator = numerator // common
        self.denominator = denominator // common

    def __add__(self, other):
        other = self._convert(other)
        new_num = self.numerator * other.denominator + other.numerator * self.denominator
        new_den = self.denominator * other.denominator
        return Rational(new_num, new_den)

    def __sub__(self, other):
        other = self._convert(other)
        new_num = self.numerator * other.denominator - other.numerator * self.denominator
        new_den = self.denominator * other.denominator
        return Rational(new_num, new_den)

    def __mul__(self, other):
        other = self._convert(other)
        return Rational(self.numerator * other.numerator, self.denominator * other.denominator)

    def __truediv__(self, other):
        other = self._convert(other)
        return Rational(self.numerator * other.denominator, self.denominator * other.numerator)

    def __pow__(self, power):
        if not isinstance(power, int) or power < 0:
            raise ValueError("Power must be non-negative integer")
        return Rational(self.numerator ** power, self.denominator ** power)

    def __eq__(self, other):
        other = self._convert(other)
        return self.numerator == other.numerator and self.denominator == other.denominator

    def __lt__(self, other):
        other = self._convert(other)
        return self.numerator * other.denominator < other.numerator * self.denominator

    def _convert(self, other):
        if isinstance(other, int):
            return Rational(other)
        if not isinstance(other, Rational):
            raise TypeError(f"Unsupported type: {type(other)}")
        return other

    def __float__(self):
        return self.numerator / self.denominator

    def __str__(self):
        if self.denominator == 1:
            return str(self.numerator)
        return f"{self.numerator}/{self.denominator}"

    def __repr__(self):
        return f"Rational({self.numerator}, {self.denominator})"