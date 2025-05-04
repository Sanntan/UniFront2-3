<template>
  <header>
    <h2 class="logo"><img src="../assets/images/Logo3.png" alt="Логотип"></h2>
    <nav class="navigation">
      <a href="#">Главная</a>
      <a href="#">Личный кабинет</a>
      <a href="#">Тема</a>
      <button class="btnLogin-popup" @click="handleAuthClick">
        Авторизация/Регистрация
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
  methods: {
    handleAuthClick() {
      this.$emit('open-auth');
    },
    toggleMobileMenu() {
      const nav = document.querySelector('.navigation');
      nav.classList.toggle('active');
    }
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
  background-color: #c7d7bd;
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
  color: #3a4036;
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
  background: #f3f8f1;
  border-radius: 30px;
  transform-origin: right;
  transform: scaleX(0);
  transition: transform 0.3s ease;
}

.navigation a:hover::after {
  transform-origin: left;
  transform: scaleX(1);
}

.navigation .btnLogin-popup {
  width: clamp(150px, 16vw, 250px);
  height: clamp(45px, 5vw, 60px);
  background: transparent;
  border: 3px solid #f3f8f1;
  outline: none;
  border-radius: 30px;
  cursor: pointer;
  font-size: clamp(0.9em, 1.1vw, 1.1em);
  font-weight: 500;
  margin-left: clamp(15px, 2vw, 40px);
  transition: all 0.3s ease;
  color: #3a4036;
}

.navigation .btnLogin-popup:hover {
  background: #f3f8f1;
}

.mobile-menu-btn {
  display: none;
  background: none;
  border: none;
  font-size: 1.8em;
  color: #3a4036;
  cursor: pointer;
  transition: all 0.3s ease;
}

@media (max-width: 992px) {
  .navigation a {
    margin-left: clamp(10px, 1.5vw, 20px);
    font-size: 0.95em;
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
</style>