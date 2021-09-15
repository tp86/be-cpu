#!/usr/bin/env python

import pytest

pytest_args = [
    "--cov",
    "--cov-branch",
    "--cov-report",
    "term",
    "--cov-report",
    "xml",
    # "-m",
    # "not slow"
]

exit(pytest.main(pytest_args))
