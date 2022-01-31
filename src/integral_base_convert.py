from typing import List
from os import path
import sys


def programLaunchCommand():
    return 'python3 '+path.basename(sys.argv[0])


def help():
    print("""Usage:

    $ {0} <input value> <input base> <output_base>

Examples:

- Input is 9A in hexadecimal and we want to get it as decimal:

    $ {0} 9A 16 10

    output: 154

- Decimal 276 to binary:

    $ {0} 276 10 2

    output: 100010100

Note:
    The input value is a string, so it accepts hexadecimal characters.
""".format(programLaunchCommand()))


def isValidBase(base):
    return base > 1 and base < 37


def euclidian(value: int, outBase: int) -> List[int]:
    if value == 0: return [0]
    remaining = []
    while value != 0:
        remaining.append(value % outBase)
        value //= outBase
    return remaining


def toSymbol(n: int) -> str:
    if n<10: return str(n)
    return chr(55+n)


def convert(value, outBase) -> str:
    digits = euclidian(value, outBase)
    digits.reverse()
    symbols = map(toSymbol, digits)
    return ''.join(symbols)


def errorArgCount() -> int:
    print(f"Please enter an input number, its base, and the desired base for output.")
    print(f"For more info please enter: $ {programLaunchCommand()} --help")
    return -1


def errorBaseRange(name, value) -> int:
    print(f"Error: the {name} base is invalid ({value}).")
    print("Valid range: [2, 36].")
    return -2



if __name__ == '__main__':

    for arg in sys.argv:
        if arg == '--help' or arg == '-h' or arg == '-?':
            help()
            exit()

    if len(sys.argv) < 4:
        exit(errorArgCount())

    inBase  = int(sys.argv[2])
    outBase = int(sys.argv[3])

    if not isValidBase(inBase):
        exit(errorBaseRange('input', inBase))

    if not isValidBase(outBase):
        exit(errorBaseRange('output', outBase))

    try:
        inputBase10 = int(sys.argv[1], inBase)
    except ValueError as e:
        print(e)
        exit(-3)
    except:
        exit(-4)

    print(convert(inputBase10, outBase))
