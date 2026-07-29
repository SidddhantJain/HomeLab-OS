/**
 * System and Health SDK Sub-module
 */
class SystemSDK {
  constructor(apiClient) {
    this.client = apiClient;
  }

  async getStatus() {
    const response = await this.client.get('/system/status');
    return response.data;
  }

  async getHealth() {
    const response = await this.client.get('/system/health');
    return response.data;
  }
}

export default SystemSDK;
