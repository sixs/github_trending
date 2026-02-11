import os
import requests
from datetime import datetime

def publish_to_wechat(html_content):
    """
    将GitHub Trending日报推送到微信公众号
    
    Args:
        html_content (str): HTML内容
    """
    try:
        response = requests.post(
            os.environ.get("SERVER_URL"),
            headers={"X-Api-Key": os.environ.get("SERVER_API_KEY")},
            json={
                "title": f"【{datetime.now().strftime('%m%d')}】GitHub 热门项目日报",
                "content": html_content,
                "thumb_id": os.environ.get("THUMB_ID"),
                "digest": "全方位解析今日热门 GitHub 项目：背景、架构与核心特性。"
            },
            timeout=60
        )
        print(f"微信推送结果: {response.json()}")
    except Exception as e:
        print(f"微信推送失败: {e}")