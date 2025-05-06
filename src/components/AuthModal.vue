<template>
  <div class="wrapper" :class="{ 'active-popup': showModal, 'active': isRegister }">
    <span class="icon-close" @click="closeModal">
      <i class="bx bx-x"></i>
    </span>

    <div class="form-box login">
      <h2>Авторизация</h2>
      <form @submit.prevent="handleLogin">
        <div class="input-box">
          <span class="icon"><i class="bx bx-envelope"></i></span>
          <input type="email" v-model="loginForm.email" required>
          <label>Электронная почта</label>
        </div>
        <div class="input-box">
          <span class="icon"><i class="bx bx-lock-alt"></i></span>
          <input :type="showLoginPassword ? 'text' : 'password'" v-model="loginForm.password" required>
          <label>Пароль</label>
          <span class="icon-eye" @click="showLoginPassword = !showLoginPassword">
            <i :class="showLoginPassword ? 'bx bx-show' : 'bx bx-hide'"></i>
          </span>
        </div>
        <div class="remember-forgot">
          <label><input type="checkbox" v-model="loginForm.remember"> Запомнить меня</label>
          <a href="#">Забыли пароль?</a>
        </div>
        <button type="submit" class="btn">Вход</button>
        <div class="login-register">
          <p>Создать аккаунт? <a href="#" @click.prevent="toggleForm">Регистрация</a></p>
        </div>
      </form>
    </div>

    <div class="form-box register">
      <h2>Регистрация</h2>
      <form @submit.prevent="handleRegister">
        <div class="input-box">
          <span class="icon"><i class="bx bx-user"></i></span>
          <input type="text" v-model="registerForm.username" required>
          <label>Имя пользователя</label>
        </div>
        <div class="input-box">
          <span class="icon"><i class="bx bx-envelope"></i></span>
          <input type="email" v-model="registerForm.email" required>
          <label>Электронная почта</label>
        </div>
        <div class="input-box">
          <span class="icon"><i class="bx bx-lock-alt"></i></span>
          <input :type="showRegisterPassword ? 'text' : 'password'" v-model="registerForm.password" required>
          <label>Пароль</label>
          <span class="icon-eye" @click="showRegisterPassword = !showRegisterPassword">
            <i :class="showRegisterPassword ? 'bx bx-show' : 'bx bx-hide'"></i>
          </span>
        </div>
        <div class="input-box">
          <span class="icon"><i class="bx bx-lock-alt"></i></span>
          <input :type="showConfirmPassword ? 'text' : 'password'" v-model="registerForm.confirmPassword" required>
          <label>Подтвердите пароль</label>
          <span class="icon-eye" @click="showConfirmPassword = !showConfirmPassword">
            <i :class="showConfirmPassword ? 'bx bx-show' : 'bx bx-hide'"></i>
          </span>
        </div>
        <button type="submit" class="btn">Зарегистрироваться</button>
        <div class="login-register">
          <p>Уже есть аккаунт? <a href="#" @click.prevent="toggleForm">Авторизация</a></p>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AuthModal',
  props: {
    show: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      isRegister: false,
      showLoginPassword: false,
      showRegisterPassword: false,
      showConfirmPassword: false,
      loginForm: {
        email: '',
        password: '',
        remember: false
      },
      registerForm: {
        username: '',
        email: '',
        password: '',
        confirmPassword: ''
      }
    }
  },
  computed: {
    showModal() {
      return this.show
    }
  },
  methods: {
    toggleForm() {
      this.isRegister = !this.isRegister
    },
    closeModal() {
      this.$emit('close')
    },
    handleLogin() {
      console.log('Login data:', this.loginForm)
      this.closeModal()
    },
    async handleRegister() {
    if (this.registerForm.password !== this.registerForm.confirmPassword) {
      alert('Пароли не совпадают!');
      return;
    }

    try {
      const response = await fetch('http://your-api.com/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          username: this.registerForm.username,
          email: this.registerForm.email,
          password: this.registerForm.password
        })
      });

      const data = await response.json();
      
      if (response.ok) {
        localStorage.setItem('token', data.token);
        this.$emit('register-success');
        this.closeModal();
      } else {
        throw new Error(data.message || 'Ошибка регистрации');
      }
    } catch (error) {
      console.error('Registration error:', error);
      alert(error.message);
    }
  }
  }
}
</script>

<style scoped>
.wrapper {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%) scale(0);
  width: 400px;
  height: 440px;
  border: 2px solid #f3f8f1;
  border-radius: 30px;
  background: #f3f8f1;
  box-shadow: 0 0 30px rgba(0, 0, 0, .5);
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
  transition: transform 0.5s ease, height 0.2s ease;
  z-index: 1000;
}

