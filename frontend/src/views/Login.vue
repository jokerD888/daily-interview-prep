<template>
  <div class="auth-page">
    <div class="auth-header">
      <div class="brand-mark">&#9672;</div>
      <h1 class="brand-title">每日八股</h1>
      <p class="brand-sub">科学记忆，面试不慌</p>
    </div>

    <div class="tabs-row">
      <button class="tab-btn" :class="{ active: tab === 0 }" @click="tab = 0">登录</button>
      <button class="tab-btn" :class="{ active: tab === 1 }" @click="tab = 1">注册</button>
    </div>

    <form class="auth-form" @submit.prevent="tab === 0 ? handleLogin() : handleRegister()">
      <div class="field">
        <label class="field-label">用户名</label>
        <input v-model="form.username" class="field-input" placeholder="输入用户名" autocomplete="username" />
      </div>
      <div class="field">
        <label class="field-label">密码</label>
        <input v-model="form.password" class="field-input" type="password" placeholder="至少 6 位" autocomplete="current-password" />
      </div>
      <button type="submit" class="submit-btn" :disabled="loading">
        {{ loading ? '...' : tab === 0 ? '登录' : '创建账号' }}
      </button>
    </form>

    <p class="error-msg" v-if="error">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const tab = ref(0)
const error = ref('')
const loading = ref(false)
const form = reactive({ username: '', password: '' })

async function handleLogin() {
  error.value = ''
  loading.value = true
  try {
    const res = await axios.post('/api/auth/login', form)
    localStorage.setItem('token', res.data.access_token)
    router.push('/')
  } catch (e) {
    error.value = e.response?.data?.detail || '登录失败'
  } finally {
    loading.value = false
  }
}

async function handleRegister() {
  error.value = ''
  loading.value = true
  try {
    const res = await axios.post('/api/auth/register', form)
    localStorage.setItem('token', res.data.access_token)
    router.push('/')
  } catch (e) {
    error.value = e.response?.data?.detail || '注册失败'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-page {
  min-height: 100dvh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 32px 24px;
}

.auth-header { text-align: center; margin-bottom: 40px; }
.brand-mark { font-size: 42px; color: var(--accent); margin-bottom: 12px; }
.brand-title { font-family: var(--display); font-size: 32px; font-weight: 700; color: var(--text); letter-spacing: 2px; }
.brand-sub { color: var(--text-secondary); margin-top: 8px; font-size: 15px; }

.tabs-row { display: flex; gap: 0; margin-bottom: 24px; background: var(--surface); border-radius: 10px; padding: 4px; }
.tab-btn {
  flex: 1; padding: 10px 0; border: none; background: transparent;
  color: var(--text-secondary); font-size: 15px; font-family: var(--body); font-weight: 500;
  border-radius: 8px; cursor: pointer; transition: all 0.2s;
}
.tab-btn.active { background: var(--accent); color: var(--accent-text); }

.auth-form { width: 100%; max-width: 320px; }
.field { margin-bottom: 16px; }
.field-label { display: block; font-size: 13px; color: var(--text-secondary); margin-bottom: 6px; font-weight: 500; }
.field-input {
  width: 100%; padding: 12px 16px; border: 1px solid var(--border); border-radius: 10px;
  background: var(--surface); color: var(--text); font-size: 16px; font-family: var(--body);
  outline: none; transition: border-color 0.2s;
}
.field-input:focus { border-color: var(--accent); }
.field-input::placeholder { color: var(--text-secondary); opacity: 0.6; }

.submit-btn {
  width: 100%; padding: 14px; margin-top: 8px; border: none; border-radius: 10px;
  background: var(--accent); color: var(--accent-text); font-size: 16px; font-weight: 600;
  font-family: var(--body); cursor: pointer; transition: opacity 0.2s;
}
.submit-btn:disabled { opacity: 0.6; cursor: default; }

.error-msg { color: var(--danger); font-size: 14px; margin-top: 16px; text-align: center; }
</style>
