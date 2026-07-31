/**
 * Snapshot Management SDK Sub-module
 */
class SnapshotSDK {
  constructor(apiClient) {
    this.client = apiClient;
  }

  async listSnapshots(projectId) {
    const response = await this.client.get(`/projects/${projectId}/snapshots`);
    return response.data;
  }

  async createSnapshot(projectId) {
    const response = await this.client.post(`/projects/${projectId}/snapshot`);
    return response.data;
  }

  async restoreSnapshot(snapshotId) {
    const response = await this.client.post(`/projects/snapshots/${snapshotId}/restore`);
    return response.data;
  }
}

export default SnapshotSDK;
