#!/usr/bin/env python

import pytest

pytest_args = [
    "--cov",
    "--cov-branch",
    "--cov-report",
    "term",
    "-m",
    "not slow"
]

exit(pytest.main(pytest_args))