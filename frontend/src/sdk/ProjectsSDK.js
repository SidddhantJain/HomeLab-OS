/**
 * Git Projects SDK Sub-module
 */
class ProjectsSDK {
  constructor(apiClient) {
    this.client = apiClient;
  }

  async list() {
    const response = await this.client.get('/projects');
    return response.data;
  }

  async create(projectData) {
    const response = await this.client.post('/projects', projectData);
    return response.data;
  }
}

export default ProjectsSDK;
