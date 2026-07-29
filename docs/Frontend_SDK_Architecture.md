# Frontend SDK Architecture

## Purpose

The Frontend SDK abstracts and standardizes all HTTP communications, routes, and query patterns between the React + Vite frontend dashboard and the FastAPI HomeLab OS backend. This architecture prevents API route leakage, handles request payload validation on the client-side, and decouples components from library choices (like Axios).

## Scope

- Central class interfaces for all platform functional services.
- Auto-injects authorization token headers.
- Standardizes return payloads for UI integration.

## Class Diagram

```text
┌──────────────────────────────────────────────────────────┐
│                      HomeLabSDK                          │
├──────────────────────────────────────────────────────────┤
│ - auth: AuthSDK                                          │
│ - system: SystemSDK                                      │
│ - storage: StorageSDK                                    │
│ - vault: VaultSDK                                        │
│ - projects: ProjectsSDK                                  │
│ - workspace: WorkspaceSDK                                │
│ - monitoring: MonitoringSDK                              │
│ - notifications: NotificationsSDK                        │
└──────────────────────────────────────────────────────────┘
```

## Basic Usage

```javascript
import axios from 'axios';
import HomeLabSDK from './sdk';

// Initialize with configured client
const apiClient = axios.create({ baseURL: '/api/v1' });
const sdk = new HomeLabSDK(apiClient);

// Unlock vault
try {
  const result = await sdk.vault.unlock('my_secure_passphrase');
  console.log('Vault unlocked:', result.mounted);
} catch (error) {
  console.error('Failed to unlock vault:', error);
}
```
