/**
 * Metrics and Telemetry Monitoring SDK Sub-module
 */
class MonitoringSDK {
  constructor(apiClient) {
    this.client = apiClient;
  }

  async getMetrics() {
    const response = await this.client.get('/monitoring/metrics');
    return response.data;
  }

  async getAlerts() {
    const response = await this.client.get('/monitoring/alerts');
    return response.data;
  }
}

export default MonitoringSDK;
