#!/usr/bin/env python3
"""
run_tests.py

Automated test runner for the E-Commerce Pets API.
Usage: python run_tests.py
"""

import subprocess
import sys
import os
from datetime import datetime


def main():
    project_root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_root)
    os.environ["TESTING"] = "true"

    print("=" * 60)
    print("E-Commerce Pets API - Test Suite")
    print(f"Run Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()

    result = subprocess.run([
        sys.executable, "-m", "pytest",
        "test/",
        "-v",
        "--tb=short",
        "-W", "ignore::DeprecationWarning",
    ], cwd=project_root)

    print()
    print("=" * 60)
    if result.returncode == 0:
        print("RESULT: ALL TESTS PASSED")
    else:
        print(f"RESULT: SOME TESTS FAILED (exit code: {result.returncode})")
    print("=" * 60)

    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
