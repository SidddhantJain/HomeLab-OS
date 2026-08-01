export const ActivitySDK = {
  getTimeline: async (limit = 50) => {
    try {
      const res = await fetch(`/api/v1/activity?limit=${limit}`);
      return await res.json();
    } catch (e) {
      return [];
    }
  }
};
