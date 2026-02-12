import json
import os
import time
from datetime import datetime, timedelta

# 缓存文件路径
CACHE_FILE = "data/project_summaries_cache.json"
# 缓存过期时间（7天）
CACHE_EXPIRY_DAYS = 7

def init_cache():
    """初始化缓存目录和文件"""
    os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
    if not os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump({}, f)

def load_cache():
    """加载缓存数据"""
    try:
        with open(CACHE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # 如果文件不存在或损坏，初始化空缓存
        init_cache()
        return {}

def save_cache(cache_data):
    """保存缓存数据"""
    try:
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"保存缓存失败: {e}")

def is_cache_expired(timestamp):
    """检查缓存是否过期"""
    try:
        cache_time = datetime.fromisoformat(timestamp)
        return datetime.now() - cache_time > timedelta(days=CACHE_EXPIRY_DAYS)
    except:
        # 如果时间戳格式不正确，认为已过期
        return True

def get_cached_summary(project_name):
    """获取项目的缓存摘要"""
    cache = load_cache()
    
    # 检查项目是否在缓存中
    if project_name in cache:
        project_data = cache[project_name]
        
        # 检查缓存是否过期
        if not is_cache_expired(project_data.get('timestamp', '')):
            return project_data.get('summary', None)
        else:
            # 缓存过期，从缓存中删除
            del cache[project_name]
            save_cache(cache)
    
    return None

def cache_summary(project_name, summary):
    """缓存项目摘要"""
    cache = load_cache()
    
    # 更新或添加项目摘要
    cache[project_name] = {
        'summary': summary,
        'timestamp': datetime.now().isoformat()
    }
    
    save_cache(cache)