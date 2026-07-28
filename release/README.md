# HomeLab OS Release Management System

This directory manages official release metadata and compiled installation packages for HomeLab OS.

---

## 📁 Directory Structure

- `version.json`: Current release version information (SemVer format `Major.Minor.Patch`).
- `changelog-template.md`: Template for release notes.
- `packages/`: Directory where release tarballs and installer setup executables are stored.

---

## 📦 Packaging a Release

To compile a production release package for distribution to the deployment server:

```bash
# 1. Update version.json to new SemVer version
# 2. Package tarball release bundle into release/packages/
tar -czvf release/packages/homelab-os-v1.0.0.tar.gz \
    --exclude='.git' \
    --exclude='node_modules' \
    --exclude='.venv' \
    --exclude='Documentation/Private' \
    .
```
