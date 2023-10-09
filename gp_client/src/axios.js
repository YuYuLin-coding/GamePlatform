// src/axios.js
import axios from 'axios';

const instance = axios.create({
    baseURL: 'http://0.0.0.0:8000/'
});

// 請求攔截器
instance.interceptors.request.use(
    config => {
      // 從 localStorage 中獲取 token
      const token = localStorage.getItem('user_token');
  
      // 如果 token 存在，則攜帶在請求 header 中
      if (token) {
        config.headers['Authorization'] = 'Bearer ' + token;
      }
  
      return config;
    },
    error => {
      // 對請求錯誤做些什麼
      return Promise.reject(error);
    }
  );

export default instance;

