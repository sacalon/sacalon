import sys
import colorama
class HascalException():
    def __init__(self, exception_message):
        colorama.init()
        sys.stderr.write(colorama.Fore.RED+"Error : ")
        sys.stderr.write(colorama.Style.RESET_ALL)
        sys.stderr.write(exception_message)
        sys.stderr.write("\n")
        sys.exit(1)