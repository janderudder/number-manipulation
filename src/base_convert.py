from fractional_base_convert import euclidian_f, convert as convert_f, fromSymbol
from integral_base_convert import euclidian as euclidian_i, convert as convert_i, isValidBase
from os import path
import sys



# string -> (integral part, fractional part)
def decomposeString(strVal, base):
    comaPos = strVal.find('.')
    if comaPos == -1:
        strVal.find(',')
    if comaPos != -1:
        return (int(strVal[:comaPos], base), strVal[comaPos+1:])
    else:
        return (int(strVal, base), '0.0')



def programLaunchCommand():
    return 'python3 '+path.basename(sys.argv[0])



def help():
    print('<help>')



class HandleError:

    def argCount() -> int:
        print(f"Please enter an input number, its base, and the desired base for output.")
        print(f"For more info please enter: $ {programLaunchCommand()} --help")
        return -2

    def baseRange(name, value) -> int:
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

    intPart,fracPart = decomposeString(sys.argv[1], inBase)

    print(intPart, fracPart)

    intResult  = convert_i(intPart, outBase)
    fracResult = convert_f(fracPart, outBase, 12)

    if not fracResult:
        print(intResult)
    else:
        print(f'{intResult}.{fracResult}')
