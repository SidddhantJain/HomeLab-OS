#!/usr/bin/env python3
"""
HomeLab OS — Master Full-Stack Test Suite Runner

Executes all automated tests across Backend (Pytest), PySide Manager,
Frontend SDK, and Security Auditors in a single unified run.
"""

import sys
import os
import subprocess

# Ensure UTF-8 stdout handling on Windows console
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def run_cmd(cmd, description):
    print("\n" + "=" * 70)
    print(f" [*] [RUNNING] {description}")
    print("=" * 70)
    res = subprocess.run(cmd, shell=True)
    if res.returncode == 0:
        print(f" [OK] [SUCCESS] {description} PASSED!")
        return True
    else:
        print(f" [FAIL] [ERROR] {description} FAILED with code {res.returncode}")
        return False


def main():
    print("==========================================================")
    print(" HomeLab OS Master Automated Quality & Security Suite")
    print("==========================================================")

    results = []

    # 1. Pytest Backend Suite
    results.append(("Pytest Backend Test Suite", run_cmd(f"{sys.executable} -m pytest tests/backend -q", "Pytest Backend Test Suite")))

    # 2. PySide6 Desktop Manager Suite
    results.append(("PySide6 Manager Desktop Test Suite", run_cmd(f"{sys.executable} scripts/test_pyside_manager.py", "PySide6 Manager Desktop Test Suite")))

    # 3. Frontend Integration Suite
    results.append(("Frontend Integration & Security Test Suite", run_cmd(f"{sys.executable} scripts/test_frontend_suite.py", "Frontend Integration & Security Test Suite")))

    # Summary
    print("\n" + "=" * 70)
    print(" MASTER TEST SUITE SUMMARY")
    print("=" * 70)
    all_passed = True
    for name, passed in results:
        status = "PASSED [OK]" if passed else "FAILED [FAIL]"
        print(f" • {name:<45}: {status}")
        if not passed:
            all_passed = False

    print("=" * 70)
    if all_passed:
        print(" ALL BACKEND, DESKTOP, AND FRONTEND TESTS PASSED CLEANLY!")
        sys.exit(0)
    else:
        print(" SOME TESTS FAILED. PLEASE REVIEW LOGS ABOVE.")
        sys.exit(1)


if __name__ == "__main__":
    main()

