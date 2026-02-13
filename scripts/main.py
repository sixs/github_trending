#!/usr/bin/env python3
"""
GitHub Trending 日报生成器
"""

import sys
import os
from datetime import datetime
from zoneinfo import ZoneInfo

# 在程序开始时获取统一的北京时间，避免跨日期和时区不一致问题
CURRENT_DATE = datetime.now(ZoneInfo("Asia/Shanghai"))

sys.path.append(os.path.join(os.path.dirname(__file__)))

from github_trending import fetch_trending
from page_generator import build_refined_html, save_html_file, generate_pages_index
from wechat_publisher import publish_to_wechat
from feishu_publisher import publish_to_feishu

def main():
    """主函数"""
    # 收集数据
    print("正在收集GitHub Trending数据...")
    d, w, m = fetch_trending('daily'), fetch_trending('weekly'), fetch_trending('monthly')
    
    if d or w or m:
        print("数据收集完成，正在生成日报...")
        # 构建HTML内容
        final_html = build_refined_html(d, w, m, CURRENT_DATE)
        
        # 保存HTML文件用于GitHub Pages
        filepath = save_html_file(final_html, CURRENT_DATE)
        print(f"日报已保存至: {filepath}")
        
        # 生成GitHub Pages索引页面
        generate_pages_index()
        print("GitHub Pages索引页面生成完成")
        
        # 发送到微信公众号（如果需要）
        print("正在推送至微信公众号...")
        publish_to_wechat(final_html, CURRENT_DATE)
        
        # 发送到飞书机器人（如果需要）
        print("正在推送至飞书机器人...")
        publish_to_feishu(final_html, CURRENT_DATE)
        
        print("所有任务完成！")
    else:
        print("未能获取到GitHub Trending数据")

if __name__ == "__main__":
    main()
