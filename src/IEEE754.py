from typing import Tuple
from typing_extensions import Self


class IEEE754_32():

    EXPONENT_BIAS = 127

    def fromValue(value: float) -> Self:
        exp = 0
        sign = int(value<0)
        mantissa = abs(value)
        while int(mantissa) > 1:
            mantissa /= 2
            exp += 1
        exp += IEEE754_32.EXPONENT_BIAS
        return IEEE754_32(sign, exp, mantissa)

    def __init__(self, sign, exponent, mantissa) -> None:
        self._sign = int(sign)
        self._exponent = exponent
        self._mantis = mantissa

    def sign(self):
        return self._sign

    def exponent(self):
        return self._exponent

    def mantissa(self):
        return self._mantis

    def value(self):
        return (
            (-1)**self._sign
            * 2**(self._exponent - IEEE754_32.EXPONENT_BIAS)
            * self._mantis)
