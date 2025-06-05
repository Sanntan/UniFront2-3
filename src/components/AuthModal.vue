<template>
  <div class="wrapper" :class="{ 'active-popup': showModal, 'active': isRegister }">
    <span class="icon-close" @click="closeModal">
      <i class="bx bx-x"></i>
    </span>

    <!-- Login Form -->
    <div class="form-box login">
      <h2>Авторизация</h2>
      <form @submit.prevent="handleLogin">
        <div class="input-box tooltip-container">
          <input
            type="email"
            v-model="loginForm.email"
            required
            @focus="focusedField = 'loginEmail'"
            @blur="focusedField = ''"
          >
          <label>Электронная почта</label>
          <span class="icon"><i class="bx bx-envelope"></i></span>
          <div class="tooltip" v-if="focusedField === 'loginEmail'">
            Введите корректный email (например, name@example.com)
          </div>
        </div>
        <div class="input-box">
          <input :type="showLoginPassword ? 'text' : 'password'" v-model="loginForm.password" required>
          <label>Пароль</label>
          <span class="icon-eye" @click="showLoginPassword = !showLoginPassword">
            <i :class="showLoginPassword ? 'bx bx-show' : 'bx bx-hide'"></i>
          </span>
          <span class="icon"><i class="bx bx-lock-alt"></i></span>
        </div>
        <div class="remember-forgot">
          <label><input type="checkbox" v-model="loginForm.remember"> Запомнить меня</label>
          <a href="#" v-show="false">Забыли пароль?</a>
        </div>
        <button type="submit" class="btn" :disabled="isLoggingIn">
          <span v-if="isLoggingIn">Вход...</span>
          <span v-else>Вход</span>
        </button>
        <p v-if="loginError" class="error">{{ loginError }}</p>
        <div class="social-login">
          <p>Или войти через:</p>
          <div class="social-icons">
            <a href="#" @click.prevent="loginWithGitHub" class="social-icon github">
              <i class="bx bxl-github"></i>
            </a>
          </div>
        </div>
        <div class="login-register">
          <p>Нет аккаунта? <a href="#" @click.prevent="toggleForm">Регистрация</a></p>
        </div>
      </form>
    </div>

    <!-- Register Form -->
    <div class="form-box register">
      <h2>Регистрация</h2>
      <form @submit.prevent="handleRegister">
        <div class="input-box tooltip-container">
          <span class="icon"><i class="bx bx-user"></i></span>
          <input
            type="text"
            v-model="registerForm.firstName"
            required
            :class="{ invalid: invalidFields.includes('firstName') }"
            @focus="focusedField = 'firstName'"
            @blur="focusedField = ''"
          >
          <label>Имя</label>
          <div class="tooltip" v-if="focusedField === 'firstName'">
            Только кириллица, от 2 до 30 символов, с заглавной буквы
          </div>
        </div>

        <div class="input-box tooltip-container">
          <span class="icon"><i class="bx bx-user"></i></span>
          <input
            type="text"
            v-model="registerForm.lastName"
            required
            :class="{ invalid: invalidFields.includes('lastName') }"
            @focus="focusedField = 'lastName'"
            @blur="focusedField = ''"
          >
          <label>Фамилия</label>
          <div class="tooltip" v-if="focusedField === 'lastName'">
            Только кириллица, от 2 до 30 символов, с заглавной буквы
          </div>
        </div>

        <div class="input-box tooltip-container">
          <span class="icon"><i class="bx bx-envelope"></i></span>
          <input
            type="email"
            v-model="registerForm.email"
            required
            :class="{ invalid: invalidFields.includes('email') }"
            @focus="focusedField = 'email'"
            @blur="focusedField = ''"
          >
          <label>Электронная почта</label>
          <div class="tooltip" v-if="focusedField === 'email'">
            Пример: name@example.com
          </div>
        </div>

        <div class="input-box tooltip-container">
          <span class="icon"><i class="bx bx-lock-alt"></i></span>
          <input
            :type="showRegisterPassword ? 'text' : 'password'"
            v-model="registerForm.password"
            required
            :class="{ invalid: invalidFields.includes('password') }"
            @focus="focusedField = 'password'"
            @blur="focusedField = ''"
          >
          <label>Пароль</label>
          <span class="icon-eye" @click="showRegisterPassword = !showRegisterPassword">
            <i :class="showRegisterPassword ? 'bx bx-show' : 'bx bx-hide'"></i>
          </span>
          <div class="tooltip" v-if="focusedField === 'password'">
            Мин. 8 символов, заглавная и строчная буквы, цифра, спецсимвол
          </div>
        </div>

        <div class="input-box tooltip-container">
          <span class="icon"><i class="bx bx-lock-alt"></i></span>
          <input
            :type="showConfirmPassword ? 'text' : 'password'"
            v-model="registerForm.confirmPassword"
            required
            :class="{ invalid: invalidFields.includes('confirmPassword') }"
            @focus="focusedField = 'confirmPassword'"
            @blur="focusedField = ''"
          >
          <label>Подтвердите пароль</label>
          <span class="icon-eye" @click="showConfirmPassword = !showConfirmPassword">
            <i :class="showConfirmPassword ? 'bx bx-show' : 'bx bx-hide'"></i>
          </span>
          <div class="tooltip" v-if="focusedField === 'confirmPassword'">
            Пароли должны совпадать
          </div>
        </div>

        <button type="submit" class="btn">Зарегистрироваться</button>
        <p v-if="registerError" class="error">{{ registerError }}</p>
        <div class="social-login">
          <p>Или зарегистрироваться через:</p>
          <div class="social-icons">
            <a href="#" @click.prevent="loginWithGitHub" class="social-icon github">
              <i class="bx bxl-github"></i>
            </a>
          </div>
        </div>
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
      isLoggingIn: false,
      showLoginPassword: false,
      showRegisterPassword: false,
      showConfirmPassword: false,
      invalidFields: [],
      loginError: '',
      registerError: '',
      focusedField: '',
      loginForm: {
        email: '',
        password: '',
        remember: false
      },
      registerForm: {
        firstName: '',
        lastName: '',
        email: '',
        password: '',
        confirmPassword: '', 
      },
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
      this.loginError = ''
      this.registerError = ''
    },
    closeModal() {
      this.$emit('close')
    },
    async handleLogin() {
      this.isLoggingIn = true
      try {
        const res = await fetch('http://localhost:8000/api/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            email: this.loginForm.email,
            password: this.loginForm.password
          })
        })
        const data = await res.json()
        if (data.success) {
          sessionStorage.setItem('isAuthenticated', 'true')
          sessionStorage.setItem('user', JSON.stringify(data.user))
          this.loginError = ''
          this.$emit('login-success')
          this.closeModal()
          window.dispatchEvent(new Event('auth-changed'));
          window.dispatchEvent(new CustomEvent('auth-loaded'));
        } else {
          this.loginError = data.message || 'Неверный email или пароль'
        }
      } catch (err) {
        this.loginError = 'Ошибка соединения с сервером'
      } finally {
        this.isLoggingIn = false
      }
    },
    async handleRegister() {
      this.registerError = '';
      this.invalidFields = [];

      const nameRegex = /^[А-ЯЁ][а-яё]+$/u;
      const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
      const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+{}\[\]:;<>,.?~\\/-]).{8,}$/;

      const first = this.registerForm.firstName.trim();
      const last = this.registerForm.lastName.trim();
      const email = this.registerForm.email.trim();
      const password = this.registerForm.password;
      const confirm = this.registerForm.confirmPassword;

      if (!nameRegex.test(first) || first.length < 2 || first.length > 30) {
        this.invalidFields.push('firstName');
      }
      if (!nameRegex.test(last) || last.length < 2 || last.length > 30) {
        this.invalidFields.push('lastName');
      }
      if (!emailRegex.test(email) || email.length > 100) {
        this.invalidFields.push('email');
      }
      if (!passwordRegex.test(password)) {
        this.invalidFields.push('password');
      }
      if (password !== confirm) {
        this.invalidFields.push('confirmPassword');
      }

      if (this.invalidFields.length > 0) {
        this.registerError = "Неверно введённые данные";
        return;
      }

      try {
        const res = await fetch('http://localhost:8000/api/register', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            first_name: first,
            last_name: last,
            email: email,
            password: password
          })
        });

        const data = await res.json();
        if (res.status === 409) {
          this.registerError = data.detail || 'Такой email уже зарегистрирован';
        } else if (data.success) {
          this.$emit('close');
          alert('Успешная регистрация! Теперь вы можете войти.');
        } else {
          this.registerError = data.message || 'Ошибка регистрации';
        }
      } catch (err) {
        this.registerError = "Ошибка соединения с сервером";
      }
    },
    // Заглушки для соц. сетей
    loginWithGitHub() {
      alert('OAuth авторизация отключена')
    },
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
  height: 670px;   /* было 520px, стало 670px (+150) */
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
  height: 830px;
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

  position: relative;
  width: 100%;
  height: 50px;
  border-bottom: 2px solid #3a4036;
  margin: 30px 0;
}

