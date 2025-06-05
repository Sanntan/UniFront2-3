<template>
  <section class="profile-section">
    <div class="profile-form">
      <!-- Имя -->
      <div class="form-group">
        <label>Имя</label>
        <input
          type="text"
          v-model="userData.name"
          placeholder="Имя"
        >
        <p v-if="validationError" class="error">{{ validationError }}</p>
      </div>

      <!-- Email -->
      <div class="form-group">
        <label>Email</label>
        <input
          type="email"
          v-model="userData.email"
          placeholder="email"
          disabled
        >
      </div>

      <!-- Кнопки -->
      <div class="form-actions">
        <button class="save-btn" @click="saveProfile">
          <i class='bx bx-save'></i> Сохранить изменения
        </button>

        <button class="save-btn" @click="showPasswordFields = !showPasswordFields">
          <i class='bx bx-key'></i> Изменить пароль
        </button>
      </div>

      <p v-if="saveMessage" style="color: green; margin-top: 10px;">{{ saveMessage }}</p>

      <!-- Блок смены пароля -->
      <div v-if="showPasswordFields" class="password-change">
        <div class="form-group">
          <label>Старый пароль</label>
          <div class="input-wrapper">
            <input :type="showOldPassword ? 'text' : 'password'" v-model="oldPassword" placeholder="Введите старый пароль">
            <span class="icon-eye" @click="showOldPassword = !showOldPassword">
              <i :class="showOldPassword ? 'bx bx-show' : 'bx bx-hide'"></i>
            </span>
          </div>
        </div>
        <div class="form-group">
          <label>Новый пароль</label>
          <div class="input-wrapper">
            <input :type="showNewPassword ? 'text' : 'password'" v-model="newPassword" placeholder="Введите новый пароль">
            <span class="icon-eye" @click="showNewPassword = !showNewPassword">
              <i :class="showNewPassword ? 'bx bx-show' : 'bx bx-hide'"></i>
            </span>
          </div>
        </div>
        <div class="form-actions">
          <button class="save-btn" @click="changePassword">
            <i class='bx bx-refresh'></i> Сохранить новый пароль
          </button>
        </div>
        <p v-if="passwordError" class="error">{{ passwordError }}</p>
        <p v-if="passwordSuccess" style="color: green; margin-top: 10px;">{{ passwordSuccess }}</p>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: 'ProfileSection',
  props: {
    user: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      userData: {
        name: this.user.name || '',
        email: this.user.email || ''
      },
      saveMessage: '',
      validationError: '',
      showPasswordFields: false,
      oldPassword: '',
      newPassword: '',
      passwordError: '',
      passwordSuccess: '',
      showOldPassword: false,
      showNewPassword: false,
    }
  },
  watch: {
    user: {
      handler(newVal) {
        this.userData = {
          name: newVal.name || '',
          email: newVal.email || ''
        }
      },
      deep: true
    }
  },
  methods: {
    async saveProfile() {
      this.validationError = '';
      const name = this.userData.name.trim();

      if (!this.isValidName(name)) {
        this.validationError = "Введите имя в формате 'Фамилия Имя', с заглавных букв, только кириллица, 5–50 символов.";
        return;
      }

      const userData = JSON.parse(sessionStorage.getItem('user'));
      try {
        const res = await fetch(`http://localhost:8000/api/user/${userData.user_id}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ name })
        });
        const data = await res.json();
        if (data.success) {
          this.saveMessage = "Изменения профиля сохранены";
          userData.name = name;
          sessionStorage.setItem('user', JSON.stringify(userData));
          this.$emit('profile-saved');
        } else {
          this.saveMessage = "Ошибка сохранения профиля";
        }
      } catch (err) {
        this.saveMessage = "Ошибка соединения с сервером";
      }
      setTimeout(() => { this.saveMessage = ""; }, 2000);
    },
    isValidName(name) {
      const regex = /^[А-ЯЁ][а-яё]+ [А-ЯЁ][а-яё]+$/u;
      return regex.test(name.trim()) && name.length >= 5 && name.length <= 50;
    },
    async changePassword() {
      this.passwordError = '';
      this.passwordSuccess = '';

      const password = this.newPassword.trim();
      const old = this.oldPassword.trim();

      const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+{}\[\]:;<>,.?~\\/-]).{8,}$/;

      if (!old || !password) {
        this.passwordError = "Заполните оба поля";
        return;
      }

      if (!passwordRegex.test(password)) {
        this.passwordError = "Пароль должен быть не менее 8 символов и содержать строчные, заглавные буквы, цифры и спецсимволы.";
        return;
      }

      const userData = JSON.parse(sessionStorage.getItem('user'));
      try {
        const res = await fetch(`http://localhost:8000/api/user/${userData.user_id}/change-password`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            old_password: old,
            new_password: password
          })
        });

        const data = await res.json();
        if (res.status === 400) {
          this.passwordError = data.detail;
        } else if (data.success) {
          this.passwordSuccess = "Пароль успешно изменён";
          this.oldPassword = '';
          this.newPassword = '';
        } else {
          this.passwordError = "Ошибка при смене пароля";
        }
      } catch (err) {
        this.passwordError = "Ошибка соединения с сервером";
      }

      setTimeout(() => {
        this.passwordSuccess = '';
        this.passwordError = '';
      }, 4000);
    },
  }
}
</script>
  
  <style scoped>
  .profile-section {
  padding: 20px;
}

.profile-form {
  max-width: 600px;
  margin: 0 auto;
}

.form-group {
  margin-bottom: 25px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #394038;
}

.form-group input[type="text"],
.form-group input[type="email"],
.input-wrapper input {
  width: 100%;
  padding: 12px 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
}

.input-wrapper {
  position: relative;
}

.input-wrapper input {
  padding-right: 42px;
}

.icon-eye {
  position: absolute;
  top: 50%;
  right: 12px;
  transform: translateY(-50%);
  font-size: 1.2rem;
  color: #394038;
  cursor: pointer;
}

.form-actions {
  margin-top: 25px;
  text-align: center;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.save-btn {
  padding: 12px 25px;
  background: #394038;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.3s ease;
}

.save-btn:hover {
  background: #4a5547;
}

.password-change {
  margin-top: 40px;
}

.error {
  color: red;
  margin-top: 10px;
  background-color: rgba(255, 0, 0, 0.1);
  border-radius: 8px;
  padding: 6px 12px;
  text-align: center;
  font-weight: 500;
}

.dark-theme .form-group label {
  color: #f3f8f1;
}

.dark-theme .form-group input[type="text"],
.dark-theme .form-group input[type="email"],
.dark-theme .input-wrapper input {
  background: rgba(70, 78, 69, 0.7);
  border-color: #4a5547;
  color: #f3f8f1;
}

.dark-theme .icon-eye {
  color: #f3f8f1;
}

.dark-theme .save-btn {
  background: #f3f8f1;
  color: #394038;
}

.dark-theme .save-btn:hover {
  background: #e0e8dd;
}

.dark-theme .error {
  color: #ff6b6b;
  background-color: rgba(255, 100, 100, 0.1);
}

  </style>