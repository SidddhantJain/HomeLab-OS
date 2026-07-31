/**
 * Download Manager SDK Sub-module
 */
class DownloadSDK {
  constructor(apiClient) {
    this.client = apiClient;
  }

  async listDownloads() {
    const response = await this.client.get('/downloads');
    return response.data;
  }

  async enqueueDownload(url, destination) {
    const response = await this.client.post('/downloads', { url, destination });
    return response.data;
  }
}

export default DownloadSDK;