.input-box label {
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
  top: 50%;
  right: 8px;
  transform: translateY(-50%);
  font-size: 1.2em;
  color: #394038;
  pointer-events: none;
}

.input-box .icon-eye {
  position: absolute;
  top: 50%;
  right: 38px;
  transform: translateY(-50%);
  font-size: 1.2em;
  color: #394038;
  cursor: pointer;
  pointer-events: auto;
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
  margin-bottom: 15px;
  transition: all 0.3s ease;
  transform: scale(1);
} 

.btn:hover {
  transform: scale(1.03);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.social-login {
  text-align: center;
  margin: 20px 0;
}

.social-login p {
  color: #394038;
  margin-bottom: 15px;
  background: #f3f8f1;
}

.social-icons {
  display: flex;
  justify-content: center;
  gap: 15px;
}

.social-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  color: white;
  font-size: 1.2rem;
  text-decoration: none;
  transition: transform 0.3s;
}

.social-icon:hover {
  transform: scale(1.1);
}

.social-icon.github {
  background: #333;
}

.social-icon.vk {
  background: #4a76a8;
}

.social-icon.google {
  background: #db4437;
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
  transition: all 0.2s ease;
  display: inline-block;
}

.login-register p a:hover {
  text-decoration: underline;
  transform: scale(1.03);
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

  border-bottom-color: #161a15;
}

