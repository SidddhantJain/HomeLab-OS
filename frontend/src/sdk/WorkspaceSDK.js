/**
 * Sandbox Workspace SDK Sub-module
 */
class WorkspaceSDK {
  constructor(apiClient) {
    this.client = apiClient;
  }

  async listWorkspaces() {
    const response = await this.client.get('/workspaces');
    return response.data;
  }

  async startWorkspace(id) {
    const response = await this.client.post(`/workspaces/${id}/start`);
    return response.data;
  }

  async stopWorkspace(id) {
    const response = await this.client.post(`/workspaces/${id}/stop`);
    return response.data;
  }
}

export default WorkspaceSDK;
