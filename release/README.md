# HomeLab OS Release Management System

This directory manages official release metadata, compiled installation packages, and delivery channels for HomeLab OS.

---

## 📁 Directory Structure

- `version.json`: Current release version information (SemVer format `Major.Minor.Patch`).
- `changelog-template.md`: Template for release notes.
- `stable/`: Production-ready, fully validated release bundles.
- `beta/`: Staging releases for validation of new architecture modules.
- `nightly/`: Automatically generated developer packages built from `main`.
- `packages/`: Compiled archive directories.

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

---

## 🚀 Release Channels & Policies

### Release Channels
1. **Stable**: Upgraded only after passing all QA tests on physical hardware (Dell Inspiron 5558). Target interval: Monthly.
2. **Beta**: Contains new architecture changes. Intended for developer sandbox machines. Target interval: Bi-weekly.
3. **Nightly**: Built on every commit push to `main`. Unstable.

### Upgrade Policy
- Auto-run database, config, and Docker migrations during upgrades.
- Always create a temporary system configuration snapshot before starting.

### Rollback Policy
- If an update fails health-check criteria, restore the snapshot config, revert database tables, and point Docker services back to the previous stable images.
