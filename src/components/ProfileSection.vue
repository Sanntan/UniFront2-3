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
          >
        </div>
        
        <div class="form-group">
          <label>Научные интересы</label>
          <div class="interests">
            <span 
              v-for="(interest, index) in userData.interests" 
              :key="index" 
              class="interest-tag"
            >
              {{ interest }}
              <button @click="removeInterest(index)" class="remove-interest">
                <i class='bx bx-x'></i>
              </button>
            </span>
            <input 
              type="text" 
              v-model="newInterest" 
              placeholder="Добавить интерес"
              @keyup.enter="addInterest"
            >
          </div>
        </div>
        
        <div class="form-actions">
          <button class="save-btn" @click="saveProfile">
            <i class='bx bx-save'></i> Сохранить изменения
          </button>
        </div>
      </div>
    </section>
  </template>
  
  <script>
  export default {
    name: 'ProfileSection',
    data() {
      return {
        userData: {
          name: "Имя",
          email: "email@example.com",
          interests: ["Интерес 1", "Интерес 2"]
        },
        newInterest: ""
      }
    },
    methods: {
      addInterest() {
        if (this.newInterest.trim() && !this.userData.interests.includes(this.newInterest.trim())) {
          this.userData.interests.push(this.newInterest.trim());
          this.newInterest = "";
        }
      },
      removeInterest(index) {
        this.userData.interests.splice(index, 1);
      },
      saveProfile() {
        alert("Изменения профиля сохранены");
        //...
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