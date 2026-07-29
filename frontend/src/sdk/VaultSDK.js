/**
 * Vault Encryption SDK Sub-module
 */
class VaultSDK {
  constructor(apiClient) {
    this.client = apiClient;
  }

  async getStatus() {
    const response = await this.client.get('/vault/status');
    return response.data;
  }

  async unlock(password) {
    const response = await this.client.post('/vault/unlock', { password });
    return response.data;
  }

  async lock() {
    const response = await this.client.post('/vault/lock');
    return response.data;
  }
}

export default VaultSDK;
