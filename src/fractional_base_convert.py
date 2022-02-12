from typing import List
from os import path
import sys


## Help and messages utils
def programLaunchCommand():
    return 'python3 '+path.basename(sys.argv[0])


def help():
    print("""Usage:

  $ {0} <VALUE> <INPUT_BASE> <OUTPUT_BASE>

  VALUE must be a fractional part.

Example:

  To convert decimal 0.625 to hex, input:

  $ {0} 625 10 16
        """
    .format(programLaunchCommand()))



## Input error checking
def isValidBase(base):
    return base > 1 and base < 37


def errorArgCount() -> int:
    print(f"Please enter an input number and the desired base for output.")
    print(f"For more info please enter: $ {programLaunchCommand()} --help")
    return -1


def errorBaseRange(name, value) -> int:
    print(f"Error: the {name} base is invalid ({value}).")
    print("Valid range: [2, 36].")
    return -2



## Number, list and numeric-string manipulation helpers
def toSymbol(n: int) -> str:
    if n<10: return str(n)
    return chr(55+n)


def toValue(symbol: str):
    code = ord(symbol)
    if code > 90:
        return code-87
    elif code > 64:
        return code-55
    else:
        return code-48


def strToBase10_f(string: str, inBase: int) -> float:
    if inBase==10:
        return float('.'+string)
    value = 0.0
    for i,symbol in enumerate(string):
        symbolValue = toValue(symbol)
        if symbolValue>=inBase:
            raise ValueError(f"Symbol out of base range: symbol {symbol}, base {inBase}")
        value += symbolValue * inBase**(-1-i)
    return value


def removeTrailingZeros(digits: List[int]) -> List[int]:
    index = 0
    for digit in reversed(digits):
        if digit != 0: break
        else: index+=1
    return digits[:len(digits)-index]



## Principal algorithm
def euclidian_f(fracPart: float, outBase: int, digitCountMax) -> List[int]:
    if fracPart == 0.0:
        return [0]
    productsUnits = []
    value = fracPart
    for _ in range(digitCountMax):
        if value==0: break
        value *= outBase
        intPart = int(value)
        productsUnits.append(intPart)
        value -= intPart
    return productsUnits



## Logic driver function
## @param value should be of form 0.xxxx
def convert(value: float, outBase: int, digitsCountMax: int) -> str:
    if value >= 1.0:
        raise ValueError(f"fractional part value must be < 1 ({value} given).")
    digits = euclidian_f(value, outBase, digitsCountMax)
    digits = removeTrailingZeros(digits) if len(digits)>1 else digits
    symbols = map(toSymbol, digits)
    return ''.join(symbols)



## even higher level driver
def convertString(valueString: str, inBase: int, outBase: int, digitsCountMax: int) -> str:
    value = strToBase10_f(valueString, inBase)
    return convert(value, outBase, digitsCountMax)



## CLI driver function
if __name__ == '__main__':

    for arg in sys.argv:
        if arg == '--help' or arg == '-h' or arg == '-?':
            help()
            exit()

    if len(sys.argv) < 4:
        exit(errorArgCount())

    inBase = int(sys.argv[2])
    outBase = int(sys.argv[3])

    if not isValidBase(inBase):
        exit(errorBaseRange('input', inBase))

    if not isValidBase(outBase):
        exit(errorBaseRange('output', outBase))

    try:
        print(convertString(sys.argv[1], inBase, outBase, 23))

    except Exception as ex:
        print(ex)
        exit(-1)
