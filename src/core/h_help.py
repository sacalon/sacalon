import platform
from sys import exit

HASCAL_COMPILER_VERSION = "1.4.1"
HASCAL_GITHUB_REPO = "https://github.com/hascal/hascal"


def help_all():
    output_message = [
        f"Hascal Compiler {HASCAL_COMPILER_VERSION} {str(platform.system()).lower()}/{str(platform.machine()).lower()}",
        "Copyright (c) 2019-2023 Hascal Foundation,",
        "All rights reserved.",
        "\nEnter following command to compile a Hascal program :",
        "\thascal <inputfile.has> [output file name]",
        "other commands:",
        "\thelp: show help",
        "\tversion : show version",
        "\tinit : create new config.json file",
        "\tbuild : build project",
        "\trun : run project",
        "\tget <package url(git repository)> : install a package",
        "\tupdate <package url(git repository)> : update a package",
    ]
    for line in output_message:
        print(line)
    exit(0)


def help_short():
    output_message = [
        f"Hascal Compiler {HASCAL_COMPILER_VERSION} {str(platform.system()).lower()}/{str(platform.machine()).lower()}",
        "Copyright (c) 2019-2023 Hascal Foundation,",
        "All rights reserved.",
        "\nEnter following command to compile a Hascal program :",
        "\thascal <inputfile.has> [output file name]",
        "to show other commands enter following command :",
        "\thascal help",
    ]
    for line in output_message:
        print(line)
    exit(0)