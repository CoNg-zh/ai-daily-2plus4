#!/usr/bin/env python3
"""
4 个订阅日报抓取脚本
- 爱窝啦 AI 日报
- AI 趋势
- Inference Brief
- 智语观潮
"""

import argparse
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# 配置数据源
SOURCES = [
    {
        'name': '爱窝啦 AI 日报',
        'url': 'https://news.aivora.cn/',
        'type': 'html',
        'selector': '.news-item'  # 需要根据实际页面结构调整
    },
    {
        'name': 'AI 趋势',
        'url': 'https://www.aitrend.us/',
        'type': 'html',
        'selector': '.article-item'
    },
    {
        'name': '智语观潮',
        'url': 'https://ai.daily.yangsir.net/',
        'type': 'html',
        'selector': '.daily-item'
    },
    {
        'name': 'Inference Brief',
        'url': 'https://inferencebrief.ai/',
        'type': 'html',
        'selector': '.brief-item'
    },
]

def fetch_html(url, selector):
    """抓取 HTML 页面"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        items = []
        
        # 查找文章列表
        article_elements = soup.select(selector) if selector else soup.find_all('article')
        
        for elem in article_elements[:10]:  # 每个源最多 10 条
            try:
                title_elem = elem.find(['h2', 'h3', 'a'], class_=lambda x: x and ('title' in x.lower() or 'headline' in x.lower()))
                link_elem = elem.find('a', href=True)
                summary_elem = elem.find(['p', 'div'], class_=lambda x: x and ('summary' in x.lower() or 'excerpt' in x.lower()))
                
                title = title_elem.get_text(strip=True) if title_elem else '无标题'
                link = link_elem['href'] if link_elem else url
                summary = summary_elem.get_text(strip=True)[:200] if summary_elem else ''
                
                items.append({
                    'title': title,
                    'link': link if link.startswith('http') else f"https://{link}",
                    'summary': summary,
                    'source': '订阅源'
                })
            except Exception:
                continue
        
        return items
    except Exception as e:
        print(f"⚠️ 抓取失败 {url}: {e}")
        return []

def generate_report(all_items, output_dir):
    """生成各订阅源日报"""
    os.makedirs(output_dir, exist_ok=True)
    
    # 如果没有任何内容，创建占位文件
    if not all_items:
        for source in SOURCES:
            safe_name = source['name'].replace(' ', '_').replace('/', '_')
            path = os.path.join(output_dir, f'{safe_name}.md')
            with open(path, 'w', encoding='utf-8') as f:
                f.write(f"# {source['name']} - {datetime.now().strftime('%Y-%m-%d')}\n\n暂无内容\n")
        return
    
    # 按来源分组
    by_source = {}
    for item in all_items:
        source = item.get('source', 'Unknown')
        if source not in by_source:
            by_source[source] = []
        by_source[source].append(item)
    
    # 生成总文件
    total_path = os.path.join(output_dir, 'all_subscribes.md')
    with open(total_path, 'w', encoding='utf-8') as f:
        f.write(f"# 4 个订阅日报 - {datetime.now().strftime('%Y-%m-%d')}\n\n")
        f.write(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        
        for source, items in by_source.items():
            f.write(f"\n## 📰 {source}\n\n")
            f.write(f"**共 {len(items)} 条**\n\n")
            f.write("---\n\n")
            
            for i, item in enumerate(items[:5], 1):  # 每个源最多展示 5 条
                f.write(f"### {i}. {item['title']}\n\n")
                if item.get('summary'):
                    f.write(f"{item['summary']}\n\n")
                f.write(f"👉 [阅读原文]({item['link']})\n\n")
    
    print(f"✅ 订阅日报已生成：{total_path}")
    
    # 生成各源单独文件
    for source, items in by_source.items():
        safe_name = source.replace(' ', '_').replace('/', '_')
        path = os.path.join(output_dir, f'{safe_name}.md')
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(f"# {source} - {datetime.now().strftime('%Y-%m-%d')}\n\n")
            
            for i, item in enumerate(items, 1):
                f.write(f"### {i}. {item['title']}\n")
                f.write(f"👉 [阅读原文]({item['link']})\n\n")
        
        print(f"   ✅ {source}: {path}")

def main():
    parser = argparse.ArgumentParser(description='4 个订阅日报抓取')
    parser.add_argument('--output', type=str, default='output/subscribes/', help='输出目录')
    
    args = parser.parse_args()
    
    print(f"🚀 开始抓取 4 个订阅日报...")
    
    all_items = []
    
    # 抓取各订阅源
    for source in SOURCES:
        print(f"📡 抓取 {source['name']}...")
        items = fetch_html(source['url'], source.get('selector'))
        print(f"   ✅ 获取 {len(items)} 条")
        all_items.extend(items)
    
    # 生成日报
    generate_report(all_items, args.output)
    
    print(f"\n✅ 订阅日报抓取完成！共 {len(all_items)} 条")

if __name__ == '__main__':
    main()
