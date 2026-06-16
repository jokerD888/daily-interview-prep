<template>
  <div class="home-page">
    <div class="home-hero">
      <div class="greeting">
        <p class="greeting-label">{{ greeting }}</p>
        <h1 class="greeting-title">今天也要加油</h1>
      </div>
      <div class="quick-stats" v-if="progress">
        <div class="stat-pill">
          <span class="stat-num">{{ progress.daily_streak }}</span>
          <span class="stat-label">连续打卡</span>
        </div>
        <div class="stat-pill">
          <span class="stat-num">{{ progress.today_remaining }}</span>
          <span class="stat-label">待复习</span>
        </div>
      </div>
    </div>

    <div class="action-card" @click="$router.push('/review')">
      <div class="action-card-inner">
        <div class="ac-left">
          <span class="ac-tag">开始复习</span>
          <span class="ac-desc">{{ reviewHint }}</span>
        </div>
        <span class="ac-arrow">&rarr;</span>
      </div>
    </div>

    <nav class="home-nav">
      <router-link to="/upload" class="nav-item">
        <span class="nav-icon">&uarr;</span>
        <span class="nav-text">上传资料</span>
        <span class="nav-badge" v-if="materialsCount">{{ materialsCount }} 份</span>
      </router-link>
      <router-link to="/stats" class="nav-item">
        <span class="nav-icon">&#9689;</span>
        <span class="nav-text">学习统计</span>
      </router-link>
    </nav>

    <div class="seed-hint" v-if="!progress || progress.total_cards === 0">
      <p>首次使用？我们准备了 60 张高频八股卡片，覆盖 Java、Spring、操作系统。</p>
      <button class="seed-btn" @click="installSeed">一键安装种子卡片</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const progress = ref(null)
const materialsCount = ref(0)
const seedInstalled = ref(false)

const greeting = computed(() => {
  const h = new Date().getHours()
  if (h < 9) return '早上好'
  if (h < 12) return '上午好'
  if (h < 18) return '下午好'
  return '晚上好'
})

const reviewHint = computed(() => {
  if (!progress.value) return '加载中...'
  if (progress.value.today_remaining > 0) return `还有 ${progress.value.today_remaining} 张卡片待复习`
  if (progress.value.mastered_count > 0) return '今天的任务已完成'
  return '开始你的第一轮复习'
})

async function fetchProgress() {
  try {
    const res = await axios.get('/api/progress')
    progress.value = res.data
  } catch {}
}

async function fetchMaterials() {
  try {
    const res = await axios.get('/api/materials')
    materialsCount.value = res.data.length
  } catch {}
}

async function installSeed() {
  await axios.post('/api/seed/install')
  seedInstalled.value = true
  fetchProgress()
}

onMounted(() => {
  axios.defaults.headers.common['Authorization'] = `Bearer ${localStorage.getItem('token')}`
  fetchProgress()
  fetchMaterials()
})
</script>

<style scoped>
.home-page { padding: 24px 16px; }

.home-hero { margin-bottom: 24px; }
.greeting { margin-bottom: 20px; }
.greeting-label { font-size: 14px; color: var(--text-secondary); }
.greeting-title { font-family: var(--display); font-size: 28px; color: var(--text); margin-top: 4px; letter-spacing: 1px; }

.quick-stats { display: flex; gap: 12px; }
.stat-pill {
  flex: 1; background: var(--surface); border-radius: var(--radius); padding: 16px;
  display: flex; flex-direction: column; gap: 4px;
}
.stat-num { font-family: var(--display); font-size: 36px; color: var(--accent); line-height: 1; }
.stat-label { font-size: 13px; color: var(--text-secondary); }

.action-card {
  background: var(--accent);
  border-radius: 14px; margin-bottom: 20px; cursor: pointer;
  transition: transform 0.15s;
}
.action-card:active { transform: scale(0.98); }
.action-card-inner {
  display: flex; align-items: center; justify-content: space-between;
  padding: 20px;
}
.ac-tag { font-size: 18px; font-weight: 700; color: var(--accent-text); display: block; }
.ac-desc { font-size: 13px; color: rgba(255,255,255,0.7); margin-top: 2px; display: block; }
.ac-arrow { font-size: 24px; color: var(--accent-text); }

.home-nav { display: flex; gap: 12px; margin-bottom: 24px; }
.nav-item {
  flex: 1; background: var(--surface); border-radius: var(--radius); padding: 16px;
  display: flex; flex-direction: column; gap: 6px; text-decoration: none; position: relative;
  transition: background 0.15s;
}
.nav-item:active { background: var(--border); }
.nav-icon { font-size: 22px; color: var(--accent); }
.nav-text { font-size: 15px; color: var(--text); font-weight: 500; }
.nav-badge {
  position: absolute; top: 12px; right: 12px; font-size: 11px; color: var(--accent);
  font-family: var(--mono);
}

.seed-hint {
  background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius);
  padding: 20px; text-align: center;
}
.seed-hint p { font-size: 14px; color: var(--text-secondary); margin-bottom: 12px; line-height: 1.6; }
.seed-btn {
  padding: 10px 24px; border: 1px solid var(--accent); border-radius: 8px;
  background: transparent; color: var(--accent); font-size: 14px; font-family: var(--body);
  cursor: pointer; transition: all 0.2s;
}
.seed-btn:active { background: var(--accent-dim); }
</style>
