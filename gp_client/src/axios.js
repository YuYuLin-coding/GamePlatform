// src/axios.js
import axios from 'axios';
import { Notify } from 'notiflix';

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

// 響應攔截器
instance.interceptors.response.use(
    response => {
        // 如果請求成功，則直接返回響應數據
        Notify.success('Request Successful!'); // 提示用戶請求成功
        return response.data;
    },
    error => {
        console.error("An error occurred: ", error);
        
        // 判斷錯誤的類型，並給出相應的用戶反饋
        if (error.response) {
            // 伺服器返回了一個非 2xx 的響應
            Notify.failure(`Error ${error.response.status}: ${error.response.statusText}`);
        } else if (error.request) {
            // 請求已經發出，但沒有收到回應
            Notify.failure('No response received from the server. Please try again later.');
        } else {
            // 有些其他的錯誤
            Notify.failure('An error occurred while making the request. Please try again later.');
        }
        
        // 可以選擇將錯誤傳遞給下一個 .catch() 處理器
        return Promise.reject(error);
    }
);

export default instance;