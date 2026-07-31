/**
 * Backup Service SDK Sub-module
 */
class BackupSDK {
  constructor(apiClient) {
    this.client = apiClient;
  }

  async listBackupJobs() {
    const response = await this.client.get('/backup/jobs');
    return response.data;
  }

  async triggerBackup(name, source, destination) {
    const response = await this.client.post('/backup/jobs', { name, source, destination });
    return response.data;
  }
}

export default BackupSDK;
