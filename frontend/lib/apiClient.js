import axios from 'axios';

const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_BASE_URL,
});

apiClient.interceptors.request.use(async (config) => {
  try {
    const response = await fetch('/api/auth/get-token');
    if (response.ok) {
      const { accessToken } = await response.json();
      config.headers.Authorization = `Bearer ${accessToken}`;
    }
  } catch (error) {
    console.error('Could not get access token:', error);
  }
  return config;
});

export default apiClient;