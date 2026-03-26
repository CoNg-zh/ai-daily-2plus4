#!/usr/bin/env python3
"""
4 个订阅日报 - RSS/邮件订阅方式
不爬虫，只解析订阅内容
"""

import os
from datetime import datetime

# 配置数据源（RSS + 邮件订阅）
SOURCES = [
    {
        'name': '智语观潮',
        'type': 'rss',
        'rss_url': 'https://ai.daily.yangsir.net/rss.xml',  # ✅ 已验证
    },
    {
        'name': 'AI 趋势',
        'type': 'rss',
        'rss_url': 'https://www.aitrend.us/feed.json',  # ✅ 已验证
    },
    {
        'name': 'Inference Brief',
        'type': 'rss',
        'rss_url': 'https://inferencebrief.ai/feed.json',  # ✅ 已验证
    },
    # 爱窝啦 AI 日报：邮件订阅（需要配置邮箱）
    # {
    #     'name': '爱窝啦 AI 日报',
    #     'type': 'email',
    #     'email_subject': '爱窝啦 AI 日报',
    #     'email_account': 'your-email@gmail.com',  # 待配置
    # }
]

def fetch_rss(rss_url):
    """解析 RSS feed"""
    try:
        import feedparser
        feed = feedparser.parse(rss_url)
        items = []
        for entry in feed.entries[:10]:
            items.append({
                'title': entry.title,
                'link': entry.link,
                'summary': entry.get('summary', '')[:200],
                'published': entry.get('published', ''),
                'source': feed.feed.get('title', 'RSS')
            })
        return items
    except Exception as e:
        print(f"⚠️ RSS 解析失败 {rss_url}: {e}")
        return []

def fetch_email(subject_keyword):
    """从邮件获取订阅内容（需要配置 IMAP）"""
    # TODO: 配置邮件账号后实现
    print(f"ℹ️ 邮件订阅待配置：{subject_keyword}")
    return []

def main():
    """主函数"""
    print("📬 检查订阅源...")
    
    output_dir = os.environ.get('OUTPUT_DIR', 'output/subscribes')
    os.makedirs(output_dir, exist_ok=True)
    
    for source in SOURCES:
        print(f"\n📰 {source['name']}...")
        
        if source['type'] == 'rss':
            items = fetch_rss(source.get('rss_url', ''))
        elif source['type'] == 'email':
            items = fetch_email(source.get('email_subject', ''))
        else:
            items = []
        
        # 保存结果
        safe_name = source['name'].replace(' ', '_').replace('/', '_')
        path = os.path.join(output_dir, f'{safe_name}.md')
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(f"# {source['name']} - {datetime.now().strftime('%Y-%m-%d')}\n\n")
            
            if items:
                for i, item in enumerate(items[:5], 1):
                    f.write(f"### {i}. {item['title']}\n")
                    f.write(f"{item.get('summary', '')}\n")
                    f.write(f"👉 [阅读原文]({item['link']})\n\n")
            else:
                f.write("暂无内容（RSS 不可用或邮件待配置）\n")
        
        print(f"   ✅ 保存：{path} ({len(items)} 条)")

if __name__ == '__main__':
    main()
