<template>
  <div id="app">
    <Header @open-auth="showAuthModal = true" />
    <MainContent />
    <AuthModal 
      :show="showAuthModal"
      @close="showAuthModal = false"
    />
  </div>
</template>

<script>
import Header from './components/Header.vue'
import MainContent from './components/MainContent.vue'
import AuthModal from './components/AuthModal.vue'

export default {
  components: {
    Header,
    MainContent,
    AuthModal
  },
  data() {
    return {
      showAuthModal: false
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
</style>

