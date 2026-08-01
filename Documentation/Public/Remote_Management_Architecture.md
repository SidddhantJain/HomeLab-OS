# Remote Management Architecture

## Overview
Allows secure remote server administration from desktop, web, or mobile clients without exposing raw SSH ports.

## Core Layers
- **Remote API Gateway**: Controlled execution router.
- **Sandboxed Web Terminal**: Command pattern filter and execution sandbox.
- **2FA TOTP Layer**: Device registration & secret hash verification.
- **Remote File Manager**: Browsing and file operations restricted to allowed roots (`/projects`, `/storage`).
