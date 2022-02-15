from math import inf, nan
from typing_extensions import Self
from integral_base_convert import convert as convert_i
from fractional_base_convert import convertString as convert_f


class IEEE754_32():

    EXPONENT_BIAS = 127

    def fromValue(value: float) -> Self:
        exp = 0
        sign = int(value<0)
        mantissa = abs(value)
        while int(mantissa) > 1:
            mantissa /= 2
            exp += 1
        mantissa = mantissa if mantissa<1.0 else mantissa-1.0
        mantissa = round(mantissa, 7)
        biasedExponent = exp + IEEE754_32.EXPONENT_BIAS
        return IEEE754_32(sign, biasedExponent, mantissa)

    def fromIntegral(intVal):
        sign = intVal >> 31
        biasedExponent = (intVal>>23) & 0xff
        mantissaStr_int = '{:0>23}'.format(convert_i(intVal & 0x7fffff, 2))
        mantissaStr_float = '.'+convert_f(mantissaStr_int, 2, 10, 23)
        return IEEE754_32(sign, biasedExponent, float(mantissaStr_float))

    def __init__(self, sign: int, biasedExponent: int, mantissa: float) -> None:
        self._sign = sign
        self._exponentBiased = biasedExponent
        self._mantissa = mantissa

    def sign(self):
        return self._sign

    def exponentBiased(self):
        return self._exponentBiased

    def exponentUnbiased(self):
        return self._exponentBiased-IEEE754_32.EXPONENT_BIAS

    def mantissa(self):
        return self._mantissa

    def isNormalized(self):
        return not (self._exponentBiased==0 and self._mantissa!=0)

    def value(self):
        if self._exponentBiased==255:
            if self._mantissa==0:
                return (-1)**self._sign * inf
            return nan
        elif self._exponentBiased==0 and self._mantissa==0:
            return 0.0
        return (
            (-1)**self._sign
            * (2**self.exponentUnbiased())
            * ((1.0 if self.isNormalized() else 0.0) + self._mantissa)
        )
