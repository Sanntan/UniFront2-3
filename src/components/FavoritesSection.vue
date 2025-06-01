<template>
  <section class="favorites-section">
    <h2><i class='bx bx-bookmark-heart'></i> Избранное</h2>

    <div class="filters">
      <div class="search-box">
        <i class='bx bx-search'></i>
        <input type="text" placeholder="Поиск в избранном...">
      </div>
      <select class="sort-select">
        <option>Сортировать по дате</option>
        <option>Сортировать по названию</option>
      </select>
    </div>

    <div class="favorites-list">
      <div
        v-for="(item, index) in favorites"
        :key="index"
        class="favorite-item"
      >
        <div class="item-content">
          <h3>{{ item.title }}</h3>
          <p class="authors">{{ Array.isArray(item.authors) ? item.authors.join(', ') : item.authors }}</p>
          <p class="link" v-if="item.article_url">
            <a :href="item.article_url" target="_blank">Ссылка на статью</a>
          </p>
          <p class="abstract" v-if="item.abstract">{{ item.abstract }}</p>
          <div class="meta">
            <span class="journal" v-if="item.journal">{{ item.journal }}</span>
            <span class="year" v-if="item.year">{{ item.year }}</span>
            <span class="tags" v-if="item.tags">
              <span v-for="(tag, i) in item.tags" :key="i" class="tag">{{ tag }}</span>
            </span>
          </div>
        </div>
        <div class="item-actions">
          <button class="action-btn" @click="$emit('remove-favorite', index)">
            <i class='bx bx-trash'></i>
          </button>
        </div>
      </div>

      <div v-if="favorites.length === 0" class="empty-state">
        <i class='bx bx-bookmark-heart'></i>
        <p>Ваше избранное пусто</p>
        <router-link to="/" class="browse-btn">
          <i class='bx bx-search-alt'></i> Найти материалы
        </router-link>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: 'FavoritesSection',
  props: {
    favorites: {
      type: Array,
      required: true
    }
  },
  emits: ['remove-favorite']
}
</script>

<style scoped>
.favorites-section {
  width: 100%;
}

h2 {
  color: #394038;
  font-size: 1.4rem;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
}

h2 i {
  font-size: 1.6rem;
}

.filters {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
  gap: 15px;
}

.search-box {
  flex: 1;
  position: relative;
}

.search-box i {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: #666;
}

.search-box input {
  width: 100%;
  padding: 10px 15px 10px 40px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 0.95rem;
}

.sort-select {
  padding: 10px 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 0.95rem;
  background: white;
}

.favorites-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.favorite-item {
  display: flex;
  background: #f3f8f1;
  border-radius: 10px;
  padding: 20px;
  transition: all 0.3s ease;
}

.favorite-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 10px rgba(0, 0, 0, 0.1);
}

.item-content {
  flex: 1;
}

.favorite-item h3 {
  font-size: 1.1rem;
  color: #394038;
  margin-bottom: 8px;
}

.authors {
  font-size: 0.9rem;
  color: #555;
  margin-bottom: 6px;
  font-style: italic;
}

.link a {
  font-size: 0.9rem;
  color: #394038;
  text-decoration: underline;
}

.abstract {
  font-size: 0.9rem;
  color: #555;
  margin: 8px 0 12px;
  line-height: 1.5;
}

.meta {
  display: flex;
  gap: 15px;
  font-size: 0.8rem;
  color: #666;
}

.tags {
  display: flex;
  gap: 8px;
  margin-left: auto;
}

.tag {
  background: #e0e8dd;
  padding: 3px 8px;
  border-radius: 12px;
  font-size: 0.75rem;
}

.item-actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-left: 15px;
}

.action-btn {
  background: none;
  border: none;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #666;
  transition: all 0.2s ease;
}

.action-btn:hover {
  background: rgba(0, 0, 0, 0.05);
  color: #394038;
}

.action-btn i {
  font-size: 1.2rem;
}

.empty-state {
  text-align: center;
  padding: 50px 20px;
  color: #666;
}

.empty-state i {
  font-size: 3rem;
  margin-bottom: 15px;
  color: #aaa;
}

.empty-state p {
  margin-bottom: 20px;
  font-size: 1.1rem;
}

.browse-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: #394038;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.browse-btn:hover {
  background: #4a5547;
}

/* 🌙 Тёмная тема */
.dark-theme .favorites-section h2,
.dark-theme .favorite-item h3 {
  color: #f3f8f1;
}

.dark-theme .authors,
.dark-theme .abstract,
.dark-theme .meta,
.dark-theme .empty-state {
  color: #ccc;
}

.dark-theme .favorite-item {
  background: rgba(70, 78, 69, 0.7);
}

.dark-theme .search-box input,
.dark-theme .sort-select {
  background: rgba(70, 78, 69, 0.7);
  border-color: #4a5547;
  color: #f3f8f1;
}

.dark-theme .search-box i {
  color: #ccc;
}

.dark-theme .tag {
  background: #e0e8dd;
  color: #394038;
}

.dark-theme .link a {
  color: #e0e8dc;
}

.dark-theme .browse-btn {
  background: #f3f8f1;
  color: #394038;
}

.dark-theme .browse-btn:hover {
  background: #e0e8dd;
}

@media (max-width: 768px) {
  .favorite-item {
    flex-direction: column;
  }

  .item-actions {
    flex-direction: row;
    margin-left: 0;
    margin-top: 15px;
    justify-content: flex-end;
  }

  .filters {
    flex-direction: column;
  }
}
</style>
