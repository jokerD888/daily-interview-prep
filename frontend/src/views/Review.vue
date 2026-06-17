<template>
  <div class="review-page">
    <div class="review-topbar">
      <div class="progress-track">
        <div class="progress-fill" :style="{ width: progress + '%' }"></div>
      </div>
      <span class="counter">{{ currentIndex + 1 }}<span class="counter-total"> / {{ cards.length }}</span></span>
    </div>

    <div v-if="cards.length === 0" class="empty-state">
      <span class="empty-icon">&#10022;</span>
      <p>今天的卡片已全部完成</p>
      <p class="empty-sub">明天再来，知识需要时间沉淀</p>
      <router-link to="/" class="back-link">返回首页</router-link>
    </div>

    <div v-else class="card-stage">
      <transition name="card-swap" mode="out-in">
        <div class="card-container" :key="card.card_id" @click="flipped = !flipped">
          <div class="flashcard" :class="{ flipped }">
            <div class="card-face card-front">
              <div class="card-meta">
                <span class="card-tag" :class="card.state === 'new' ? 'tag-new' : 'tag-review'">
                  {{ card.state === 'new' ? '新卡' : '复习' }}
                </span>
                <span class="card-stars">{{ '★'.repeat(card.importance_score) }}{{ '☆'.repeat(5 - card.importance_score) }}</span>
              </div>
              <p class="card-question">{{ card.question }}</p>
              <p class="flip-hint">轻触卡片翻转</p>
            </div>
            <div class="card-face card-back">
              <p class="card-answer">{{ card.answer }}</p>
              <div class="review-actions">
                <button class="btn-forgot" @click.stop="submitReview('forgot')">忘了</button>
                <button class="btn-correct" @click.stop="submitReview('correct')">记住了</button>
              </div>
            </div>
          </div>
        </div>
      </transition>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const cards = ref([])
const currentIndex = ref(0)
const flipped = ref(false)

const card = computed(() => cards.value[currentIndex.value] || {})
const progress = computed(() => cards.value.length ? ((currentIndex.value) / cards.value.length) * 100 : 0)

async function fetchCards() {
  const res = await axios.get('/api/daily-cards')
  cards.value = res.data
}

async function submitReview(result) {
  const c = card.value
  try {
    await axios.post(`/api/reviews?card_id=${c.card_id}&result=${result}`)
  } catch {}
  flipped.value = false
  if (currentIndex.value < cards.value.length - 1) {
    currentIndex.value++
  } else {
    cards.value = []
  }
}

onMounted(() => {
  axios.defaults.headers.common['Authorization'] = `Bearer ${localStorage.getItem('token')}`
  fetchCards()
})
</script>

<style scoped>
.review-page { padding: 0; min-height: 100dvh; display: flex; flex-direction: column; }

.review-topbar { display: flex; align-items: center; gap: 12px; padding: 12px 16px; }
.progress-track { flex: 1; height: 3px; background: var(--border); border-radius: 2px; overflow: hidden; }
.progress-fill { height: 100%; background: var(--accent); border-radius: 2px; transition: width 0.3s ease; }
.counter { font-family: var(--mono); font-size: 14px; color: var(--text-secondary); white-space: nowrap; }
.counter-total { color: var(--border); }

.empty-state {
  flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center;
  padding: 48px; text-align: center;
}
.empty-icon { font-size: 48px; color: var(--accent); margin-bottom: 16px; }
.empty-state p { font-size: 17px; color: var(--text); }
.empty-sub { color: var(--text-secondary); font-size: 14px; margin-top: 8px; }
.back-link { color: var(--accent); margin-top: 24px; text-decoration: none; font-size: 15px; }

.card-stage { flex: 1; display: flex; align-items: flex-start; justify-content: center; padding: 8px 16px 16px; }
.card-container { width: 100%; max-width: 400px; perspective: 1200px; }

.flashcard {
  width: 100%; min-height: 380px; position: relative;
  transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1);
  transform-style: preserve-3d;
}
.flashcard.flipped { transform: rotateY(180deg); }

.card-face {
  position: absolute; inset: 0; backface-visibility: hidden;
  border-radius: 18px; padding: 24px;
  display: flex; flex-direction: column;
  background: var(--surface);
  border: 1px solid var(--border);
  box-shadow: 0 4px 24px rgba(0,0,0,0.3);
}

.card-front { justify-content: space-between; }
.card-back {
  transform: rotateY(180deg);
  border-color: var(--accent);
  box-shadow: 0 4px 24px rgba(0,0,0,0.15);
}

.card-meta { display: flex; align-items: center; gap: 10px; }
.card-tag { font-size: 11px; font-family: var(--mono); padding: 4px 10px; border-radius: 6px; font-weight: 500; }
.tag-new { background: var(--accent-dim); color: var(--accent); }
.tag-review { background: var(--accent-dim); color: var(--success); }
.card-stars { font-size: 11px; color: var(--accent); letter-spacing: 1px; }

.card-question {
  font-size: 18px; line-height: 1.7; color: var(--text);
  margin: auto 0; padding: 16px 0;
}
.card-answer {
  font-size: 15px; line-height: 1.75; color: var(--text);
  flex: 1; overflow-y: auto; padding: 8px 0;
}

.flip-hint { font-size: 13px; color: var(--text-secondary); text-align: center; opacity: 0.7; }

.review-actions { display: flex; gap: 12px; margin-top: 16px; }
.btn-forgot, .btn-correct {
  flex: 1; padding: 14px 0; border: none; border-radius: 12px;
  font-size: 16px; font-weight: 600; font-family: var(--body); cursor: pointer;
  transition: opacity 0.15s;
}
.btn-forgot { background: var(--danger); color: #fff; }
.btn-correct { background: var(--success); color: #fff; }
.btn-forgot:active, .btn-correct:active { opacity: 0.8; }

.card-swap-enter-active { transition: opacity 0.2s ease, transform 0.2s ease; }
.card-swap-leave-active { transition: opacity 0.15s ease; }
.card-swap-enter-from { opacity: 0; transform: translateX(20px); }
.card-swap-leave-to { opacity: 0; }
</style>
