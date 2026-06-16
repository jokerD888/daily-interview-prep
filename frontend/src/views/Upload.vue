<template>
  <div class="upload-page">
    <div class="upload-header">
      <h1 class="upload-title">上传资料</h1>
      <p class="upload-desc">上传 PDF 或 Markdown 文件，AI 自动拆解为记忆卡片</p>
    </div>

    <label class="drop-zone">
      <input type="file" accept=".pdf,.md" @change="handleFile" hidden ref="fileInput" />
      <span class="dz-icon">&uarr;</span>
      <span class="dz-text">{{ uploading ? '上传中...' : '点击选择文件' }}</span>
      <span class="dz-hint">PDF &middot; Markdown &middot; 最大 20MB</span>
    </label>

    <div class="material-list" v-if="materials.length > 0">
      <h2 class="list-title">已上传</h2>
      <div class="material-item" v-for="m in materials" :key="m.id">
        <div class="mi-info">
          <span class="mi-name">{{ m.title }}</span>
          <span class="mi-meta">{{ m.file_type.toUpperCase() }} &middot; {{ statusLabel(m.status) }} &middot; {{ m.card_count }} 卡片</span>
        </div>
        <div class="mi-actions">
          <button v-if="m.status === 'uploaded'" class="mi-btn" @click="generateCards(m.id)">生成卡片</button>
          <span class="mi-date">{{ formatTime(m.created_at) }}</span>
          <button class="mi-delete" @click="handleDelete(m.id)">&times;</button>
        </div>
      </div>
    </div>

    <div class="empty-hint" v-else>
      <span class="empty-icon">&#128196;</span>
      <p>还没有上传资料</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const materials = ref([])
const uploading = ref(false)
const fileInput = ref(null)

async function fetchMaterials() {
  const res = await axios.get('/api/materials')
  materials.value = res.data
}

async function handleFile(e) {
  const file = e.target.files[0]
  if (!file) return
  uploading.value = true
  const form = new FormData()
  form.append('file', file)
  try {
    await axios.post('/api/materials', form)
    fetchMaterials()
  } catch {}
  uploading.value = false
}

async function generateCards(id) {
  try {
    await axios.post(`/api/materials/${id}/generate`)
    fetchMaterials()
  } catch {}
}

async function handleDelete(id) {
  await axios.delete(`/api/materials/${id}`)
  fetchMaterials()
}

function statusLabel(s) {
  const map = { uploaded: '待处理', processing: '生成中', completed: '已完成', failed: '失败' }
  return map[s] || s
}

function formatTime(t) {
  return new Date(t).toLocaleDateString('zh-CN')
}

onMounted(() => {
  axios.defaults.headers.common['Authorization'] = `Bearer ${localStorage.getItem('token')}`
  fetchMaterials()
})
</script>

<style scoped>
.upload-page { padding: 24px 16px; }

.upload-header { margin-bottom: 24px; }
.upload-title { font-family: var(--display); font-size: 28px; color: var(--text); letter-spacing: 1px; }
.upload-desc { font-size: 14px; color: var(--text-secondary); margin-top: 6px; line-height: 1.5; }

.drop-zone {
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  gap: 8px; padding: 40px 16px;
  border: 2px dashed var(--border); border-radius: 16px;
  cursor: pointer; transition: border-color 0.2s, background 0.2s;
  margin-bottom: 28px;
}
.drop-zone:hover, .drop-zone:active { border-color: var(--accent); background: var(--accent-dim); }
.dz-icon { font-size: 32px; color: var(--accent); }
.dz-text { font-size: 16px; color: var(--text); font-weight: 500; }
.dz-hint { font-size: 13px; color: var(--text-secondary); }

.material-list { margin-top: 24px; }
.list-title { font-size: 14px; color: var(--text-secondary); font-weight: 500; margin-bottom: 12px; }

.material-item {
  background: var(--surface); border-radius: var(--radius); padding: 14px 16px;
  margin-bottom: 8px; display: flex; align-items: center; justify-content: space-between;
  gap: 12px;
}
.mi-info { flex: 1; min-width: 0; }
.mi-name { font-size: 15px; color: var(--text); font-weight: 500; display: block; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.mi-meta { font-size: 12px; color: var(--text-secondary); margin-top: 3px; display: block; }
.mi-actions { display: flex; align-items: center; gap: 10px; flex-shrink: 0; }
.mi-btn {
  padding: 6px 12px; border: 1px solid var(--accent); border-radius: 6px;
  background: transparent; color: var(--accent); font-size: 12px; font-family: var(--body);
  cursor: pointer;
}
.mi-date { font-size: 11px; color: var(--text-secondary); font-family: var(--mono); }
.mi-delete {
  background: none; border: none; color: var(--text-secondary); font-size: 20px; cursor: pointer;
  padding: 0 4px; line-height: 1;
}

.empty-hint {
  text-align: center; padding: 48px; color: var(--text-secondary);
}
.empty-icon { font-size: 40px; display: block; margin-bottom: 12px; }
.empty-hint p { font-size: 15px; }
</style>
