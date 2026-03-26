# AI Daily 推送定时任务

## 配置 Cron 任务

在 OpenClaw 中添加定时任务，每 30 分钟检查一次新日报：

```bash
# 编辑 OpenClaw cron 配置
openclaw cron create --name "AI Daily Push" --schedule "*/30 * * * *" --command "python3 /home/ubuntu/.openclaw/workspace/github-actions-2plus4/scripts/check_and_push.py"
```

或者在 OpenClaw 配置文件中添加：

```json
{
  "cron": {
    "ai-daily-push": {
      "name": "AI Daily Push",
      "schedule": "*/30 * * * *",
      "command": "python3 /home/ubuntu/.openclaw/workspace/github-actions-2plus4/scripts/check_and_push.py",
      "enabled": true
    }
  }
}
```

## 测试运行

```bash
cd /home/ubuntu/.openclaw/workspace/github-actions-2plus4
python3 scripts/check_and_push.py
```

## 预期行为

1. GitHub Actions 每天 09:00 运行，生成日报保存到 `output/full/daily-YYYY-MM-DD.md`
2. OpenClaw 每 30 分钟检查一次
3. 发现新日报后，解析内容并发送到飞书
4. 标记已推送（创建 `.sent` 文件），避免重复推送

## 监控

查看定时任务日志：

```bash
openclaw cron logs ai-daily-push
```
