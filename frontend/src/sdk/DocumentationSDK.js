/**
 * Documentation Server SDK Sub-module
 */
class DocumentationSDK {
  constructor(apiClient) {
    this.client = apiClient;
  }

  async renderMarkdown(path) {
    const response = await this.client.get(`/documentation/render?path=${encodeURIComponent(path)}`);
    return response.data;
  }

  async searchDocs(query) {
    const response = await this.client.get(`/documentation/search?query=${encodeURIComponent(query)}`);
    return response.data;
  }
}

export default DocumentationSDK;
