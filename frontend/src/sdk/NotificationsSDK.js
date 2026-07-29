/**
 * Notification alerts SDK Sub-module
 */
class NotificationsSDK {
  constructor(apiClient) {
    this.client = apiClient;
  }

  async listNotifications() {
    const response = await this.client.get('/notifications');
    return response.data;
  }

  async markAsRead(notificationId) {
    const response = await this.client.post(`/notifications/${notificationId}/read`);
    return response.data;
  }
}

export default NotificationsSDK;
