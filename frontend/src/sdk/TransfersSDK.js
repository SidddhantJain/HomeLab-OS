export const TransfersSDK = {
  list: async () => {
    try {
      const res = await fetch('/api/v1/transfers');
      return await res.json();
    } catch (e) {
      return [];
    }
  }
};
