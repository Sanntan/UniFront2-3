<template>
  <div class="content-container">
    <div class="intro">
      <h1>НАЙДИ СВОИХ В НАУКЕ</h1>
      <p>Сервис для поиска исследователей для работы над исследовательским проектом, работающих в схожей области или похожей тематике</p>
      <footer>
        <div class="social-links">
          <a href="#"><i class='bx bxl-github'></i></a>
          <a href="#"><i class='bx bxs-envelope'></i></a>
          <a href="#"><i class='bx bxl-telegram'></i></a>
        </div>
      </footer>
    </div>
    <form action="#" class="search-bar">
      <div class="file-input-wrapper">
        <input 
          type="file" 
          id="file-upload"
          accept=".pdf,.doc,.docx,.txt" 
          aria-label="Загрузить файл"
        >
        <label for="file-upload" class="file-input-label">
          <span class="placeholder-text">Загрузите файл...</span>
        </label>
      </div>
      <button type="submit" aria-label="Найти">
        <i class='bx bx-search'></i>
      </button>
    </form>
  </div>
</template>

<script>
export default {
  name: 'MainContent'
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
  display: block;
  width: 100%;
  padding: clamp(12px, 1.2vw, 18px) clamp(15px, 1.5vw, 25px);
  font-size: clamp(0.9em, 1.1vw, 1.2em);
  border: 2px solid #394038;
  border-radius: 30px;
  background-color: #394038;
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
  
  .search-bar {
    flex-direction: column;
    margin-top: 0;
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

</style>