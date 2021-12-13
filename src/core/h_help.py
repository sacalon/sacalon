# Help Informations
#
# The Hascal Programming Language
# Copyright 2019-2022 Hascal Development Team,
# all rights reserved.
import platform

HASCAL_COMPILER_VERSION = "1.3.5"
HASCAL_GITHUB_REPO = "https://github.com/hascal/hascal"

def help_all():
    output_message = [
        f"Hascal Compiler {HASCAL_COMPILER_VERSION} {str(platform.system()).lower()}/{str(platform.machine()).lower()}",
        "Copyright (c) 2019-2022 Hascal Foundation,",
        "All rights reserved.",
        "\nEnter following command for compile a Hascal program :",
        "\thascal <inputfile.has> [output file name]",
        "other commands:",
        "\thelp: show help",
        "\tversion : show version",
        "\tinstall <library_name> : install a library",
        "\tupdate <library_name> : update a library",
        "\tuninstall <library_name> : uninstall a library",
    ]

    for line in output_message:
        print(line)

def help_short():
    output_message = [
        f"Hascal Compiler {HASCAL_COMPILER_VERSION} {str(platform.system()).lower()}/{str(platform.machine()).lower()}",
        "Copyright (c) 2019-2022 Hascal Foundation,",
        "All rights reserved.",
        "\nEnter following command for compile a Hascal program :",
        "\thascal <inputfile.has> [output file name]",
        "for show other commands:",
        "\thascal help",
    ]
    
    for line in output_message:
        print(line)