.dark-theme .input-box label {

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

.dark-theme .btn:hover {
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.dark-theme .login-register p,
.dark-theme .login-register p a {
  color: #161a15;
}

.dark-theme .icon-close {
  background: #394038;
  color: #f3f8f1;
}

.dark-theme .social-login p {
  color: #161a15;
  background: #99aa8e;
}

.error {
  color: red;
  margin-top: 10px;
  text-align: center;
  background-color: rgba(255, 0, 0, 0.1);
  border-radius: 10px;
  padding: 10px;
  font-weight: bold;
}

.dark-theme .error {
  background-color: rgba(255, 0, 0, 0.15);
  color: rgb(104, 0, 0);
  border: 1px solid #700101;
}

.tooltip-container {
  position: relative;
}

.tooltip {
  position: absolute;
  top: 105%; /* чуть ниже поля */
  left: 0;
  background: #f3f8f1;
  border: 1px solid #394038;
  color: #394038;
  padding: 8px 12px;
  border-radius: 8px;
  font-size: 0.85rem;
  max-width: 280px;
  width: max-content;
  white-space: normal;
  word-wrap: break-word;
  z-index: 10;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
  opacity: 1;
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.dark-theme .tooltip {
  background: #394038;
  color: #f3f8f1;
  border-color: #f3f8f1;
}

.tooltip-fade-enter-from,
.tooltip-fade-leave-to {
  opacity: 0;
  transform: translateY(-4px);
}

.tooltip-fade-enter-active,
.tooltip-fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.dark-theme .tooltip {
  background: #394038;
  color: #f3f8f1;
  border-color: #f3f8f1;
}

.input-box input.invalid {
  border-bottom: 2px solid red !important;
}

.dark-theme .input-box input.invalid {
  border-bottom: 2px solid #ff6b6b !important;
}

</style>