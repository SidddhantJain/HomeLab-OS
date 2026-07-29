/**
 * Authentication SDK Sub-module
 */
class AuthSDK {
  constructor(apiClient) {
    this.client = apiClient;
  }

  async login(username, password) {
    const response = await this.client.post('/auth/login', { username, password });
    return response.data;
  }

  async register(username, password) {
    const response = await this.client.post('/auth/register', { username, password });
    return response.data;
  }
}

export default AuthSDK;
