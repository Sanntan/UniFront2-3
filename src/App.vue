<template>
  <div id="app" :class="{ 'dark-theme': isDarkTheme }">
    <Header @open-auth="showAuthModal = true" @theme-changed="toggleTheme" :key="headerKey" />
    
    <router-view v-slot="{ Component }">
      <component :is="Component" @open-auth="showAuthModal = true" />
    </router-view>

    <AuthModal 
      :show="showAuthModal"
      @close="showAuthModal = false"
      @login-success="handleLoginSuccess"
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
      isDarkTheme: false,
      headerKey: 0
    }
  },
  methods: {
    toggleTheme() {
      this.isDarkTheme = !this.isDarkTheme;
      document.documentElement.classList.toggle('dark-theme', this.isDarkTheme);
    },
    handleLoginSuccess() {
      this.showAuthModal = false;
      sessionStorage.setItem('isAuthenticated', 'true');
      window.dispatchEvent(new Event('auth-changed'));
      this.$router.push('/cabinet');
    },
    updateHeaderKey() {
      this.headerKey++;
    }
  },
  mounted() {
    sessionStorage.removeItem('isAuthenticated');
    sessionStorage.removeItem('user');
    window.addEventListener('auth-changed', this.updateHeaderKey);
  },
  beforeUnmount() {
    window.removeEventListener('auth-changed', this.updateHeaderKey);
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
  background: url('./assets/images/fon_test.png') no-repeat center center fixed;
  background-size: cover;
}
.dark-theme body {
  background-color: #3a4036;
  background: url('./assets/images/fon_dark_test.png') no-repeat center center fixed;
  background-size: cover;
  color: #f0f0f0;
}
</style>

