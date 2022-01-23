from typing import List
from os import path
import math
import sys


def programLaunchCommand():
    return 'python3 '+path.basename(sys.argv[0])


def help():
    print("""Usage: <section not written yet>""")


def isValidBase(base):
    return base > 1 and base < 37


def toSymbol(n: int) -> str:
    if n<10: return str(n)
    return chr(55+n)


def errorArgCount() -> int:
    print(f"Please enter an input number and the desired base for output.")
    print(f"For more info please enter: $ {programLaunchCommand()} --help")
    return -1


def errorBaseRange(name, value) -> int:
    print(f"Error: the {name} base is invalid ({value}).")
    print("Valid range: [2, 36].")
    return -2


def decompose(value):
    intPart = math.floor(value)
    fracPart= value-intPart
    return (intPart, fracPart)


def euclidianFrac(fracPart: float, outBase: int, digitCountMax=12) -> List[int]:
    intProducts = []
    for i in range(digitCountMax):
        if fracPart==0: break
        fracPart *= outBase
        intPart,fracPart = decompose(fracPart)
        intProducts.append(intPart)
    return intProducts


def convert(value, outBase, digitCount):
    fracPart = decompose(value)[1]
    results = euclidianFrac(fracPart,outBase,digitCount)
    symbols = []
    for n in results:
        symbols.append(toSymbol(n))
    return ''.join(symbols)



if __name__ == '__main__':

    for arg in sys.argv:
        if arg == '--help' or arg == '-h' or arg == '-?':
            help()
            exit()

    if len(sys.argv) < 3:
        exit(errorArgCount())

    outBase = int(sys.argv[2])

    if not isValidBase(outBase):
        exit(errorBaseRange('output', outBase))

    if (len(sys.argv) < 4):
        digitCount = 12
    else:
        digitCount = int(sys.argv[3])

    try:
        inputBase10 = float(sys.argv[1])
    except ValueError as e:
        print(e)
        exit(-3)
    except:
        exit(-4)

    print(convert(inputBase10, outBase, digitCount))
