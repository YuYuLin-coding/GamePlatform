<template>
  <div>
    <h1>Login</h1>
    <form @submit.prevent="login">
      <div>
        <label for="user_id">Username:</label>
        <input v-model="user_id" id="user_id" required>
      </div>
      <div>
        <label for="password">Password:</label>
        <input type="password" v-model="password" id="password" required>
      </div>
      <button type="submit">Login</button>
    </form>
  </div>
  <!-- 动态消息展示 -->
  <div v-if="showMessage" :class="messageClass">
      {{ message }}
  </div>

</template>
  
<script>
import axios from '@/axios.js';

export default {
  data() {
    return {
      user_id: '',
      password: '',
      message: '', // 用來顯示消息的變數
      showMessage: false, // 用來確定是否顯示消息的變數
      messageClass: '', // 用来添加不同狀態的樣式
    };
  },
  methods: {
    async login() {
      try {
        const response = await axios.post('api/user/login', {
          user_id: this.user_id,
          password: this.password,
        });
        
        console.log('Response Data:', response.data);

        // 檢查響應的 status
        if (response.status === 200) {
          this.message = 'Login successful!';
          this.messageClass = 'success';
          localStorage.setItem('user_token', response.data.user_token);
        }
        else if (response.status !== 200){
          this.message = 'Login failed!';
          this.messageClass = 'error';
          console.error('Error Status:', response.status);
          console.error('Error Message:', response.statusText);
        }

        // 使用回傳的資料（例如 token）
        console.log('User logged in', response.data);
        
        // 你可以在這裡進行其他操作，比如跳轉或儲存 token
        // 例如：this.$router.push({ name: 'Home' });
      } catch (error) {
        console.error('An error occurred during login:', error);
        this.message = error.response.data.message;
        this.messageClass = 'error';
        // 如果 error.response 存在，則印出詳細的錯誤資訊
        if (error.response) {
          console.error('Error Status:', error.response.status);
          console.error('Error Message:', error.response.data);
        }
      } finally {
        this.showMessage = true;
        // 幾秒後自動隱藏消息
        setTimeout(() => {
          this.showMessage = false;
        }, 3000);
      }
    },
  },
};
</script>

<style scoped>

/* 成功的消息樣式 */
.success {
  color: green;
  background-color: #f0f9f0;
  border: 1px solid #d4edd4;
  padding: 10px;
  margin: 10px 0;
}

/* 錯誤的消息樣式 */
.error {
  color: red;
  background-color: #fef0f0;
  border: 1px solid #edd4d4;
  padding: 10px;
  margin: 10px 0;
}
</style>
  