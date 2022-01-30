from os import path
from typing import List
import math
import sys


## Utility used in help display and such
def programLaunchCommand():
    return 'python3 '+path.basename(sys.argv[0])


## ~-=^°~#
def help():
    print("""Usage:

    $ {0} <input value> <input base> <output_base>

Examples:

- Input is 9A in hexadecimal and we want to get it as decimal:

    $ {0} 9A 16 10

    output: 154

- Decimal 276.125 to binary:

    $ {0} 276.125 10 2

    output: 100010100.001

Note:
    The input value is a string, so it accepts hexadecimal characters.
""".format(programLaunchCommand()))



## A base is slightly more constrained here than what Python does by itself
def isValidBase(base):
    return base > 1 and base < 37



## Convert a numeric value to a character digit (10 -> 'A')
def toSymbol(n: int) -> str:
    if n<10: return str(n)
    return chr(55+n)



## value -> (integral part, fractional part)
def decomposeNumber(value):
    intPart = math.floor(value)
    fracPart= value-intPart
    return (intPart, fracPart)



## string -> (integral part, fractional part)
def decomposeString(string, base):
    comaPos = string.find('.')
    if comaPos == -1:
        string.find(',')
    if comaPos != -1:
        return (int(string[:comaPos], base), float('0.'+string[comaPos+1:]))
    else:
        return (int(string, base), float(0.0))



## Euclidian algorithm for the integral part: get the remainders
def euclidianInt(value: int, outBase: int, digitCountMax=16) -> List[int]:
    remainders = []
    for _ in range(digitCountMax):
        if value==0: break
        remainders.append(value % outBase)
        value //= outBase
    return remainders



## Euclidian algorithm for the fractional part: get the products
def euclidianFrac(fracPart: float, outBase: int, digitCountMax=12) -> List[int]:
    integralProducts = []
    for i in range(digitCountMax):
        if fracPart==0: break
        intPart,fracPart = decomposeNumber(fracPart * outBase)
        integralProducts.append(intPart)
    return integralProducts



## driver subprogram for the euclidian algorithm (integral)
def convertInt(value: int, outBase: int, digitCountMax) -> str:
    digits = euclidianInt(value, outBase, digitCountMax)
    digits.reverse()
    symbols = map(toSymbol, digits)
    return ''.join(symbols)



## driver subprogram for the euclidian algorithm (fractional)
def convertFrac(value: float, outBase: int, digitCountMax) -> str:
    fracPart = decomposeNumber(value)[1]
    digits = euclidianFrac(fracPart, outBase, digitCountMax)
    symbols = map(toSymbol, digits)
    return ''.join(symbols)



## ~-=^°~#
class HandleError:

    def argCount() -> int:
        print(f"Please enter an input number, its base, and the desired base for output.")
        print(f"For more info please enter: $ {programLaunchCommand()} --help")
        return -2

    def baseRange(name, value) -> int:
        print(f"Error: the {name} base is invalid ({value}).")
        print("Valid range: [2, 36].")
        return -3



## ~-=^°~#
if __name__ == '__main__':

    for arg in sys.argv:
        if arg == '--help' or arg == '-h' or arg == '-?':
            help()
            exit()

    if len(sys.argv) < 4:
        exit(HandleError.argCount())

    inBase = int(sys.argv[2])
    outBase= int(sys.argv[3])

    if not isValidBase(inBase):
        exit(HandleError.baseRange('input', inBase))
    elif not isValidBase(outBase):
        exit(HandleError.baseRange('output', outBase))


    intPart,fracPart = (0, 0.0)

    if inBase == 10:
        try:
            intPart, fracPart = decomposeNumber(float(sys.argv[1]))
        except ValueError as ex:
            print(ex)
            exit(-1)
    else:
        try:
            intPart, fracPart = decomposeString(sys.argv[1], inBase)
        except ValueError as ex:
            print(ex)
            exit(-3)


    intResult  = convertInt(intPart, outBase, 16)
    fracResult = convertFrac(fracPart, outBase, 12)

    if not fracResult:
        print(intResult)
    else:
        print(f'{intResult}.{fracResult}')
