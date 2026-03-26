#!/usr/bin/env python3
"""
JARVIS - 完整版整合脚本（所有数据源：2+4）
"""

import os
import json
import dashscope
from datetime import datetime
from dashscope import Generation

def read_file(path):
    """读取文件内容"""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"⚠️ 文件不存在：{path}")
        return ""

def jarvis_merge(all_contents, interests=None):
    """JARVIS 智能整合 - 每个数据源输出 10 条精选"""
    
    prompt = f"""你是一名专业的 AI 资讯编辑 JARVIS。

请整合以下多个来源的 AI 新闻，生成一份详细版日报。

## 要求
1. **每个数据源选 10 条**：TrendRadar 10 条 + AI Daily Digest 10 条 + 订阅源各 10 条
2. 去重：合并相似内容
3. 评分：按重要性打分（1-5 星）
4. 分类：分为"重磅新闻"、"技术更新"、"行业应用"、"研究论文"
5. 格式：Markdown
6. **只提取真实新闻**，忽略测试/配置/系统状态等内容

## 用户兴趣
{interests or 'AI, Agent, 大模型，OpenClaw'}

## 数据来源

{'\n\n'.join(all_contents)[:15000]}

## 输出格式

# AI Daily 2+4 - YYYY-MM-DD

**生成时间**: YYYY-MM-DD HH:MM
**数据来源**: TrendRadar, AI Daily Digest, 智语观潮，AI 趋势，Inference Brief
**总计**: 约 50 条

---

## 🔥 重磅新闻（10 条）

1. **标题** ⭐⭐⭐⭐⭐
   - 来源：来源名
   - 摘要：一句话摘要（50 字以内）
   - 👉 [阅读原文](链接)

...

## ⚡ 技术更新（10 条）

...

## 💼 行业应用（10 条）

...

## 📄 研究论文（10 条）

...

## 📰 订阅源精选（各 10 条）

### 智语观潮（10 条）
1. **标题** - 摘要...

### AI 趋势（10 条）
1. **标题** - 摘要...

### Inference Brief（10 条）
1. **标题** - 摘要...

---

只输出 Markdown 内容。"""

    try:
        response = Generation.call(
            model='qwen-max',
            prompt=prompt,
            api_key=os.environ.get('DASHSCOPE_API_KEY')
        )
        
        if response.status_code == 200:
            return response.output.text
        else:
            print(f"⚠️ API 调用失败：{response.code}")
            
    except Exception as e:
        print(f"⚠️ JARVIS 整合异常：{e}")
    
    # Fallback
    return f"# AI Daily 2+4 - {datetime.now().strftime('%Y-%m-%d')}\n\n整合失败，请检查日志。"

def main():
    """主函数"""
    print("🤖 JARVIS 开始整合...")
    
    # 读取所有数据源
    sources = {
        'TrendRadar': read_file('output/trend_radar.md'),
        'AI Daily Digest': read_file('output/ai_daily_digest.md'),
        '智语观潮': read_file('output/subscribes/智语观潮.md'),
        'AI 趋势': read_file('output/subscribes/AI 趋势.md'),
        'Inference Brief': read_file('output/subscribes/Inference Brief.md'),
    }
    
    # 过滤空内容
    sources = {k: v for k, v in sources.items() if v and len(v) > 50}
    
    print(f"📚 读取到 {len(sources)} 个有效数据源")
    for name, content in sources.items():
        print(f"  - {name}: {len(content)} 字符")
    
    # 获取兴趣配置
    interests = os.environ.get('INTERESTS', 'AI,Agent,OpenClaw，大模型')
    
    # JARVIS 整合
    report = jarvis_merge(list(sources.values()), interests)
    
    # 保存日报
    os.makedirs('output/full', exist_ok=True)
    today = datetime.now().strftime('%Y-%m-%d')
    report_path = f'output/full/daily-{today}.md'
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"✅ 日报已保存：{report_path}")
    print(f"📊 预计输出：~50 条新闻（每个数据源 10 条）")

if __name__ == '__main__':
    main()
