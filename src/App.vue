<template>
  <div id="app" :class="{ 'dark-theme': isDarkTheme }">
    <Header @open-auth="showAuthModal = true" @theme-changed="toggleTheme" />
    <router-view></router-view>
    <AuthModal 
      :show="showAuthModal"
      @close="showAuthModal = false"
    />
  </div>
</template>

<script>
import Header from './components/Header.vue'
import AuthModal from './components/AuthModal.vue'

export default {
  components: {
    Header,
    AuthModal
  },
  data() {
    return {
      showAuthModal: false,
      isDarkTheme: false
    }
  },
  methods: {
    toggleTheme() {
      this.isDarkTheme = !this.isDarkTheme;
      document.documentElement.classList.toggle('dark-theme', this.isDarkTheme);
    }
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Poppins', sans-serif;
}

body {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #c6dab7; 
  background: url('./assets/images/Fon.png') no-repeat center center fixed;
  background-size: cover;
}
.dark-theme body {
  background-color: #3a4036;
  background: url('./assets/images/Fon2.png') no-repeat center center fixed;
  background-size: cover;
  color: #f0f0f0;
}
</style>

