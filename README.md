# AI Daily 2+4 Workflow

基于 GitHub Actions 的 AI 日报整合系统，每天北京时间 9:30 自动推送飞书。

## 信息来源

### 2 个开源项目
- **TrendRadar** - 多平台热点聚合（GitHub Actions 运行）
- **AI Daily Digest** - 92 个顶级技术博客（GitHub Actions 运行）

### 4 个订阅日报
- **爱窝啦 AI 日报** - news.aivora.cn
- **AI 趋势** - www.aitrend.us
- **Inference Brief** - inferencebrief.ai
- **智语观潮** - ai.daily.yangsir.net

### JARVIS 整合
- **频率**: 每天 9:30 AM
- **输出**: 飞书详细版推送
- **API**: 通义千问（Qwen）

## 部署步骤

### 1. Fork 本仓库

```bash
# 访问 https://github.com/new
# 仓库名：ai-daily-2plus4
# 可见性：Public
```

### 2. 配置 Secrets

进入 `Settings → Secrets and variables → Actions`

| Secret Name | Value | 说明 |
|-------------|-------|------|
| `DASHSCOPE_API_KEY` | `sk-xxxxx` | 通义千问 API Key |
| `FEISHU_WEBHOOK` | `https://open.feishu.cn/...` | 飞书机器人 Webhook |
| `INTERESTS` | `AI,Agent,OpenClaw，大模型` | 兴趣关键词 |

### 3. 启用 Actions

```bash
# Actions 标签 → 确认启用工作流
```

### 4. 手动触发测试

```bash
# Actions → Daily Workflow → Run workflow
```

## 推送时间

| 任务 | UTC 时间 | 北京时间 |
|------|---------|----------|
| TrendRadar 抓取 | 00:30 | 08:30 |
| AI Daily Digest 抓取 | 00:45 | 08:45 |
| 4 个订阅抓取 | 01:00 | 09:00 |
| **JARVIS 整合推送** | **01:30** | **09:30** |

## 成本

| 项目 | 用量 | 费用 |
|------|------|------|
| GitHub Actions | ~600 分钟/月 | $0 (免费 2000 分钟) |
| 通义千问 API | ~3000 次/月 | ~¥50-100/月 |
| **总计** | - | **~¥50-100/月** |

## 许可证

MIT
