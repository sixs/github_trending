import os
import requests
import json
import time
from datetime import datetime

# 导入GitHub工具模块
try:
    import scripts.github_utils
    get_github_pages_url = scripts.github_utils.get_github_pages_url
except ImportError:
    # 如果无法导入，定义一个默认函数
    def get_github_pages_url():
        return "https://sixs.github.io/github_trending/"

def get_trending_page_url():
    """
    获取当前日期的GitHub Trending日报页面URL
    
    Returns:
        str: 当前日期的日报页面URL
    """
    from datetime import datetime
    base_url = get_github_pages_url()
    if base_url.endswith('/'):
        base_url = base_url[:-1]
    
    date_str = datetime.now().strftime('%Y-%m-%d')
    return f"{base_url}/trending-{date_str}.html"

# 缓存tenant_access_token及其过期时间
_tenant_access_token = None
_token_expires_at = 0

def get_tenant_access_token():
    """
    获取飞书租户访问令牌(tenant_access_token)
    使用App ID和App Secret获取，有效期2小时
    """
    global _tenant_access_token, _token_expires_at
    
    # 检查缓存的token是否 still有效 (提前5分钟过期)
    current_time = time.time()
    if _tenant_access_token and _token_expires_at > current_time + 300:
        return _tenant_access_token
    
    app_id = os.environ.get("FEISHU_APP_ID")
    app_secret = os.environ.get("FEISHU_APP_SECRET")
    
    if not app_id or not app_secret:
        print("未配置飞书App ID或App Secret")
        return None
    
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/"
    
    payload = {
        "app_id": app_id,
        "app_secret": app_secret
    }
    
    headers = {
        "Content-Type": "application/json; charset=utf-8"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        if response.status_code == 200:
            result = response.json()
            if result.get("code") == 0:
                _tenant_access_token = result.get("tenant_access_token")
                # 设置过期时间 (2小时 - 10分钟缓冲)
                _token_expires_at = current_time + 6600
                return _tenant_access_token
            else:
                print(f"获取tenant_access_token失败: {result}")
                return None
        else:
            print(f"获取tenant_access_token失败: HTTP {response.status_code}")
            return None
    except Exception as e:
        print(f"获取tenant_access_token异常: {e}")
        return None

def send_message_to_receivers(receive_ids, message_content, receive_id_type="open_id"):
    """
    向指定的receive_id列表发送消息
    
    Args:
        receive_ids (list): 接收者ID列表
        message_content (dict): 消息内容
        receive_id_type (str): 接收者ID类型 (open_id, union_id, user_id, email, chat_id)
    """
    tenant_access_token = get_tenant_access_token()
    if not tenant_access_token:
        return False
    
    url = f"https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type={receive_id_type}"
    
    headers = {
        "Authorization": f"Bearer {tenant_access_token}",
        "Content-Type": "application/json; charset=utf-8"
    }
    
    success_count = 0
    failed_count = 0
    
    for receive_id in receive_ids:
        try:
            payload = {
                "receive_id": receive_id,
                "msg_type": "interactive",
                "content": json.dumps(message_content, ensure_ascii=False)
            }
            
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            if response.status_code == 200:
                result = response.json()
                if result.get("code") == 0:
                    success_count += 1
                else:
                    print(f"向 {receive_id} 发送消息失败: {result}")
                    failed_count += 1
            else:
                print(f"向 {receive_id} 发送消息失败: HTTP {response.status_code}")
                print(f"Response content: {response.text}")
                failed_count += 1
        except Exception as e:
            print(f"向 {receive_id} 发送消息异常: {e}")
            failed_count += 1
    
    print(f"飞书消息推送完成: 成功 {success_count} 个, 失败 {failed_count} 个")
    return success_count > 0

def create_interactive_message(html_content):
    """
    创建交互式消息卡片
    
    Args:
        html_content (str): HTML内容
        
    Returns:
        dict: 消息卡片内容
    """
    return {
        "config": {
            "wide_screen_mode": True
        },
        "header": {
            "template": "blue",
            "title": {
                "content": f"【{datetime.now().strftime('%m%d')}】GitHub 热门项目日报",
                "tag": "plain_text"
            }
        },
        "elements": [
            {
                "tag": "div",
                "text": {
                    "content": "GitHub Trending 日报已生成，请点击下方按钮查看完整内容",
                    "tag": "lark_md"
                }
            },
            {
                "tag": "action",
                "actions": [
                    {
                        "tag": "button",
                        "text": {
                            "content": "查看日报",
                            "tag": "plain_text"
                        },
                        "type": "primary",
                        "url": get_trending_page_url()
                    }
                ]
            }
        ]
    }

def publish_to_feishu_webhook(html_content):
    """
    通过Webhook将GitHub Trending日报推送到飞书机器人
    
    Args:
        html_content (str): HTML内容
    """
    try:
        webhook_url = os.environ.get("FEISHU_WEBHOOK_URL")
        if not webhook_url:
            print("未配置飞书Webhook URL")
            return
            
        # 构造飞书消息体
        payload = {
            "msg_type": "interactive",
            "card": {
                "config": {
                    "wide_screen_mode": True
                },
                "header": {
                    "template": "blue",
                    "title": {
                        "content": f"【{datetime.now().strftime('%m%d')}】GitHub 热门项目日报",
                        "tag": "plain_text"
                    }
                },
                "elements": [
                    {
                        "tag": "div",
                        "text": {
                            "content": "GitHub Trending 日报已生成，请点击下方按钮查看完整内容",
                            "tag": "lark_md"
                        }
                    },
                    {
                        "tag": "action",
                        "actions": [
                            {
                                "tag": "button",
                                "text": {
                                    "content": "查看日报",
                                    "tag": "plain_text"
                                },
                                "type": "primary",
                                "url": get_trending_page_url()
                            }
                        ]
                    }
                ]
            }
        }
        
        # 发送请求
        response = requests.post(
            webhook_url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload, ensure_ascii=False).encode('utf-8'),
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get("code") == 0:
                print("飞书Webhook推送成功")
            else:
                print(f"飞书Webhook推送失败: {result}")
        else:
            print(f"飞书Webhook推送失败: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"飞书Webhook推送异常: {e}")

def publish_to_feishu_app(html_content):
    """
    通过App ID和App Secret将GitHub Trending日报推送到指定的receive_id列表
    
    Args:
        html_content (str): HTML内容
    """
    try:
        # 检查是否配置了App ID和App Secret
        app_id = os.environ.get("FEISHU_APP_ID")
        app_secret = os.environ.get("FEISHU_APP_SECRET")
        
        if not app_id or not app_secret:
            print("未配置飞书App ID或App Secret，跳过App推送")
            return
            
        # 获取接收者ID列表
        receive_ids_str = os.environ.get("FEISHU_RECEIVE_IDS")
        if not receive_ids_str:
            print("未配置飞书接收者ID列表")
            return
            
        # 解析接收者ID列表
        try:
            receive_ids = json.loads(receive_ids_str)
            if not isinstance(receive_ids, list):
                print("飞书接收者ID列表格式错误，应为JSON数组")
                return
        except json.JSONDecodeError:
            print("飞书接收者ID列表格式错误，应为JSON数组")
            return
            
        if not receive_ids:
            print("飞书接收者ID列表为空")
            return
            
        # 创建消息内容
        message_content = create_interactive_message(html_content)
        
        # 发送消息
        send_message_to_receivers(receive_ids, message_content)
        
    except Exception as e:
        print(f"飞书App推送异常: {e}")

def publish_to_feishu(html_content):
    """
    将GitHub Trending日报推送到飞书
    
    Args:
        html_content (str): HTML内容
    """
    # 优先使用Webhook推送
    webhook_url = os.environ.get("FEISHU_WEBHOOK_URL")
    if webhook_url:
        publish_to_feishu_webhook(html_content)
    
    # 如果配置了App ID和App Secret，则也使用App推送
    app_id = os.environ.get("FEISHU_APP_ID")
    app_secret = os.environ.get("FEISHU_APP_SECRET")
    if app_id and app_secret:
        publish_to_feishu_app(html_content)