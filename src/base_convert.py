from typing import Tuple
from os import path
import sys
from fractional_base_convert import convertString as convert_f
from integral_base_convert import convert as convert_i, isValidBase



def programLaunchCommand():
    return 'python3 '+path.basename(sys.argv[0])


def help():
    print('<help: should write that at some point>')



# string -> (integral part, fractional part)
def decomposeNumber(valueString: str) -> Tuple[str, str]:
    parts = valueString.partition('.')
    if parts[1] != '.':
        parts = valueString.partition(',')
    if parts[2] == '':
        return (parts[0], '0')
    return (parts[0], parts[2])




class HandleError:

    def argCount() -> int:
        print(f"Please enter an input number, its base, and the desired base for output.")
        print(f"For more info please enter: $ {programLaunchCommand()} --help")
        return -2

    def baseRange(name: str, value: int) -> int:
        print(f"Error: the {name} base is invalid ({value}).")
        print("Valid range: [2, 36].")
        return -3



if __name__ == '__main__':

    for arg in sys.argv:
        if arg == '--help' or arg == '-h' or arg == '-?':
            help()
            exit()

    if len(sys.argv) < 4:
        exit(HandleError.argCount())

    inBase  = int(sys.argv[2])
    outBase = int(sys.argv[3])

    if not isValidBase(inBase):
        exit(HandleError.baseRange('input', inBase))
    elif not isValidBase(outBase):
        exit(HandleError.baseRange('output', outBase))

    intPart,fracPart = decomposeNumber(sys.argv[1])

    intResult  = convert_i(int(intPart), outBase)
    fracResult = convert_f(fracPart, inBase, outBase, 23)

    if not fracResult:
        print(intResult)
    else:
        print(f'{intResult}.{fracResult}')
