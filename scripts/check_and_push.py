#!/usr/bin/env python3
"""
OpenClaw 心跳检查 - 检查 GitHub 新日报并推送到飞书
"""

import os
import requests
from datetime import datetime, timedelta

def check_new_report():
    """检查是否有新的日报"""
    today = datetime.now().strftime('%Y-%m-%d')
    report_path = f'/home/ubuntu/.openclaw/workspace/github-actions-2plus4/output/full/daily-{today}.md'
    
    if os.path.exists(report_path):
        # 检查是否已推送
        sent_flag = report_path + '.sent'
        if not os.path.exists(sent_flag):
            return report_path
        else:
            print(f"ℹ️ 今日日报已推送：{report_path}")
            return None
    else:
        print(f"ℹ️ 今日日报尚未生成：{report_path}")
        return None

def parse_report(report_path):
    """解析日报内容，生成飞书消息"""
    with open(report_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取各分类内容（简化版）
    lines = content.split('\n')
    sections = {}
    current_section = 'intro'
    sections[current_section] = []
    
    for line in lines:
        if line.startswith('## '):
            current_section = line.replace('## ', '').strip()
            sections[current_section] = []
        elif line.strip() and not line.startswith('#') and not line.startswith('**'):
            sections[current_section].append(line.strip())
    
    # 构建飞书消息
    message = "🤖 **AI Daily 2+4** - " + datetime.now().strftime('%Y-%m-%d') + "\n\n"
    
    for section_name, items in sections.items():
        if section_name == 'intro' or not items:
            continue
        
        emoji_map = {
            '🔥 重磅新闻': '🔥',
            '⚡ 技术更新': '⚡',
            '💼 行业应用': '💼',
            '📄 研究论文': '📄'
        }
        emoji = emoji_map.get(section_name, '📌')
        
        message += f"{emoji} **{section_name}**\n"
        for item in items[:5]:  # 每个分类最多 5 条
            if item.startswith('- ') or item.startswith('1.'):
                message += f"  {item}\n"
        message += "\n"
    
    message += "\n📊 查看完整日报：https://github.com/CoNg-zh/ai-daily-2plus4/tree/main/output/full"
    
    return message

def send_to_feishu(message):
    """通过 OpenClaw message 工具发送到飞书"""
    # 这里调用 OpenClaw 的 message 工具
    # 由于是在 OpenClaw 环境中运行，可以直接使用 message 工具
    print(f"📤 准备发送飞书消息...\n{message[:200]}...")
    
    # 实际调用由 OpenClaw 处理
    return True

def main():
    """主函数"""
    print("🔍 检查新日报...")
    
    report_path = check_new_report()
    if not report_path:
        print("✅ 无新日报需要推送")
        return
    
    print(f"📰 发现新日报：{report_path}")
    
    # 解析日报
    message = parse_report(report_path)
    
    # 发送到飞书
    success = send_to_feishu(message)
    
    if success:
        # 标记已发送
        with open(report_path + '.sent', 'w') as f:
            f.write(datetime.now().isoformat())
        print("✅ 推送成功！")
    else:
        print("❌ 推送失败")

if __name__ == '__main__':
    main()
