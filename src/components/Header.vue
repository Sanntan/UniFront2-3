<template>
  <header>
    <h2 class="logo">
      <img 
        v-show="!isDarkTheme"
        src="../assets/images/Logo.png" 
        alt="Логотип светлой темы"
        class="logo-image"
      >
      <img 
        v-show="isDarkTheme"
        src="../assets/images/Logo2.png" 
        alt="Логотип темной темы"
        class="logo-image"
      >
    </h2>
    <nav class="navigation">
      <router-link to="/">Главная</router-link>
      <a href="#" 
         class="nav-link" 
         @click.prevent="navigateToCabinet"
         :class="{ 'active': $route.path === '/cabinet' }">
        Личный кабинет
      </a>
      <button class="theme-toggle" @click="toggleTheme">
        <i :class="themeIcon"></i>
      </button>
      <button class="btnLogin-popup" @click="handleAuthClick">
        {{ isAuthenticated ? 'Выйти' : 'Авторизация/Регистрация' }}
      </button>
    </nav>
    <button class="mobile-menu-btn" @click="toggleMobileMenu">
      <i class='bx bx-menu'></i>
    </button>
  </header>
</template>

<script>
export default {
  name: 'AppHeader',
  data() {
    return {
      isDarkTheme: false,
      authKey: 0, // ключ для форс-обновления
    }
  },
  computed: {
    isAuthenticated() {
      return sessionStorage.getItem('isAuthenticated') === 'true'
    },
    themeIcon() {
      return this.isDarkTheme ? 'bx bx-sun' : 'bx bx-moon'
    }
  },
  methods: {
    handleAuthClick() {
      if (this.isAuthenticated) {
        this.logoutMock();
      } else {
        this.$emit('open-auth');
      }
    },
    logoutMock() {
      sessionStorage.removeItem('isAuthenticated');
      sessionStorage.removeItem('user');
      this.$router.push('/');
      window.dispatchEvent(new Event('auth-changed'));
    },
    toggleMobileMenu() {
      const nav = document.querySelector('.navigation');
      nav.classList.toggle('active');
    },
    toggleTheme() {
      this.isDarkTheme = !this.isDarkTheme;
      document.documentElement.classList.toggle('dark-theme', this.isDarkTheme);
      this.$emit('theme-changed', this.isDarkTheme);
    },
    navigateToCabinet() {
      if (this.isAuthenticated) {
        this.$router.push('/cabinet');
      } else {
        this.$emit('open-auth');
      }
    },
    forceAuthUpdate() {
      // Меняем ключ, чтобы компонент перерисовался
      this.authKey++;
    }
  },
  created() {
    // слушаем глобальное событие на логин
    window.addEventListener('auth-changed', this.forceAuthUpdate);
  },
  beforeUnmount() {
    window.removeEventListener('auth-changed', this.forceAuthUpdate);
  }
}
</script>

<style scoped>
header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  padding: clamp(15px, 2vw, 25px) clamp(20px, 5%, 100px);
  display: flex;
  justify-content: space-between;
  align-items: center;
  z-index: 99;
  box-shadow: 0 2px 10px rgba(0, 0, 0, .2);
  background-color: #ffffff;
  transition: all 0.4s ease;
}

img {
  width: clamp(120px, 15vw, 200px);
  height: auto;
  transition: width 0.3s ease;
}

.navigation {
  display: flex;
  align-items: center;
  transition: all 0.4s ease;
}

.navigation a {
  position: relative;
  font-size: clamp(0.9em, 1.1vw, 1.1em);
  color: #141414;
  text-decoration: none;
  font-weight: 500;
  margin-left: clamp(15px, 2vw, 40px);
  transition: all 0.3s ease;
}

.navigation a::after {
  content: '';
  position: absolute;
  left: 0;
  bottom: -6px;
  width: 100%;
  height: 3px;
  background: #000000;
  border-radius: 30px;
  transform-origin: right;
  transform: scaleX(0);
  transition: transform 0.3s ease;
}

