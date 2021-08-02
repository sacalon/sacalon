# h_error.py
#
# The Hascal Programming Language
# Copyright 2019-2021 Hascal Development Team,
# all rights reserved.

# this module is written by @pranavbaburaj
class HascalException(object):
    def __init__(self, exception_message, exception_type="Exception",  line_number="[~]", details=""):
        self.exception_message = str(exception_message)
        self.exception_type = exception_type

        self.line_number = str(line_number)

        self.exception_detailed_info = str(details)

        self.__evoke_exception_message()

    def __evoke_exception_message(self):
        output_messages = [
            f"{self.exception_message}"
            f"{self.exception_detailed_info}"
        ]

        for element_index in range(len(output_messages)):
            print(output_messages[element_index])