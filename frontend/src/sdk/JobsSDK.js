export const JobsSDK = {
  list: async () => {
    try {
      const res = await fetch('/api/v1/jobs');
      return await res.json();
    } catch (e) {
      return [];
    }
  }
};
