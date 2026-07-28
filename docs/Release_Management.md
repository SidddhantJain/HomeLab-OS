# HomeLab OS Release Management

This document defines the release lifecycle and versioning policies for HomeLab OS.

---

## 🏷️ Versioning Format

HomeLab OS follows [Semantic Versioning (SemVer 2.0.0)](https://semver.org/):

```text
MAJOR . MINOR . PATCH
  │       │       │
  │       │       └─► Bug fixes & security patches
  │       └─────────► Feature additions & non-breaking enhancements
  └─────────────────► Breaking architectural changes
```

Example: `1.0.0`

---

## 📦 Release Package Contents

Every official release artifact must contain:
1. `version.json`: Release metadata (Version string, Release Date, Commit Hash, Target Compatibility).
2. `CHANGELOG.md`: Itemized record of Added, Changed, Fixed, and Security updates.
3. Source bundle (`backend/`, `frontend/`, `docker/`, `deployment/`, `scripts/`).

---

## 📋 Release Checklist

Before tagging a release:
- [ ] Run backend unit tests: `python -m pytest tests/backend`
- [ ] Run security scan: `bash scripts/security_scan.sh`
- [ ] Verify `Documentation/Private/` is ignored by Git
- [ ] Update `release/version.json` with new version number
- [ ] Append release notes to `CHANGELOG.md`
- [ ] Commit and push changes: `git push origin main`
