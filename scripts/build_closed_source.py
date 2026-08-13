#!/usr/bin/env python3
"""
HomeLab OS — Closed-Source Obfuscation & Binary Packaging Compiler Script

Compiles Python backend services and PySide6 desktop manager into
standalone binary executables (.exe / .pyd / .so) using Nuitka and PyArmor,
ensuring zero plain-text source code is exposed in production releases.
"""

import sys
import os
import shutil
import subprocess
import argparse


def check_toolchain(tool: str) -> bool:
    """Checks if executable compiler tool is installed and available on PATH."""
    return shutil.which(tool) is not None


def compile_with_nuitka(target: str, output_dir: str, standalone: bool = True):
    """Compiles target Python module into C machine binary using Nuitka."""
    print(f"[*] Starting Nuitka C-extension binary compilation for: {target}")
    
    cmd = [
        sys.executable, "-m", "nuitka",
        "--follow-imports",
        "--remove-output",
        f"--output-dir={output_dir}"
    ]
    
    if standalone:
        cmd.append("--standalone")
    
    if sys.platform.startswith("win"):
        cmd.append("--windows-console-mode=disable")
    
    cmd.append(target)
    
    print(f"[RUN] {' '.join(cmd)}")
    try:
        res = subprocess.run(cmd, check=True)
        print(f"[SUCCESS] Nuitka compilation completed for {target}")
        return res.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Nuitka compilation failed: {e}")
        return False


def obfuscate_with_pyarmor(target_dir: str, output_dir: str):
    """Obfuscates target directory bytecode using PyArmor."""
    print(f"[*] Starting PyArmor byte-code obfuscation for: {target_dir}")
    
    cmd = ["pyarmor", "gen", "-O", output_dir, "-r", target_dir]
    print(f"[RUN] {' '.join(cmd)}")
    
    try:
        res = subprocess.run(cmd, check=True)
        print(f"[SUCCESS] PyArmor obfuscation completed for {target_dir}")
        return res.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] PyArmor obfuscation failed: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="HomeLab OS Closed-Source Binary Obfuscation Compiler")
    parser.add_argument("--mode", choices=["nuitka", "pyarmor", "dry-run"], default="dry-run", help="Compilation engine mode")
    parser.add_argument("--target-app", choices=["backend", "manager", "all"], default="all", help="Target component to compile")
    parser.add_argument("--output-dir", default="dist/closed_source", help="Output distribution directory")
    parser.add_argument("--clean", action="store_true", help="Clean build artifact cache")
    args = parser.parse_args()

    print("==========================================================")
    print(" HomeLab OS Closed-Source Binary Packaging Pipeline")
    print("==========================================================")
    print(f"Mode: {args.mode}")
    print(f"Target Component: {args.target_app}")
    print(f"Output Directory: {args.output_dir}")
    print(f"Python Platform: {sys.platform} ({sys.version.split()[0]})")
    print("----------------------------------------------------------")

    if args.clean and os.path.exists(args.output_dir):
        print(f"[*] Cleaning build directory: {args.output_dir}")
        shutil.rmtree(args.output_dir)

    os.makedirs(args.output_dir, exist_ok=True)

    if args.mode == "dry-run":
        print("[DRY-RUN] Checking compiler prerequisites...")
        nuitka_ok = check_toolchain("nuitka")
        pyarmor_ok = check_toolchain("pyarmor")
        gcc_ok = check_toolchain("gcc") or check_toolchain("cl")
        
        print(f" - Nuitka Installed: {nuitka_ok}")
        print(f" - PyArmor Installed: {pyarmor_ok}")
        print(f" - C/C++ Compiler Installed (GCC/MSVC): {gcc_ok}")
        print("[DRY-RUN] Validation complete. Pass --mode=nuitka or --mode=pyarmor to trigger build.")
        sys.exit(0)

    success = True
    if args.mode == "nuitka":
        if args.target_app in ["manager", "all"]:
            success &= compile_with_nuitka("manager/main.py", os.path.join(args.output_dir, "manager"))
        if args.target_app in ["backend", "all"]:
            success &= compile_with_nuitka("backend/app/main.py", os.path.join(args.output_dir, "backend"))

    elif args.mode == "pyarmor":
        if args.target_app in ["manager", "all"]:
            success &= obfuscate_with_pyarmor("manager", os.path.join(args.output_dir, "manager"))
        if args.target_app in ["backend", "all"]:
            success &= obfuscate_with_pyarmor("backend/app", os.path.join(args.output_dir, "backend"))

    if success:
        print(f"\n[DONE] Production closed-source build generated successfully in '{args.output_dir}'")
        sys.exit(0)
    else:
        print("\n[FAIL] Closed-source build encountered errors.")
        sys.exit(1)


if __name__ == "__main__":
    main()
