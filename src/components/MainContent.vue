<template>
  <div class="content-container">
    <!-- Левая часть -->
    <div class="intro">
      <h1>НАЙДИ СВОИХ В НАУКЕ</h1>
      <p>
        Сервис для поиска исследователей для работы над исследовательским проектом, работающих в схожей области или похожей тематике
      </p>
      <footer>
        <div class="social-links">
          <a href="https://github.com/Sanntan/UniFront2-3" target="_blank">
            <i class='bx bxl-github'></i>
          </a>
          <div class="email-wrapper" @mouseenter="cancelEmailHide" @mouseleave="scheduleEmailHide">
            <i class='bx bxs-envelope' @click="toggleEmailPopup"></i>
            <transition name="fade">
              <div
                v-if="showEmailPopup"
                class="email-popup"
                :class="{ 'dark-popup': isDarkTheme }"
                @mouseenter="cancelEmailHide"
                @mouseleave="scheduleEmailHide"
              >
                <p @click="copyEmail('stud0000286472@utmn.ru')">stud0000286472@utmn.ru</p>
                <p @click="copyEmail('stud0000282272@utmn.ru')">stud0000282272@utmn.ru</p>
              </div>
            </transition>
          </div>
        </div>
      </footer>
    </div>

    <!-- Правая часть -->
    <div class="right-panel">
      <form class="search-bar search-bar-column" @submit.prevent>
        <div class="file-input-wrapper file-hover-transition">
          <input 
            type="file" 
            id="file-upload"
            accept=".pdf,.doc,.docx,.txt"
            @change="handleFileChange"
          >
          <label for="file-upload" class="file-input-label">
            <span class="placeholder-text">{{ fileName || 'Загрузите файл...' }}</span>
          </label>
        </div>

        <div class="file-input-wrapper text-input-wrapper file-hover-transition">
          <input
            type="text"
            class="file-input-label"
            placeholder="Введите текст"
            v-model="inputText"
            @keydown.enter.prevent="handleTextSubmit"
            style="background: #fff; color: #394038; border: 2px solid #394038;"
          >
        </div>
      </form>

      <!-- 🔄 Прогресс-бар -->
      <div v-if="isProcessing" class="progress-wrapper">
        <div class="progress-bar" :style="{ width: progress + '%' }"></div>
      </div>

      <!-- ✅ Результаты -->
      <div v-if="showResults" class="results-container">
        <div class="article-card" v-for="(article, index) in results" :key="index">
          <h3>{{ article.title }}</h3>
          <p><strong>Авторы:</strong> {{ article.authors }}</p>
          <p><a :href="article.article_url" target="_blank">Ссылка на статью</a></p>
          <button class="favorite-button" @click="handleAddToFavorites(article)">
            <i class="bx bxs-star"></i> В избранное
          </button>
        </div>
      </div>
    </div>

    <!-- 🪧 Уведомление -->
    <div v-if="showToast" class="custom-toast" :class="{ 'dark-toast': isDarkTheme }">
      {{ toastMessage }}
    </div>
  </div>
</template>

