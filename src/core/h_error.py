import sys
import colorama
import warnings

class HascalError:
    def __init__(self, exception_message):
        colorama.init()
        sys.stderr.write(colorama.Fore.RED+"Error : ")
        sys.stderr.write(colorama.Style.RESET_ALL)
        sys.stderr.write(exception_message)
        sys.stderr.write("\n")
        sys.exit(1)

class HascalWarning:
    def __init__(self, warning_message):
        colorama.init()
        warnings.warn(colorama.Fore.YELLOW+"Warning : "+colorama.Style.RESET_ALL+warning_message)