.wrapper.active-popup {
  transform: translate(-50%, -50%) scale(1);
}

.wrapper.active {
  height: 600px;
}

.wrapper .form-box {
  background: #f3f8f1;
  width: 100%;
  padding: 40px;
  border-radius: 30px;
}

.wrapper .form-box.login {
  transition: transform .18s ease;
  transform: translateX(0);
}

.wrapper.active .form-box.login {
  transition: none;
  transform: translateX(-400px);
}

.wrapper .form-box.register {
  position: absolute;
  transition: none;
  transform: translateX(400px);
}

.wrapper.active .form-box.register {
  transition: transform .18s ease;
  transform: translateX(0);
}

.wrapper .icon-close {
  position: absolute;
  top: 0;
  right: 0;
  width: 45px;
  height: 45px;
  background: #394038;
  font-size: 1.5em;
  color: #f3f8f1;
  display: flex;
  justify-content: center;
  align-items: center;
  border-bottom-left-radius: 20px;
  cursor: pointer;
  z-index: 1;
}
.form-box h2 {
  background: #f3f8f1;
  font-size: 2em;
  color: #394038;
  text-align: center;
  font-weight: bold;
}

.input-box {
  background: #f3f8f1;
  position: relative;
  width: 100%;
  height: 50px;
  border-bottom: 2px solid #3a4036;
  margin: 30px 0;
}

.input-box label {
  background: #f3f8f1;
  position: absolute;
  top: 50%;
  left: 5px;
  transform: translateY(-50%);
  font-size: 1em;
  color:#394038;
  font-weight: 500;
  pointer-events: none;
  transition: .5s;
}

.input-box input:focus~label,
.input-box input:valid~label {
  top: -5px;
}

.input-box input {
  width: 100%;
  height: 100%;
  background: transparent;
  border: none;
  outline: none;
  font-size: 1em;
  color: #394038;
  font-weight: 600;
  padding: 0 35px 0 5px;
}

.input-box .icon {
  position: absolute;
  right: 30px;
  font-size: 1.2em;
  color:#394038;
  line-height: 57px;
  background: transparent;
}

.input-box .icon-eye {
  position: absolute;
  right: 8px;
  font-size: 1.2em;
  color:#394038;
  line-height: 57px;
  background: transparent;
  cursor: pointer;
}

.remember-forgot {
  background: #f3f8f1;
  font-size: .9em;
  color: #394038;
  font-size: 500;
  margin: -15px 0 15px;
  display: flex;
  justify-content: space-between;
}

.remember-forgot label input {
  accent-color: #394038;
  margin-right: 3px;
}

.remember-forgot a {
  background: #f3f8f1;
  color:#394038;
  text-decoration: none;
}

.remember-forgot a:hover {
  text-decoration: underline;
}

.btn {
  width: 100%;
  height: 45px;
  background: #394038;
  border: none;
  outline: none;
  border-radius: 30px;
  cursor: pointer;
  font-size: 1em;
  color: #f3f8f1;
  font-weight: 500;
} 

.login-register {
  font-size: .9em;
  color: #394038;
  text-align: center;
  font-weight: 500;
  margin: 25px 0 10px;
}

.login-register p a {
  color: #394038;
  text-decoration: none;
  font-weight: 600;
}

.login-register p a:hover {
  text-decoration: underline;
}

.login-register p, .login-register p a {
  background: #f3f8f1;
}


.dark-theme .wrapper {
  border-color: #99aa8e;
  background: #99aa8e;
  box-shadow: 0 0 30px rgba(0, 0, 0, 0.7);
}

.dark-theme .wrapper .form-box {
  background: #99aa8e;
}

.dark-theme .form-box h2 {
  background: #99aa8e;
  color: #161a15;
}

.dark-theme .input-box {
  background: #99aa8e;
  border-bottom-color: #161a15;
}

.dark-theme .input-box label {
  background: #99aa8e;
  color: #161a15;
}

.dark-theme .input-box input {
  color: #161a15;
}

.dark-theme .input-box .icon,
.dark-theme .input-box .icon-eye {
  color: #161a15;
}

.dark-theme .remember-forgot,
.dark-theme .remember-forgot a {
  color: #161a15;
  background: #99aa8e;
}

.dark-theme .btn {
  background: #394038;
  color: #f3f8f1;
}

.dark-theme .login-register p,
.dark-theme .login-register p a {
  color: #161a15;
  background: #99aa8e;
}

.dark-theme .icon-close {
  background: #394038;
  color: #f3f8f1;
}
</style>