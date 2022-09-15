import pytest
import subprocess
import os
from pathlib import Path

base_path = Path(os.path.dirname(os.path.abspath(__file__))) / ".."
hascal_path = base_path / "dist" / "hascal"

if not hascal_path.exists():
    pytest.xfail("first build hascal, then run tests: `make build`")


@pytest.mark.parametrize(
    "case",
    [
        "fibonacci.has",
        "for_in.has",
        "format.has",
        "func.has",
        "funcp.has",
        # "get.has",
        "hello.has",
        "linear_regression.has",
        "mem.has",
        "multiline.has",
        "null_in_arth.has",
        "path.has",
        "print_array.has",
        "print_struct.has",
        "ptr.has",
        "read_from_stdin.has",
        "regex.has",
        "return_at_end.has",
        "scope.has",
        "sha256.has",
        "sizeof.has",
        "static.has",
        "struct_inheritance.has",
        "test.has",
        "typeof.has",
        # "fail/incomplete_type.has",
        # "fail/op_error_on_string.has",
        # "fail/return_at_end.has",
        # "fail/static.has",
        # "fail/null/1.has",
        # "fail/null/2.has",
        # "fail/null/3.has",
        # "fail/null/4.has",
        # "fail/null/5.has",
        # "fail/null/6.has",
    ],
)
def test_hascal(case):
    assert subprocess.Popen(f"{hascal_path} {base_path}/tests/{case}", shell=True).wait() == 0

