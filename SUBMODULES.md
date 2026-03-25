# 子模块配置

## AI Daily Digest

```bash
cd /home/ubuntu/.openclaw/workspace/github-actions-2plus4
git submodule add https://github.com/zhalice2011/ai-daily.git ai-daily-digest
```

## 或者手动克隆

```bash
cd /home/ubuntu/.openclaw/workspace/github-actions-2plus4
git clone https://github.com/zhalice2011/ai-daily.git ai-daily-digest
```

## 提交子模块

```bash
git add .gitmodules ai-daily-digest
git commit -m "Add AI Daily Digest submodule"
git push
```