.navigation a:hover::after {
  transform-origin: left;
  transform: scaleX(1);
}

.theme-toggle {
  background: transparent;
  border: none;
  font-size: clamp(1.2em, 1.5vw, 1.5em);
  color: #141414;
  cursor: pointer;
  margin-left: clamp(15px, 2vw, 40px);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.theme-toggle:hover {
  transform: scale(1.1);
}

.navigation .btnLogin-popup {
  width: clamp(150px, 16vw, 250px);
  height: clamp(45px, 5vw, 60px);
  background: transparent;
  border: 2px solid #000000;
  outline: none;
  border-radius: 30px;
  cursor: pointer;
  font-size: clamp(0.9em, 1.1vw, 1.1em);
  font-weight: 500;
  margin-left: clamp(15px, 2vw, 40px);
  transition: all 0.3s ease;
  color: #141414;
}

.navigation .btnLogin-popup:hover {
  background: #f3f8f1;
}

.mobile-menu-btn {
  display: none;
  background: none;
  border: none;
  font-size: 1.8em;
  color: #141414;
  cursor: pointer;
  transition: all 0.3s ease;
}

@media (max-width: 992px) {
  .navigation a {
    margin-left: clamp(10px, 1.5vw, 20px);
    font-size: 0.95em;
  }
  
  .theme-toggle {
    font-size: 1.3em;
    margin-left: clamp(10px, 1.5vw, 20px);
  }
  
  .navigation .btnLogin-popup {
    width: clamp(130px, 14vw, 180px);
    font-size: 0.95em;
  }
}

@media (max-width: 768px) {
  header {
    padding: 15px 20px;
  }
  
  .navigation {
    position: fixed;
    top: 80px;
    left: -100%;
    width: 100%;
    height: calc(100vh - 80px);
    background: rgba(255, 255, 255, 0.95);
    flex-direction: column;
    align-items: center;
    padding: 40px 0;
    transition: left 0.4s ease;
  }
  
  .navigation.active {
    left: 0;
    background-color: #c7d7bd;
  }
  
  .navigation a {
    margin: 15px 0;
    font-size: 1.2em;
  }
  
  .theme-toggle {
    margin: 15px 0;
    font-size: 1.5em;
  }
  
  .navigation .btnLogin-popup {
    margin: 20px 0 0;
    width: 200px;
    height: 50px;
  }
  
  .mobile-menu-btn {
    display: block;
  }
}

@media (max-width: 480px) {
  header {
    padding: 12px 15px;
  }
  
  img {
    width: 100px;
  }
  
  .mobile-menu-btn {
    font-size: 1.5em;
  }
  
  .navigation {
    top: 70px;
    height: calc(100vh - 70px);
  }
}

.dark-theme header {
  background-color: #141414;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.4);
  transition: all 0.4s ease;
}

.dark-theme .navigation a {
  color: #f3f8f1;
  transition: all 0.3s ease;
}

.dark-theme .navigation a::after {
  background: #f3f8f1;
  transform-origin: right;
  transform: scaleX(0);
  transition: transform 0.3s ease;
}

.dark-theme .navigation a:hover::after {
  transform-origin: left;
  transform: scaleX(1);
}

.dark-theme .theme-toggle {
  color: #f3f8f1;
  transition: all 0.3s ease;
}

.dark-theme .theme-toggle:hover {
  transform: scale(1.1);
}

.dark-theme .btnLogin-popup {
  border-color: #f3f8f1;
  color: #f3f8f1;
  transition: all 0.3s ease;
}

.dark-theme .btnLogin-popup:hover {
  background: #f3f8f1;
  color: #141414;
}

.dark-theme .mobile-menu-btn {
  color: #f3f8f1;
  transition: all 0.3s ease;
}

.dark-theme .navigation {
  background: #141414;
  transition: all 0.4s ease;
}

.dark-theme .navigation.active {
  background-color: #141414;
  transition: left 0.4s ease;
}

.dark-theme img {
  transition: width 0.3s ease;
}

</style>