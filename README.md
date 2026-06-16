# 每日八股 — 科学记忆面试知识

AI 驱动的八股文记忆学习工具。上传 PDF/Markdown 资料，AI 自动拆解为正反面记忆卡片，按艾宾浩斯遗忘曲线 + 主动回忆模式每日推送，科学提升学习效率。

## 特性

- 🤖 **AI 卡片生成** — 上传八股资料，DeepSeek V4 Flash 自动拆解为 Q&A 记忆卡片，按面试频率评分
- 🧠 **艾宾浩斯调度** — 基于 [1, 2, 4, 7, 15, 30] 天间隔序列，主动回忆 + 间隔重复
- 📱 **PWA 手机端** — 添加到主屏幕，全屏体验，离线可用
- 🌓 **明暗主题** — 深色/浅色一键切换，持久化记忆
- 📊 **学习统计** — 掌握率环形图、连续打卡天数、卡片状态分布
- 🎯 **种子数据** — 内置 Java 基础、Spring、操作系统各 20 张高频卡片

## 技术栈

| 层 | 技术 |
|---|------|
| 后端 | Python FastAPI + SQLAlchemy + SQLite |
| 前端 | Vue 3 + Vite + Vant UI (PWA) |
| AI | DeepSeek V4 Flash API |
| 部署 | Docker Compose + Nginx |

## 快速开始

### 本地开发

```bash
# 后端
cd backend
pip install -r requirements.txt
python init_db.py
uvicorn app.main:app --reload --port 8000

# 前端
cd frontend
npm install
npm run dev
```

访问 `http://localhost:5173`。

### Docker 部署

```bash
# 1. 配置环境变量
cp backend/.env.production backend/.env
vim backend/.env  # 填 DEEPSEEK_API_KEY 和 JWT_SECRET

# 2. 构建前端
cd frontend && npm install && npm run build && cd ..

# 3. 启动
docker compose up -d

# 4. 安装种子卡片
curl -X POST http://localhost/api/seed/install
```

### 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `DEEPSEEK_API_KEY` | DeepSeek API 密钥 | - |
| `DEEPSEEK_BASE_URL` | API 地址 | `https://api.deepseek.com` |
| `AI_MODEL` | 模型名称 | `deepseek-v4-flash` |
| `JWT_SECRET` | JWT 签名密钥 | 必改 |
| `DAILY_NEW_CARDS` | 每日新卡数 | 10 |
| `DAILY_REVIEW_CARDS` | 每日复习卡数 | 20 |

## 项目结构

```
daily-interview-prep/
├── backend/
│   ├── app/
│   │   ├── api/          # 路由层 (auth, materials, cards, reviews, push, seed)
│   │   ├── core/         # 配置、数据库、认证
│   │   ├── models/       # User, Material, Card, CardProgress, ReviewLog
│   │   ├── schemas/      # Pydantic 请求/响应模型
│   │   └── services/     # PDF解析、AI卡片生成、艾宾浩斯调度
│   ├── tests/
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── views/        # Login, Home, Upload, Review, Stats
│   │   └── composables/  # useTheme
│   └── vite.config.js
├── nginx.conf
└── docker-compose.yml
```
