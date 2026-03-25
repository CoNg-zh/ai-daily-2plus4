#!/usr/bin/env python3
"""
TrendRadar 简化版抓取脚本
数据源：多平台热点 + RSS
"""

import argparse
import os
import json
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

# 配置数据源
SOURCES = [
    {
        'name': 'Hacker News',
        'type': 'rss',
        'url': 'https://news.ycombinator.com/rss',
        'category': '英文'
    },
    {
        'name': 'GitHub Trending',
        'type': 'api',
        'url': 'https://api.github.com/search/repositories?q=stars:>1000&sort=stars&order=desc',
        'category': '英文'
    },
    {
        'name': 'Reddit - r/MachineLearning',
        'type': 'rss',
        'url': 'https://www.reddit.com/r/MachineLearning/hot/.rss',
        'category': '英文'
    },
    {
        'name': 'Product Hunt',
        'type': 'rss',
        'url': 'https://www.producthunt.com/feed',
        'category': '英文'
    },
]

def fetch_rss(url, limit=20):
    """抓取 RSS 源"""
    try:
        import feedparser
        feed = feedparser.parse(url)
        items = []
        
        for entry in feed.entries[:limit]:
            try:
                items.append({
                    'title': entry.title,
                    'link': entry.link,
                    'published': entry.get('published', ''),
                    'summary': entry.get('summary', '')[:200],
                    'source': feed.feed.get('title', 'Unknown')
                })
            except Exception:
                continue
        
        return items
    except Exception as e:
        print(f"⚠️ RSS 抓取失败 {url}: {e}")
        return []

def fetch_github_trending():
    """抓取 GitHub Trending"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(SOURCES[1]['url'], headers=headers, timeout=30)
        response.raise_for_status()
        
        repos = response.json().get('items', [])[:10]
        items = []
        
        for repo in repos:
            items.append({
                'title': f"[GitHub] {repo['full_name']} - {repo.get('description', 'No description')[:100]}",
                'link': repo['html_url'],
                'published': '',
                'summary': f"⭐ {repo['stargazers_count']} | 🍴 {repo['forks_count']}",
                'source': 'GitHub Trending'
            })
        
        return items
    except Exception as e:
        print(f"⚠️ GitHub 抓取失败：{e}")
        return []

def ai_filter(items, interests=None):
    """AI 智能筛选（关键词匹配 + 评分）"""
    if not interests:
        interests = ['AI', 'Agent', 'LLM', 'GPT', 'Claude', 'OpenAI', '大模型', '智能体']
    
    filtered = []
    for item in items:
        text = (item['title'] + ' ' + item.get('summary', '')).lower()
        score = sum(1 for kw in interests if kw.lower() in text)
        if score > 0:
            item['score'] = score
            filtered.append(item)
    
    # 按评分排序
    filtered.sort(key=lambda x: x['score'], reverse=True)
    return filtered[:15]  # 返回 Top 15

def generate_report(items, output_path):
    """生成日报"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"# TrendRadar - {datetime.now().strftime('%Y-%m-%d')}\n\n")
        f.write(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        f.write(f"**共 {len(items)} 条精选**\n\n")
        f.write("---\n\n")
        
        for i, item in enumerate(items, 1):
            f.write(f"### {i}. {item['title']}\n\n")
            f.write(f"**来源**: {item['source']} | **评分**: ⭐{item.get('score', 0)}\n\n")
            if item.get('summary'):
                f.write(f"{item['summary']}\n\n")
            f.write(f"👉 [阅读原文]({item['link']})\n\n")
            f.write("---\n\n")
    
    print(f"✅ TrendRadar 已生成：{output_path}")

def main():
    parser = argparse.ArgumentParser(description='TrendRadar 简化版')
    parser.add_argument('--output', type=str, default='output/trend_radar.md', help='输出文件路径')
    parser.add_argument('--interests', type=str, default='', help='兴趣关键词')
    
    args = parser.parse_args()
    interests = [i.strip() for i in args.interests.split(',')] if args.interests else None
    
    print(f"🚀 TrendRadar 开始抓取...")
    
    all_items = []
    
    # 抓取各数据源
    for source in SOURCES:
        print(f"📡 抓取 {source['name']}...")
        
        if source['type'] == 'rss':
            items = fetch_rss(source['url'])
        elif source['type'] == 'api':
            items = fetch_github_trending()
        else:
            items = []
        
        print(f"   ✅ 获取 {len(items)} 条")
        all_items.extend(items)
    
    # AI 筛选
    print(f"🤖 AI 筛选...")
    filtered = ai_filter(all_items, interests)
    print(f"   ✅ 筛选后 {len(filtered)} 条")
    
    # 生成日报
    generate_report(filtered, args.output)
    
    print(f"\n✅ TrendRadar 完成！")

if __name__ == '__main__':
    main()
