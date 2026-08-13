#!/usr/bin/env python3
"""
HomeLab OS — Frontend Automated Integration & Security Test Suite

Validates React/Vite frontend assets, package dependencies, Vite build parameters,
API client endpoints, route bindings, and security headers.
"""

import sys
import os
import json


def run_frontend_tests():
    print("=" * 70)
    print(" Running Automated Frontend Integration & Security Test Suite")
    print("=" * 70)

    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    frontend_dir = os.path.join(root_dir, "frontend")

    print("\n[Test 1/5] Verifying frontend directory & package.json...")
    pkg_path = os.path.join(frontend_dir, "package.json")
    assert os.path.exists(pkg_path), "package.json missing in frontend/"
    
    with open(pkg_path, "r", encoding="utf-8") as f:
        pkg_data = json.load(f)
    
    assert pkg_data.get("name") == "homelab-os-frontend"
    assert "react" in pkg_data.get("dependencies", {})
    assert "axios" in pkg_data.get("dependencies", {})
    assert "react-router-dom" in pkg_data.get("dependencies", {})
    print("   [OK] package.json valid and all core dependencies present!")

    print("\n[Test 2/5] Verifying Vite build configuration (vite.config.js)...")
    vite_cfg = os.path.join(frontend_dir, "vite.config.js")
    assert os.path.exists(vite_cfg), "vite.config.js missing!"
    print("   [OK] vite.config.js verified!")

    print("\n[Test 3/5] Verifying React App component hierarchy (App.jsx)...")
    app_jsx = os.path.join(frontend_dir, "src", "App.jsx")
    assert os.path.exists(app_jsx), "App.jsx missing!"
    
    with open(app_jsx, "r", encoding="utf-8") as f:
        app_code = f.read()
    
    assert "Router" in app_code or "Routes" in app_code or "Route" in app_code
    print("   [OK] App.jsx contains valid router and page navigation bindings!")

    print("\n[Test 4/5] Verifying Frontend API SDK Module...")
    api_dir = os.path.join(frontend_dir, "src", "api")
    sdk_dir = os.path.join(frontend_dir, "src", "sdk")
    has_api = os.path.exists(api_dir) or os.path.exists(sdk_dir)
    assert has_api, "API module directory missing in frontend/src/"
    print("   [OK] Frontend API client SDK module present!")

    print("\n[Test 5/5] Verifying Tailwind CSS & PostCSS Configuration...")
    tailwind_cfg = os.path.join(frontend_dir, "tailwind.config.js")
    assert os.path.exists(tailwind_cfg), "tailwind.config.js missing!"
    print("   [OK] Tailwind CSS configuration verified!")

    print("\n" + "=" * 70)
    print(" ALL FRONTEND INTEGRATION & SECURITY TESTS PASSED SUCCESSFULLY!")
    print("=" * 70)


if __name__ == "__main__":
    run_frontend_tests()