<script>
export default {
  name: 'MainContent',
  data() {
    return {
      inputText: '',
      fileName: '',
      showResults: false,
      results: [],
      progress: 0,
      isProcessing: false,
      showToast: false,
      toastMessage: '',
      isDarkTheme: false,
      showEmailPopup: false,
      hideEmailTimer: null,
    };
  },
  watch: {
    inputText(newValue) {
      this.showResults = newValue.trim().length > 0;
    }
  },
  mounted() {
    this.checkTheme();
    const observer = new MutationObserver(this.checkTheme);
    observer.observe(document.documentElement, { attributes: true, attributeFilter: ['class'] });
  },
  methods: {
    checkTheme() {
      this.isDarkTheme = document.documentElement.classList.contains('dark-theme');
    },
    showSuccessToast(message) {
      this.toastMessage = message;
      this.showToast = true;
      setTimeout(() => {
        this.showToast = false;
        this.toastMessage = '';
      }, 3000);
    },
    toggleEmailPopup() {
      this.showEmailPopup = !this.showEmailPopup;
    },
    copyEmail(email) {
      navigator.clipboard.writeText(email).then(() => {
        this.showSuccessToast(`📋 Скопировано: ${email}`);
        this.showEmailPopup = false;
      });
    },
    scheduleEmailHide() {
      this.hideEmailTimer = setTimeout(() => {
        this.showEmailPopup = false;
      }, 400); // Задержка перед скрытием
    },

    cancelEmailHide() {
      if (this.hideEmailTimer) {
        clearTimeout(this.hideEmailTimer);
        this.hideEmailTimer = null;
      }
    },
    async handleFileChange(e) {
      const file = e.target.files[0];
      if (!file) return;

      this.fileName = file.name;
      this.showResults = false;
      this.results = [];
      this.progress = 0;
      this.isProcessing = true;

      const formData = new FormData();
      formData.append("file", file);

      const interval = setInterval(() => {
        if (this.progress < 90) {
          this.progress += Math.random() * 5;
        }
      }, 150);

      try {
        const response = await fetch("http://localhost:8000/find_similar", {
          method: "POST",
          body: formData
        });

        if (!response.ok) throw new Error("Ошибка запроса");

        const data = await response.json();
        this.results = data;
        this.showResults = true;
      } catch (err) {
        console.error("Ошибка при получении похожих статей:", err);
        this.results = [];
      } finally {
        clearInterval(interval);
        this.progress = 100;
        setTimeout(() => {
          this.isProcessing = false;
          this.progress = 0;
        }, 800);
      }
    },
    async handleTextSubmit() {
      if (!this.inputText.trim()) return;

      this.fileName = '';
      this.showResults = false;
      this.results = [];
      this.progress = 0;
      this.isProcessing = true;

      const formData = new FormData();
      formData.append("text", this.inputText.trim());

      const interval = setInterval(() => {
        if (this.progress < 90) {
          this.progress += Math.random() * 5;
        }
      }, 150);

      try {
        const response = await fetch("http://localhost:8000/find_similar_text", {
          method: "POST",
          body: formData
        });

        if (!response.ok) throw new Error("Ошибка запроса");

        const data = await response.json();
        this.results = data;
        this.showResults = true;
      } catch (err) {
        console.error("Ошибка при поиске по тексту:", err);
        this.results = [];
      } finally {
        clearInterval(interval);
        this.progress = 100;
        setTimeout(() => {
          this.isProcessing = false;
          this.progress = 0;
        }, 800);
      }
    },
    async handleAddToFavorites(article) {
      const user = JSON.parse(sessionStorage.getItem('user'));
      if (!user || !user.user_id) {
        this.$emit('open-auth');
        return;
      }

      try {
        const res = await fetch("http://localhost:8000/api/favorites/add", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            user_id: user.user_id,
            article_id: article.article_id
          })
        });

        const data = await res.json();

        if (res.status === 409 || data.message?.includes("уже")) {
          this.showSuccessToast("⚠️ Статья уже в избранном");
        } else if (data.success) {
          this.showSuccessToast("✅ Статья успешно добавлена в избранное!");
          this.$emit("refresh-favorites");
        } else {
          this.showSuccessToast("⚠️ " + (data.message || "Не удалось добавить в избранное."));
        }
      } catch (err) {
        console.error("Ошибка добавления в избранное:", err);
        this.showSuccessToast("❌ Ошибка при добавлении в избранное.");
      }
    },
  }
}
</script>

