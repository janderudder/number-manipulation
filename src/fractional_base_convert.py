from typing import List
from os import path
import sys


## Help and messages utils
def programLaunchCommand():
    return 'python3 '+path.basename(sys.argv[0])


def help():
    print("""Usage:

  $ {} <VALUE> <INPUT_BASE> <OUTPUT_BASE>

        VALUE must be a fractional part."""
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



## Number and numeric string manipulation
def toSymbol(n: int) -> str:
    if n<10: return str(n)
    return chr(55+n)


def fromSymbol(symbol):
    value = ord(symbol)
    if value > 90:
        return value-87
    elif value > 64:
        return value-55
    else:
        return value-48


def toBase10(string, inBase) -> float:
    value = 0.0
    for i,symbol in enumerate(string):
        value += fromSymbol(symbol) * inBase**(-1-i)
    return value



## Main algorithm
def euclidian_f(fracPart: float, outBase: int, digitCountMax=12) -> List[int]:
    if fracPart == 0.0: return [0]
    intProducts = []
    value = fracPart
    for _ in range(digitCountMax):
        if value==0: break
        value *= outBase
        intPart = int(value)
        intProducts.append(intPart)
        value -= intPart
    return intProducts



## Algo driver function
def convert(valueString, inBase, outBase) -> str:
    valueB10 = toBase10(valueString, inBase)
    digits = euclidian_f(valueB10, outBase)
    symbols = map(toSymbol, digits)
    return ''.join(symbols)



## Global driver function
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

    print(convert(sys.argv[1], inBase, outBase))
