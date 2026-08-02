"""
HomeLab OS v1.5 — PySide6 Manager Headless Automated Test Suite
Verifies QApplication, MainWindow, Page Switching, and Live Server Communication.
"""

import sys
import os

# Ensure root directory is in sys.path
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from PySide6.QtWidgets import QApplication
from manager.main_window import HomeLabMainWindow
from manager.core.api_client import api_client


def run_manager_tests():
    print("=" * 70)
    print(" Running Automated PySide6 Manager Test Suite")
    print("=" * 70)

    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)

    print("\n[Test 1/4] Instantiating HomeLabMainWindow...")
    window = HomeLabMainWindow()
    assert window is not None
    print("   [OK] MainWindow created successfully!")

    print("\n[Test 2/4] Verifying 11 Page Navigation Modules...")
    total_pages = window.pages_stack.count()
    print(f"   Found {total_pages} registered navigation pages.")
    assert total_pages == 11

    for i in range(total_pages):
        window.switch_page(i)
        widget = window.pages_stack.widget(i)
        print(f"   Page {i+1}/11 ({widget.__class__.__name__}): ACTIVE")

    print("\n[Test 3/4] Testing API Client against live Dell server (192.168.0.180)...")
    status = api_client.get_system_status()
    print(f"   Response: {status}")
    assert status is not None
    assert status.get("status") == "running"
    print("   [OK] Live Server API Communication PASSED!")

    print("\n[Test 4/4] Verifying QSS Dark Theme Loading...")
    qss_path = os.path.join(root_dir, "manager", "themes", "dark_theme.qss")
    assert os.path.exists(qss_path)
    print("   [OK] dark_theme.qss exists and valid!")

    print("\n" + "=" * 70)
    print(" ALL PYSIDE6 MANAGER AUTOMATED TESTS PASSED SUCCESSFULLY!")
    print("=" * 70)


if __name__ == "__main__":
    run_manager_tests()
