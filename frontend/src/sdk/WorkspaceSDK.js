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

  async createWorkspace(name, owner, description) {
    const response = await this.client.post('/workspaces', { name, owner, description });
    return response.data;
  }

  async archiveWorkspace(id) {
    const response = await this.client.post(`/workspaces/${id}/archive`);
    return response.data;
  }

  async restoreWorkspace(id) {
    const response = await this.client.post(`/workspaces/${id}/restore`);
    return response.data;
  }

  async deleteWorkspace(id) {
    const response = await this.client.delete(`/workspaces/${id}`);
    return response.data;
  }
}

export default WorkspaceSDK;

