#!/usr/bin/env python3
"""
OpenClaw 心跳检查 - 检查 GitHub 新日报并通过 message 工具推送到飞书
"""

import os
import subprocess
from datetime import datetime

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
    
    # 提取标题和链接
    lines = content.split('\n')
    message = "🤖 **AI Daily 2+4** - " + datetime.now().strftime('%Y-%m-%d') + "\n\n"
    
    # 提取各分类内容
    current_section = None
    for line in lines:
        if line.startswith('## '):
            current_section = line.replace('## ', '').strip()
            if current_section.startswith('🔥') or current_section.startswith('⚡') or current_section.startswith('💼') or current_section.startswith('📄'):
                message += f"\n{current_section}\n"
        elif line.startswith('1. **') and current_section:
            # 提取第一条新闻
            title = line.split('**')[1] if '**' in line else line
            message += f"  {line}\n"
            break
    
    message += "\n📊 查看完整日报：https://github.com/CoNg-zh/ai-daily-2plus4/tree/main/output/full"
    
    return message

def send_to_feishu(message):
    """通过 OpenClaw message 工具发送到飞书"""
    print(f"📤 准备发送飞书消息...")
    print(f"消息内容：{message[:200]}...")
    
    # 调用 message 工具，使用 main 账号
    try:
        result = subprocess.run(
            ['openclaw', 'message', 'send', '--channel', 'feishu', '--account', 'main', '--target', 'user:ou_9c5ba4ecd1c6fc7fe89dfb99caad65cf', '-m', message],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print("✅ 飞书推送成功！")
            return True
        else:
            print(f"❌ 飞书推送失败：{result.stderr}")
            return False
    except Exception as e:
        print(f"❌ 推送异常：{e}")
        return False

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
        print("✅ 推送完成！")
    else:
        print("❌ 推送失败")

if __name__ == '__main__':
    main()
