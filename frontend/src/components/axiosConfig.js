// axiosConfig.js
import axios from 'axios';

const instance = axios.create({
  baseURL: 'http://your-api-url.com/api/', // Replace with your API base URL
});

export default instance;
