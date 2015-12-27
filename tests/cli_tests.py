import os
import shutil
import contextlib

from nose.tools import istest, assert_equal
from spur import LocalShell
import tempman

_local = LocalShell()

@istest
def vendorizing_single_module_with_no_dependencies_grabs_one_module_file():
    with _vendorize_example("isolated-module") as project_path:
        result = _local.run(["python", os.path.join(project_path, "main.py")])
        assert_equal(b"('one', 1)", result.output.strip())

@contextlib.contextmanager
def _vendorize_example(example_name):
    path = os.path.join(os.path.dirname(__file__), "../examples", example_name)
    _clean_project(path)
    _local.run(["python-vendorize"], cwd=path)
    yield path


def _clean_project(path):
    vendor_path = os.path.join(path, "_vendor")
    if os.path.exists(vendor_path):
        shutil.rmtree(vendor_path)
