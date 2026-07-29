# Storage & Vault API Documentation

## Storage Endpoints

### 1. List Devices
- **Endpoint**: `GET /api/v1/storage/devices`
- **Response**:
  ```json
  [
    {
      "id": "5bc8370f-15ba-411a-8fba-22b0a9db900d",
      "name": "/dev/sda",
      "uuid": "5bc8370f-15ba-411a-8fba-22b0a9db900d",
      "filesystem": "ext4",
      "capacity_gb": 240.0,
      "type": "SSD",
      "status": "active"
    }
  ]
  ```

### 2. Device Details
- **Endpoint**: `GET /api/v1/storage/devices/{id}`

### 3. Storage Health
- **Endpoint**: `GET /api/v1/storage/health`

### 4. Mount Partition
- **Endpoint**: `POST /api/v1/storage/mount/{id}?mount_point={path}`

### 5. Unmount Partition
- **Endpoint**: `POST /api/v1/storage/unmount/{id}`

---

## Vault Endpoints

### 1. Vault Status
- **Endpoint**: `GET /api/v1/vault/status`

### 2. Unlock Vault
- **Endpoint**: `POST /api/v1/vault/unlock`
- **Body**:
  ```json
  {
    "password": "passphrase_string"
  }
  ```

### 3. Lock Vault
- **Endpoint**: `POST /api/v1/vault/lock`
