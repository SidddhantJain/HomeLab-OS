/**
 * Storage and Partition SDK Sub-module
 */
class StorageSDK {
  constructor(apiClient) {
    this.client = apiClient;
  }

  async listDisks() {
    const response = await this.client.get('/storage/disks');
    return response.data;
  }

  async mountDisk(diskId, mountPoint) {
    const response = await this.client.post('/storage/mount', { diskId, mountPoint });
    return response.data;
  }
}

export default StorageSDK;