<style scoped>
.content-container {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 clamp(20px, 5%, 100px);
  gap: clamp(30px, 10vw, 200px);
  width: 100%;
  max-width: 1800px;
  margin: 0 auto;
  box-sizing: border-box;
  transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

.intro {
  width: min(45%, 550px);
  min-width: min(90vw, 400px);
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  transition: all 0.4s ease;
}

.intro h1 {
  width: 100%;
  font-size: clamp(2em, 4vw, 3.5em);
  margin-bottom: 0.5em;
  font-family: Cambria, Cochin, Georgia, Times, 'Times New Roman', serif;
  font-weight: bold;
  line-height: 1.2;
  transition: font-size 0.4s ease;
}

.intro p {
  width: 100%;
  font-size: clamp(0.9em, 1.2vw, 1.2em);
  margin-bottom: 2em;
  font-family: Verdana, Geneva, Tahoma, sans-serif;
  line-height: 1.7;
  transition: all 0.4s ease;
}

.search-bar {
  width: min(45%, 600px);
  min-width: min(90vw, 400px);
  max-width: 650px;
  display: flex;
  gap: 10px;
  margin-top: clamp(0px, 5vh, 50px);
  transition: all 0.4s ease;
}

.file-input-wrapper {
  position: relative;
  width: 100%;
}

.file-input-wrapper input[type="file"] {
  position: absolute;
  width: 100%;
  height: 100%;
  opacity: 0;
  cursor: pointer;
}

.file-input-label {
  min-height: 56px;
  box-sizing: border-box;
  display: block;
  width: 100%;
  padding: clamp(12px, 1.2vw, 18px) clamp(15px, 1.5vw, 25px);
  font-size: clamp(0.9em, 1.1vw, 1.2em);
  border: 2px solid #2d2e2d;
  border-radius: 30px;
  background-color: #2d2e2d;
  color: #f3f8f1;
  box-shadow: 0 2px 10px rgba(0, 0, 0, .5);
  cursor: pointer;
  transition: all 0.3s ease;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.placeholder-text {
  color: #f3f8f1;
}

.search-bar button {
  width: clamp(60px, 7vw, 80px);
  font-size: clamp(0.9em, 1.1vw, 1.2em);
  border: 2px solid #394038;
  border-radius: 30px;
  outline: none;
  background-color: #394038;
  color: #f3f8f1;
  transition: all 0.3s ease;
  box-shadow: 0 2px 10px rgba(0, 0, 0, .5);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.search-bar button:hover {
  transform: scale(1.05);
}

.social-links {
  display: flex;
  gap: clamp(20px, 2vw, 30px);
  transition: all 0.4s ease;
}

.social-links i {
  font-size: clamp(1.3rem, 2vw, 2rem);
  color: #394038;
  transition: all 0.3s ease;
}

.social-links i:hover {
  transform: scale(1.1);
}

@media (max-width: 768px) {
  .content-container {
    flex-direction: column;
    padding: 15px 20px;
    gap: 30px;
    align-items: center;
    transition: all 0.4s ease;
  }

  .intro, .search-bar {
    width: 100%;
    min-width: auto;
    max-width: 100%;
  }
  
  .intro h1 {
    font-size: 1.8em;
  }
  
  .intro p {
    font-size: 0.9em;
  }
  
  .search-bar, .search-bar-column{
    flex-direction: column;
    gap: 24px;
    align-items: stretch;
  }
  
  .search-bar button {
    width: 100%;
    height: 50px;
  }
  
  .social-links i {
    font-size: 1.3rem;
  }
}

@media (min-width: 769px) and (max-width: 1024px) {
  .content-container {
    gap: clamp(80px, 10vw, 120px);
    padding: 0 clamp(40px, 8%, 80px);
  }
  
  .search-bar {
    min-width: min(50vw, 500px);
  }
}

@media (min-width: 1025px) {
  .content-container {
    gap: clamp(150px, 20vw, 250px);
    padding: 0 clamp(60px, 10%, 120px);
  }
  
  .search-bar {
    min-width: min(40vw, 550px);
  }
}
.dark-theme .intro h1,
.dark-theme .intro p {
  color: #f3f8f1;
}

.dark-theme .social-links i {
  color: #f3f8f1;
}

.dark-theme .file-input-label {
  background-color: #f3f8f1;
  border-color: #f3f8f1;
  color: #394038;
}

.dark-theme .placeholder-text {
  color: #394038;
}

.dark-theme .search-bar button {
  background-color: #f3f8f1;
  border-color: #f3f8f1;
  color: #394038;
}

.dark-theme .search-bar button:hover {
  background-color: #e0e8dc;
}

.file-hover-transition .file-input-label:hover,
.file-hover-transition .file-input-label:focus-within {
  border-color: #99aa8e;
  box-shadow: 0 4px 16px rgba(57,64,56,0.09);
  transform: scale(1.03);
  z-index: 2;
}

.results-container {
  margin-top: 40px;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px;
  width: 100%;
  max-width: 100%;
  box-sizing: border-box;
}

.article-card {
  border: 2px solid #394038;
  border-radius: 20px;
  padding: 20px;
  background: #fff;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  transition: transform 0.2s ease;
}

.article-card:hover {
  transform: scale(1.02);
}

.favorite-button {
  margin-top: 10px;
  background: #394038;
  color: #f3f8f1;
  border: none;
  padding: 10px 16px;
  border-radius: 12px;
  cursor: pointer;
  font-size: 14px;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.3);
}

.favorite-button i {
  font-size: 18px;
}

.favorite-button:hover {
  background: #4c5549;
}

.dark-theme .article-card {
  background: #394038;
  border-color: #f3f8f1;
  color: #f3f8f1;
  box-shadow: 0 2px 8px rgba(255,255,255,0.1);
}

.dark-theme .article-card a {
  color: #e0e8dc;
  text-decoration: underline;
}

.dark-theme .favorite-button {
  background: #f3f8f1;
  color: #394038;
  box-shadow: 0 2px 6px rgba(255,255,255,0.3);
}

.dark-theme .favorite-button:hover {
  background: #e0e8dc;
}

.progress-wrapper {
  width: 100%;
  max-width: 650px;
  height: 12px;
  border-radius: 30px;
  background-color: #c7d7bd;
  overflow: hidden;
  margin: 20px 0;
  box-shadow: inset 0 1px 4px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
}

.progress-bar {
  height: 100%;
  background-color: #394038;
  transition: width 0.3s ease;
}

.dark-theme .progress-wrapper {
  background-color: #4a5347;
  box-shadow: inset 0 1px 4px rgba(255, 255, 255, 0.2);
}

.dark-theme .progress-bar {
  background-color: #f3f8f1;
}

.custom-toast {
  position: fixed;
  bottom: 30px;
  right: 30px;
  background-color: #394038;
  color: #f3f8f1;
  padding: 12px 20px;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
  font-size: 0.95rem;
  z-index: 9999;
  transition: all 0.3s ease;
}
.dark-toast {
  background-color: #f3f8f1;
  color: #394038;
}

.email-wrapper {
  position: relative;
  cursor: pointer;
}

.email-popup {
  position: absolute;
  top: 30px;
  left: -20px;
  background-color: #f3f8f1;
  color: #394038;
  border: 2px solid #394038;
  border-radius: 12px;
  padding: 10px 15px;
  font-size: 14px;
  white-space: nowrap;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
  z-index: 1000;
  transition: all 0.3s ease;
}

.email-popup p {
  margin: 5px 0;
  cursor: pointer;
  user-select: none;
}

.email-popup p:hover {
  text-decoration: underline;
}

.dark-theme .email-popup {
  background-color: #394038;
  color: #f3f8f1;
  border-color: #f3f8f1;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}


</style>