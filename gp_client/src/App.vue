<template>
  <img alt="Vue logo" src="./assets/logo.png">
  <UserComponent msg="User.js App"/>
  <div id="app">
    <nav>
      <router-link to="/">Home</router-link> | 
      <router-link to="/login">Login</router-link> | 
      <router-link to="/user-register">User Register</router-link>
    </nav>
    <router-view/>
  </div>
</template>

<script>
import UserComponent from './components/UserComponent.vue'

export default {
  name: 'App',
  components: {
    UserComponent
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
