<template>
  <div>
    <h1>用戶註冊</h1>
    <form @submit.prevent="registerUser">
      <label>
        用戶名稱:
        <input v-model="user_id" required />
      </label>
      <label>
        密碼:
        <input type="password" v-model="password" required />
      </label>
      <button type="submit">註冊</button>
    </form>
  </div>
</template>

<script>
import axios from '@/axios'; // 引入創建的 axios 實例

export default {
  data() {
    return {
      username: '',
      password: ''
    };
  },
  methods: {
    async registerUser() {
      try {
        const response = await axios.post('/api/user', {
          user_id: this.user_id,
          password: this.password,
          member_level: "初等會員"
        });
        console.log('用戶已註冊:', response.data);
        // 你可以在這裡添加其他操作，例如導航到登入頁面或者顯示一個成功消息給用戶
      } catch (error) {
        console.error('註冊用戶時發生錯誤:', error);
        // 處理錯誤，例如向用戶顯示一個錯誤消息
      }
    }
  }
};
</script>

<style scoped>
/* 你可以在這裡添加你的樣式 */
</style>
