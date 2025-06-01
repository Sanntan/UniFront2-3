<template>
  <div class="personal-cabinet" :class="{ 'dark-theme': isDarkTheme }">
    <div class="cabinet-container">
      <aside class="sidebar">
        <div class="user-profile">
          <div class="avatar">
            <i class='bx bx-user'></i>
          </div>
          <h2>{{ user.name }}</h2>
          <p>{{ user.email }}</p>
        </div>
        <nav class="cabinet-nav">
          <button
            v-for="tab in tabs"
            :key="tab.id"
            :class="{ active: activeTab === tab.id }"
            @click="switchTab(tab.id)"
          >
            <i :class="tab.icon"></i>
            {{ tab.name }}
          </button>
        </nav>
      </aside>
      <main class="cabinet-content">
        <FavoritesSection
          v-if="activeTab === 'favorites'"
          :favorites="favorites"
          @remove-favorite="removeFavorite"
        />
        <ProfileSection
          v-if="activeTab === 'profile'"
          :user="user"
          @profile-saved="fetchUserData"
        />
      </main>
    </div>
  </div>
</template>

<script>
import FavoritesSection from './FavoritesSection.vue'
import ProfileSection from './ProfileSection.vue'

export default {
  name: 'PersonalCabinet',
  components: {
    FavoritesSection,
    ProfileSection
  },
  data() {
    return {
      isDarkTheme: false,
      activeTab: 'favorites',
      tabs: [
        { id: 'favorites', name: 'Избранное', icon: 'bx bx-bookmark-heart' },
        { id: 'profile', name: 'Профиль', icon: 'bx bx-user-circle' }
      ],
      favorites: [],
      user: {
        name: '',
        email: ''
      }
    }
  },
  methods: {
    switchTab(tabId) {
      this.activeTab = tabId;
      if (tabId === 'favorites') {
        this.fetchFavorites();
      }
    },
    async removeFavorite(index) {
      const userData = JSON.parse(sessionStorage.getItem('user'));
      const articleId = this.favorites[index].article_id;
      try {
        const res = await fetch(`http://localhost:8000/api/favorites/remove`, {
          method: 'DELETE',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ user_id: userData.user_id, article_id: articleId })
        });
        const data = await res.json();
        if (data.success) {
          this.favorites.splice(index, 1);
        }
      } catch (e) {
        console.error("Ошибка удаления из избранного:", e);
      }
    },
    checkTheme() {
      this.isDarkTheme = document.documentElement.classList.contains('dark-theme');
    },
    async fetchUserData() {
      const userData = JSON.parse(sessionStorage.getItem('user'));
      if (!userData) return;
      try {
        const res = await fetch(`http://localhost:8000/api/user/${userData.user_id}`);
        const data = await res.json();
        if (data.success) {
          this.user = data.user;
        }
      } catch (e) {
        console.error("Ошибка загрузки профиля:", e);
      }
    },
    async fetchFavorites() {
      const userData = JSON.parse(sessionStorage.getItem('user'));
      if (!userData) return;
      try {
        const res = await fetch(`http://localhost:8000/api/favorites/${userData.user_id}`);
        const data = await res.json();

        // Для обратной совместимости: если сервер возвращает просто массив
        this.favorites = Array.isArray(data) ? data : (data.favorites || []);
      } catch (e) {
        console.error("Ошибка загрузки избранного:", e);
      }
    },
  },
  mounted() {
    this.checkTheme();
    const themeObserver = new MutationObserver(this.checkTheme);
    themeObserver.observe(document.documentElement, {
      attributes: true,
      attributeFilter: ['class']
    });
    this.fetchUserData();
    this.fetchFavorites(); // <-- обязательно
  }
}
</script>
  
  <style scoped>
  .personal-cabinet {
    background-color: #c6dab7;
    background: url('../assets/images/Fon.png') no-repeat center center fixed;
    background-size: cover;
    min-height: calc(100vh - 80px); 
    padding-top: 80px; 
    display: flex;
    flex-direction: column;
  }
  
  .cabinet-container {
    max-width: 1200px;
    width: 100%;
    margin: 0 auto;
    display: grid;
    grid-template-columns: 250px 1fr;
    gap: 20px;
    flex: 1;
    padding: 20px;
  }
  
  .sidebar {
    background: rgba(255, 255, 255, 0.9);
    border-radius: 15px;
    padding: 20px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    height: fit-content;
  }
  
  .user-profile {
    text-align: center;
    margin-bottom: 30px;
  }
  
  .avatar {
    width: 80px;
    height: 80px;
    background: #e0e0e0;
    border-radius: 50%;
    margin: 0 auto 15px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .avatar i {
    font-size: 40px;
    color: #666;
  }
  
  .user-profile h2 {
    font-size: 1.2rem;
    color: #394038;
    margin-bottom: 5px;
  }
  
  .user-profile p {
    font-size: 0.9rem;
    color: #666;
  }
  
  .cabinet-nav {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
  
  .cabinet-nav button {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 12px 15px;
    background: transparent;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    color: #394038;
    font-size: 0.95rem;
    transition: all 0.3s ease;
  }
  
  .cabinet-nav button:hover {
    background: #f3f8f1;
  }
  
  .cabinet-nav button.active {
    background: #394038;
    color: white;
  }
  
  .cabinet-nav button i {
    font-size: 1.2rem;
  }
  
  .cabinet-content {
    background: rgba(255, 255, 255, 0.9);
    border-radius: 15px;
    padding: 25px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  }
  
  .dark-theme .personal-cabinet {
    background-color: #3a4036;
    background: url('../assets/images/Fon2.png') no-repeat center center fixed;
    background-size: cover;
  }
  
  .dark-theme .sidebar,
  .dark-theme .cabinet-content {
    background: rgba(32, 37, 31, 0.9);
  }
  
  .dark-theme .user-profile h2 {
    color: #f3f8f1;
  }
  
  .dark-theme .user-profile p {
    color: #ccc;
  }
  
  .dark-theme .cabinet-nav button {
    color: #f3f8f1;
  }
  
  .dark-theme .cabinet-nav button:hover {
    background: rgba(255, 255, 255, 0.1);
  }
  
  .dark-theme .cabinet-nav button.active {
    background: #f3f8f1;
    color: #394038;
  }
  
  @media (max-width: 768px) {
    .cabinet-container {
      grid-template-columns: 1fr;
    }
    
    .personal-cabinet {
      padding: 80px 10px 10px;
    }
  }
  </style>