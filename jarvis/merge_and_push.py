#!/usr/bin/env python3
"""
JARVIS - 主 Agent 整合脚本
合并 2+4 数据源，生成详细版飞书推送
"""

import os
import json
import requests
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

def parse_markdown_items(content, max_items=10):
    """解析 Markdown 内容，提取条目"""
    items = []
    lines = content.split('\n')
    
    current_item = {}
    for line in lines:
        line = line.strip()
        
        if line.startswith('### ') and current_item:
            items.append(current_item)
            if len(items) >= max_items:
                break
            current_item = {'title': line[4:]}
        elif line.startswith('**来源**') and current_item:
            current_item['source'] = line.replace('**来源**:', '').strip()
        elif line.startswith('👉 [阅读原文]') and current_item:
            import re
            match = re.search(r'\((https?://[^\)]+)\)', line)
            if match:
                current_item['link'] = match.group(1)
        elif line and not line.startswith('**') and not line.startswith('---') and current_item:
            if 'summary' not in current_item:
                current_item['summary'] = line
            else:
                current_item['summary'] += ' ' + line[:100]
    
    if current_item and 'title' in current_item:
        items.append(current_item)
    
    return items

def jarvis_merge(all_contents, interests=None):
    """
    JARVIS 智能整合
    使用通义千问 API 进行内容去重、评分、排序
    """
    
    # 构建提示词
    prompt = f"""你是一名专业的 AI 资讯编辑 JARVIS。

请整合以下多个来源的 AI 新闻，生成一份详细版日报。

## 要求
1. 去重：合并相似内容
2. 评分：按重要性打分（1-5 星）
3. 分类：分为"重磅新闻"、"技术更新"、"行业应用"、"研究论文"
4. 精选：每个分类选 3-5 条最重要的
5. 格式：每条包含标题、来源、一句话摘要、链接

## 用户兴趣
{interests or 'AI, Agent, 大模型，OpenClaw'}

## 数据来源

{all_contents[:8000]}  # 限制长度

## 输出格式

请按以下 JSON 格式输出：
{{
  "date": "2026-03-26",
  "categories": {{
    "重磅新闻": [
      {{
        "title": "标题",
        "source": "来源",
        "summary": "一句话摘要（50 字以内）",
        "link": "链接",
        "rating": 5
      }}
    ],
    "技术更新": [],
    "行业应用": [],
    "研究论文": []
  }},
  "total_items": 15
}}

只输出 JSON，不要其他内容。"""

    try:
        # 调用通义千问 API
        response = Generation.call(
            model='qwen-max',
            prompt=prompt,
            api_key=os.environ.get('DASHSCOPE_API_KEY')
        )
        
        if response.status_code == 200:
            result = response.output.text
            # 提取 JSON
            import re
            json_match = re.search(r'\{.*\}', result, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        else:
            print(f"⚠️ API 调用失败：{response.code} - {response.message}")
            
    except Exception as e:
        print(f"⚠️ JARVIS 整合异常：{e}")
    
    # Fallback: 简单合并
    return fallback_merge(all_contents)

def fallback_merge(all_contents):
    """Fallback: 简单合并（API 失败时使用）"""
    items = []
    
    # 简单解析所有条目
    for source_name, content in all_contents.items():
        parsed = parse_markdown_items(content, max_items=5)
        for item in parsed:
            item['source'] = source_name
            items.append(item)
    
    # 构建简单报告
    return {
        "date": datetime.now().strftime('%Y-%m-%d'),
        "categories": {
            "精选新闻": items[:10],
            "技术更新": items[10:15],
            "行业应用": items[15:20],
            "研究论文": items[20:25]
        },
        "total_items": len(items)
    }

def create_feishu_card(report):
    """创建飞书详细版卡片"""
    date = report.get('date', datetime.now().strftime('%Y-%m-%d'))
    
    card = {
        "msg_type": "interactive",
        "card": {
            "config": {
                "wide_screen_mode": True
            },
            "header": {
                "template": "blue",
                "title": {
                    "tag": "plain_text",
                    "content": f"🤖 AI 日报 - {date}"
                }
            },
            "elements": []
        }
    }
    
    categories = report.get('categories', {})
    
    # 添加各分类
    emoji_map = {
        '重磅新闻': '🔥',
        '技术更新': '⚡',
        '行业应用': '💼',
        '研究论文': '📄',
        '精选新闻': '⭐'
    }
    
    for category_name, items in categories.items():
        if not items:
            continue
        
        emoji = emoji_map.get(category_name, '📌')
        
        # 分类标题
        card["card"]["elements"].append({
            "tag": "div",
            "text": {
                "tag": "markdown",
                "content": f"\n**{emoji} {category_name}**\n"
            }
        })
        
        # 添加条目
        for i, item in enumerate(items[:5], 1):  # 每个分类最多 5 条
            title = item.get('title', '无标题')
            source = item.get('source', '')
            summary = item.get('summary', '')[:80]
            link = item.get('link', '#')
            rating = item.get('rating', 0)
            
            stars = '⭐' * rating if rating else ''
            
            content = f"**{i}. {title}** {stars}\n"
            if summary:
                content += f"_{summary}_\n"
            if source:
                content += f"📁 {source}\n"
            content += f"👉 [阅读原文]({link})\n"
            
            card["card"]["elements"].append({
                "tag": "div",
                "text": {
                    "tag": "markdown",
                    "content": content
                }
            })
        
        # 分隔线
        card["card"]["elements"].append({"tag": "hr"})
    
    # 底部统计
    total = report.get('total_items', 0)
    card["card"]["elements"].append({
        "tag": "div",
        "text": {
            "tag": "markdown",
            "content": f"\n📊 **今日共整理 {total} 条资讯**\n数据来源：TrendRadar, AI Daily Digest, 4 个订阅日报\n"
        }
    })
    
    # 操作按钮
    card["card"]["elements"].append({
        "tag": "action",
        "actions": [
            {
                "tag": "button",
                "text": {
                    "tag": "plain_text",
                    "content": "📚 查看完整归档"
                },
                "url": "https://github.com/your-username/ai-daily-2plus4",
                "type": "primary"
            }
        ]
    })
    
    return card

def push_to_feishu(webhook, card):
    """推送到飞书"""
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(webhook, json=card, headers=headers, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        if result.get('StatusCode') == 0 or result.get('code') == 0:
            print("✅ 飞书推送成功")
            return True
        else:
            print(f"❌ 飞书推送失败：{result}")
            return False
            
    except Exception as e:
        print(f"❌ 推送异常：{e}")
        return False

def main():
    """主函数"""
    print("🤖 JARVIS 开始整合...")
    
    # 读取所有数据源
    sources = {
        'TrendRadar': read_file('output/trend_radar.md'),
        'AI Daily Digest': read_file('output/ai_daily_digest.md'),
        '爱窝啦': read_file('output/subscribes/爱窝啦 AI 日报.md'),
        'AI 趋势': read_file('output/subscribes/AI 趋势.md'),
        '智语观潮': read_file('output/subscribes/智语观潮.md'),
        'Inference Brief': read_file('output/subscribes/Inference Brief.md')
    }
    
    # 过滤空内容
    sources = {k: v for k, v in sources.items() if v}
    
    print(f"📚 读取到 {len(sources)} 个数据源")
    
    # 获取兴趣配置
    interests = os.environ.get('INTERESTS', 'AI,Agent,OpenClaw，大模型')
    
    # JARVIS 整合
    report = jarvis_merge(sources, interests)
    
    print(f"✅ 整合完成，共 {report.get('total_items', 0)} 条")
    
    # 创建飞书卡片
    card = create_feishu_card(report)
    
    # 推送到飞书
    webhook = os.environ.get('FEISHU_WEBHOOK')
    if not webhook:
        print("❌ 未配置 FEISHU_WEBHOOK")
        return
    
    success = push_to_feishu(webhook, card)
    
    # 保存完整报告
    full_report = f"# AI Daily 2+4 - {datetime.now().strftime('%Y-%m-%d')}\n\n"
    full_report += f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
    full_report += f"**数据来源**: {', '.join(sources.keys())}\n\n"
    full_report += f"**总计**: {report.get('total_items', 0)} 条\n\n"
    full_report += "---\n\n"
    
    for category, items in report.get('categories', {}).items():
        full_report += f"\n## {category}\n\n"
        for item in items:
            full_report += f"### {item.get('title', '无标题')}\n"
            full_report += f"📁 {item.get('source', '')}\n"
            full_report += f"👉 {item.get('link', '#')}\n\n"
    
    os.makedirs('output/full', exist_ok=True)
    with open(f"output/full/daily-{datetime.now().strftime('%Y-%m-%d')}.md", 'w', encoding='utf-8') as f:
        f.write(full_report)
    
    print(f"✅ 完整报告已保存：output/full/daily-{datetime.now().strftime('%Y-%m-%d')}.md")
    
    if success:
        print("\n🎉 JARVIS 整合完成！飞书推送成功！")
    else:
        print("\n⚠️ JARVIS 整合完成，但飞书推送失败")

if __name__ == '__main__':
    main()
