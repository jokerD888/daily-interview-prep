<template>
  <div class="stats-page">
    <div class="stats-header">
      <h1 class="stats-title">学习统计</h1>
    </div>

    <div v-if="loading" class="loading-state">加载中...</div>

    <div v-else class="stats-grid">
      <div class="mastery-ring">
        <svg viewBox="0 0 120 120" class="ring-svg">
          <circle cx="60" cy="60" r="52" fill="none" stroke="var(--border)" stroke-width="8" />
          <circle cx="60" cy="60" r="52" fill="none" stroke="var(--accent)" stroke-width="8"
            stroke-linecap="round" :stroke-dasharray="circumference"
            :stroke-dashoffset="dashOffset" transform="rotate(-90 60 60)" />
        </svg>
        <div class="ring-center">
          <span class="ring-num">{{ masteryPercent }}</span>
          <span class="ring-unit">%</span>
        </div>
      </div>

      <div class="stat-cards">
        <div class="stat-card">
          <span class="sc-num">{{ progress.mastered_count }}</span>
          <span class="sc-label">已掌握</span>
        </div>
        <div class="stat-card">
          <span class="sc-num">{{ progress.learning_count }}</span>
          <span class="sc-label">学习中</span>
        </div>
        <div class="stat-card">
          <span class="sc-num">{{ progress.today_reviewed }}</span>
          <span class="sc-label">今日已复习</span>
        </div>
        <div class="stat-card streak-card">
          <span class="sc-num streak-num">{{ progress.daily_streak }}</span>
          <span class="sc-label">连续打卡</span>
        </div>
      </div>
    </div>

    <div class="total-line" v-if="!loading">
      全部卡片 <strong>{{ progress.total_cards }}</strong> 张
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const loading = ref(true)
const progress = ref({ total_cards: 0, mastered_count: 0, learning_count: 0, daily_streak: 0, today_reviewed: 0, today_remaining: 0 })

const circumference = 2 * Math.PI * 52

const masteryPercent = computed(() => {
  if (progress.value.total_cards === 0) return 0
  return Math.round((progress.value.mastered_count / progress.value.total_cards) * 100)
})

const dashOffset = computed(() => circumference * (1 - masteryPercent.value / 100))

async function fetchProgress() {
  try {
    const res = await axios.get('/api/progress')
    progress.value = res.data
  } catch {}
  loading.value = false
}

onMounted(() => {
  axios.defaults.headers.common['Authorization'] = `Bearer ${localStorage.getItem('token')}`
  fetchProgress()
})
</script>

<style scoped>
.stats-page { padding: 24px 16px; }

.stats-header { margin-bottom: 28px; }
.stats-title { font-family: var(--display); font-size: 28px; color: var(--text); letter-spacing: 1px; }

.loading-state { text-align: center; color: var(--text-secondary); margin-top: 80px; font-size: 15px; }

.stats-grid { display: flex; gap: 24px; align-items: flex-start; margin-bottom: 24px; }

.mastery-ring { position: relative; width: 120px; height: 120px; flex-shrink: 0; }
.ring-svg { width: 100%; height: 100%; }
.ring-center {
  position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; flex-direction: column;
}
.ring-num { font-family: var(--display); font-size: 32px; color: var(--accent); line-height: 1; }
.ring-unit { font-size: 12px; color: var(--text-secondary); margin-top: 2px; }

.stat-cards { flex: 1; display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.stat-card {
  background: var(--surface); border-radius: var(--radius); padding: 14px;
  display: flex; flex-direction: column; gap: 4px;
}
.sc-num { font-family: var(--display); font-size: 28px; color: var(--text); }
.sc-label { font-size: 13px; color: var(--text-secondary); }
.streak-card { background: var(--accent-dim); border: 1px solid var(--accent); opacity: 0.6; }
.streak-num { color: var(--accent); }

.total-line { font-size: 14px; color: var(--text-secondary); padding: 16px 0; border-top: 1px solid var(--border); }
.total-line strong { color: var(--text); }
</style>
