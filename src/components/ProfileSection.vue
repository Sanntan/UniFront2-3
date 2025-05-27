<template>
  <section class="profile-section">
    <div class="profile-form">
      <div class="form-group">
        <label>Имя</label>
        <input
          type="text"
          v-model="userData.name"
          placeholder="Имя"
        >
      </div>
      <div class="form-group">
        <label>Email</label>
        <input
          type="email"
          v-model="userData.email"
          placeholder="email"
          disabled
        >
      </div>
      <div class="form-actions">
        <button class="save-btn" @click="saveProfile">
          <i class='bx bx-save'></i> Сохранить изменения
        </button>
      </div>
      <p v-if="saveMessage" style="color: green; margin-top: 10px;">{{ saveMessage }}</p>
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
      saveMessage: ''
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
      const userData = JSON.parse(sessionStorage.getItem('user'));
      try {
        const res = await fetch(`http://localhost:8000/api/user/${userData.user_id}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            name: this.userData.name
          })
        });
        const data = await res.json();
        if (data.success) {
          this.saveMessage = "Изменения профиля сохранены";
          // Обновим user в sessionStorage
          userData.name = this.userData.name;
          sessionStorage.setItem('user', JSON.stringify(userData));
          this.$emit('profile-saved');
        } else {
          this.saveMessage = "Ошибка сохранения профиля";
        }
      } catch (err) {
        this.saveMessage = "Ошибка соединения с сервером";
      }
      setTimeout(() => { this.saveMessage = ""; }, 2000);
    }
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
  .form-group input[type="email"] {
    width: 100%;
    padding: 12px 15px;
    border: 1px solid #ddd;
    border-radius: 8px;
    font-size: 1rem;
  }
  
  .interests {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-top: 10px;
  }
  
  .interest-tag {
    background: #e0e8dd;
    padding: 8px 15px;
    border-radius: 20px;
    display: flex;
    align-items: center;
    gap: 5px;
  }
  
  .remove-interest {
    background: none;
    border: none;
    color: #666;
    cursor: pointer;
    display: flex;
    align-items: center;
  }
  
  .form-actions {
    margin-top: 30px;
    text-align: center;
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
    gap: 8px;
    transition: all 0.3s ease;
  }
  
  .save-btn:hover {
    background: #4a5547;
  }
  
  .dark-theme .form-group label {
    color: #f3f8f1;
  }
  
  .dark-theme .form-group input[type="text"],
  .dark-theme .form-group input[type="email"] {
    background: rgba(70, 78, 69, 0.7);
    border-color: #4a5547;
    color: #f3f8f1;
  }
  
  .dark-theme .interest-tag {
    background: #4a5547;
    color: #f3f8f1;
  }
  
  .dark-theme .save-btn {
    background: #f3f8f1;
    color: #394038;
  }
  
  .dark-theme .save-btn:hover {
    background: #e0e8dd;
  }
  </style>