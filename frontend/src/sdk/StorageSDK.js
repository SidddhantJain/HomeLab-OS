/**
 * Storage and Partition SDK Sub-module
 */
class StorageSDK {
  constructor(apiClient) {
    this.client = apiClient;
  }

  async listDevices() {
    const response = await this.client.get('/storage/devices');
    return response.data;
  }

  async getDeviceDetails(id) {
    const response = await this.client.get(`/storage/devices/${id}`);
    return response.data;
  }

  async getHealth() {
    const response = await this.client.get('/storage/health');
    return response.data;
  }

  async mountDevice(id, mountPoint = '/mnt/homelab-storage') {
    const response = await this.client.post(`/storage/mount/${id}`, null, {
      params: { mount_point: mountPoint }
    });
    return response.data;
  }

  async unmountDevice(id) {
    const response = await this.client.post(`/storage/unmount/${id}`);
    return response.data;
  }
}

export default StorageSDK;

