import pytest
import subprocess
import os
from pathlib import Path

base_path = Path(os.path.dirname(os.path.abspath(__file__))) / ".."
sacalon_path = base_path / "dist" / "sacalon"

if not sacalon_path.exists():
    pytest.xfail("first build sacalon, then run tests: `make build`")
 

@pytest.mark.parametrize(
    "case",
    [
        "fibonacci.sa",
        "for_in.sa",
        "format.sa",
        "func.sa",
        "funcp.sa",
        # "get.sa",
        "hello.sa",
        "linear_regression.sa",
        "mem.sa",
        "multiline.sa",
        "null_in_arth.sa",
        "path.sa",
        "print_array.sa",
        "print_struct.sa",
        "ptr.sa",
        "read_from_stdin.sa",
        "regex.sa",
        "return_at_end.sa",
        "scope.sa",
        "sha256.sa",
        "sizeof.sa",
        "static.sa",
        "struct_inheritance.sa",
        "test.sa",
        "typeof.sa",
        # "fail/incomplete_type.sa",
        # "fail/op_error_on_string.sa",
        # "fail/return_at_end.sa",
        # "fail/static.sa",
        # "fail/null/1.sa",
        # "fail/null/2.sa",
        # "fail/null/3.sa",
        # "fail/null/4.sa",
        # "fail/null/5.sa",
        # "fail/null/6.sa",
    ],
)
def test_sacalon(case):
    assert subprocess.Popen(f"{sacalon_path} {base_path}/tests/{case}", shell=True).wait() == 0

