#!/usr/bin/env bash
set -eo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "=========================================="
echo "    HomeLab OS Pre-Commit Security Scan   "
echo "=========================================="

FAILED=0

cd "$ROOT_DIR"

# 1. Verify Git status for tracked/staged .env files
echo -n "[1/4] Checking for tracked .env secret files... "
TRACKED_ENV=$(git ls-files | grep -E "^\.env$|\.env\." | grep -v "\.env\.example" || true)
if [ -n "$TRACKED_ENV" ]; then
    echo "FAILED!"
    echo "  -> CRITICAL SECURITY VIOLATION: Sensitive file tracked in Git:"
    echo "$TRACKED_ENV"
    FAILED=1
else
    echo "PASSED"
fi

# 2. Check for private SSH/RSA keys
echo -n "[2/4] Checking for private RSA/SSH keys & certificates... "
TRACKED_KEYS=$(git ls-files | grep -E "\.pem$|\.key$|\.crt$" || true)
if [ -n "$TRACKED_KEYS" ]; then
    echo "FAILED!"
    echo "  -> CRITICAL SECURITY VIOLATION: Key file tracked in Git:"
    echo "$TRACKED_KEYS"
    FAILED=1
else
    echo "PASSED"
fi

# 3. Scan for exposed private secrets in tracked files
echo -n "[3/4] Scanning tracked files for secret patterns... "
SECRET_MATCHES=$(git grep -i -E "BEGIN (RSA|OPENSSH|EC|PRIVATE) KEY|AWS_SECRET_ACCESS_KEY|SECRET_KEY\s*=\s*['\"][^'\"]{10,}['\"]" -- ':!scripts/security_scan.sh' ':!.env.example' ':!docs/' || true)
if [ -n "$SECRET_MATCHES" ]; then
    echo "FAILED!"
    echo "  -> POTENTIAL SECRET EXPOSURE DETECTED:"
    echo "$SECRET_MATCHES"
    FAILED=1
else
    echo "PASSED"
fi

# 4. Check Documentation/Private gitignore protection
echo -n "[4/4] Verifying Documentation/Private/ protection... "
if git check-ignore -q Documentation/Private/sample.txt 2>/dev/null || git check-ignore -q Documentation/Private/; then
    echo "PASSED (Documentation/Private is protected)"
else
    echo "FAILED!"
    echo "  -> Documentation/Private/ IS NOT PROPERLY IGNORED BY GIT!"
    FAILED=1
fi

echo "=========================================="
if [ "$FAILED" -eq 0 ]; then
    echo "SECURITY SCAN PASSED: Repository is clean and safe to commit."
    exit 0
else
    echo "SECURITY SCAN FAILED: Sensitive data or security risks found!"
    echo "ABORTING COMMIT/PUSH. Please fix the violations listed above."
    exit 1
fi
