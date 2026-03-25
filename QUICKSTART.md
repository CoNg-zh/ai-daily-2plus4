# ⚡ 5 分钟快速部署

## 前提条件

- ✅ GitHub 账号
- ✅ 飞书账号
- ✅ 通义千问 API Key（DashScope）

## 步骤总览

```
1. 创建 GitHub 仓库    (2 分钟)
2. 配置 3 个 Secrets     (1 分钟)
3. 获取通义千问 API Key  (1 分钟)
4. 获取飞书 Webhook     (1 分钟)
5. 手动触发测试        (2 分钟)
────────────────────────────
总计：~7 分钟
```

## 详细步骤

### 1️⃣ 创建 GitHub 仓库

```bash
# 访问 https://github.com/new
# 仓库名：ai-daily-2plus4
# 可见性：Public（免费 2000 分钟/月）
# 初始化：勾选 "Add a README file"
```

然后上传项目文件：

```bash
cd /home/ubuntu/.openclaw/workspace/github-actions-2plus4

git init
git add .
git commit -m "Initial commit: AI Daily 2+4 Workflow"

git remote add origin https://github.com/YOUR_USERNAME/ai-daily-2plus4.git
git branch -M main
git push -u origin main
```

### 2️⃣ 配置 Secrets

进入 `Settings → Secrets and variables → Actions → New repository secret`

添加 3 个 Secrets：

| Secret Name | Value 示例 | 说明 |
|-------------|-----------|------|
| `DASHSCOPE_API_KEY` | `sk-xxxxxxxxxx` | 通义千问 API Key |
| `FEISHU_WEBHOOK` | `https://open.feishu.cn/...` | 飞书机器人 Webhook |
| `INTERESTS` | `AI,Agent,OpenClaw，大模型` | 兴趣关键词 |

### 3️⃣ 获取通义千问 API Key

1. 访问 https://dashscope.console.aliyun.com/
2. 登录阿里云账号
3. **API Key 管理** → **创建新 Key**
4. 复制 Key
5. 粘贴到 GitHub Secrets 的 `DASHSCOPE_API_KEY`

### 4️⃣ 获取飞书 Webhook

1. 打开飞书 → 创建群聊（或选择现有群）
2. 群设置 → **添加机器人**
3. 选择 **自定义机器人**
4. 复制 **Webhook 地址**
5. 粘贴到 GitHub Secrets 的 `FEISHU_WEBHOOK`

### 5️⃣ 启用 Actions

1. **Actions** 标签
2. 点击 **I understand my workflows, go ahead and enable them**

### 6️⃣ 手动触发测试

1. **Actions** → **Daily 2+4 Workflow**
2. **Run workflow**
3. 选择分支（main）
4. **Run workflow**
5. 等待 3-5 分钟
6. 查看飞书是否收到推送

---

## ✅ 验证成功

收到飞书消息类似：

```
🤖 AI 日报 - 2026-03-26

🔥 重磅新闻
1. OpenAI 发布 GPT-5.4 ⭐⭐⭐⭐⭐
   GPT-5.4 在推理能力上取得重大突破...
   📁 TrendRadar
   👉 [阅读原文](...)

⚡ 技术更新
1. Anthropic 更新 Claude...
   ...

📊 今日共整理 15 条资讯
数据来源：TrendRadar, AI Daily Digest, 4 个订阅日报

[📚 查看完整归档]
```

---

## 🎉 完成！

现在：
- ✅ 每天 9:30 自动推送
- ✅ 无需管理服务器
- ✅ 2+4 数据源整合
- ✅ JARVIS 智能去重评分

---

## 📞 遇到问题？

查看项目根目录的 README.md 和 DEPLOY.md 详细指南。
