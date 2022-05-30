import sys
import colorama

class HascalError:
    def __init__(self, exception_message,filename=""):
        colorama.init()
        if filename == "" :
            sys.stderr.write(colorama.Fore.RED + "Error : ")
        else :
            sys.stderr.write(colorama.Back.BLUE + colorama.Fore.WHITE + filename + ".has::" 
                                + colorama.Style.RESET_ALL 
                                + colorama.Fore.RED + "\nError : ")
        sys.stderr.write(colorama.Style.RESET_ALL)
        sys.stderr.write(exception_message)
        sys.stderr.write("\n")
        sys.exit(1)

class HascalWarning:
    def __init__(self, warning_message,filename=""):
        colorama.init()

        if filename == "" :
            print(
                colorama.Fore.YELLOW
                + "Warning : "
                + colorama.Style.RESET_ALL
                + warning_message
            )
        else :
            print(
                colorama.Back.BLUE
                + colorama.Fore.WHITE 
                + filename 
                + ".has::" 
                + colorama.Style.RESET_ALL 
                + colorama.Fore.YELLOW
                + "\nWarning : "
                + colorama.Style.RESET_ALL
                + warning_message
            )
