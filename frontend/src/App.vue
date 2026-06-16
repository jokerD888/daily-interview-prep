<template>
  <div class="app-shell">
    <div class="theme-toggle" v-if="showTabbar" @click="toggle">
      <span v-if="theme === 'dark'">&#9788;</span>
      <span v-else>&#9790;</span>
    </div>
    <router-view v-slot="{ Component }">
      <transition name="page" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>
    <van-tabbar v-if="showTabbar" v-model="active" route :border="false" safe-area-inset-bottom>
      <van-tabbar-item to="/">
        <template #icon="props">
          <span class="tab-icon" :class="{ active: props.active }">&#8962;</span>
        </template>
        首页
      </van-tabbar-item>
      <van-tabbar-item to="/upload">
        <template #icon="props">
          <span class="tab-icon" :class="{ active: props.active }">&#8593;</span>
        </template>
        上传
      </van-tabbar-item>
      <van-tabbar-item to="/review">
        <template #icon="props">
          <span class="tab-icon" :class="{ active: props.active }">&#9635;</span>
        </template>
        复习
      </van-tabbar-item>
      <van-tabbar-item to="/stats">
        <template #icon="props">
          <span class="tab-icon" :class="{ active: props.active }">&#9689;</span>
        </template>
        统计
      </van-tabbar-item>
    </van-tabbar>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useTheme } from './composables/useTheme'

const route = useRoute()
const active = ref(0)
const showTabbar = computed(() => route.path !== '/login')
const { theme, toggle } = useTheme()
</script>

<style>
.app-shell { min-height: 100dvh; }

.theme-toggle {
  position: fixed; top: 12px; right: 12px; z-index: 100;
  width: 36px; height: 36px; border-radius: 50%;
  background: var(--surface); border: 1px solid var(--border);
  display: flex; align-items: center; justify-content: center;
  font-size: 18px; cursor: pointer; transition: background 0.2s;
}
.theme-toggle:active { background: var(--surface-hover); }

.tab-icon { font-size: 20px; transition: color 0.2s; color: var(--text-secondary); }
.tab-icon.active { color: var(--accent); }

.page-enter-active, .page-leave-active { transition: opacity 0.15s ease; }
.page-enter-from, .page-leave-to { opacity: 0; }
</style>
