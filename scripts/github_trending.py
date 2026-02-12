import requests
from bs4 import BeautifulSoup

def fetch_trending(since):
    """
    从GitHub Trending页面抓取数据（支持翻页）
    
    Args:
        since (str): 时间范围 ('daily', 'weekly', 'monthly')
    
    Returns:
        list: 包含项目信息的字典列表
    """
    projects = []
    page = 1
    
    while True:
        url = f"https://github.com/trending?since={since}&page={page}"
        try:
            res = requests.get(url, headers={"User-Agent":"Mozilla/5.0"}, timeout=30)
            res.raise_for_status()
            soup = BeautifulSoup(res.text, 'html.parser')
            
            # 检查是否有项目数据
            articles = soup.select('article.Box-row')
            if not articles:
                break
                
            for art in articles:
                title_a = art.select_one('h2 a')
                name = title_a.get_text(strip=True).replace(' ','').replace('\n','')
                link = "https://github.com" + title_a['href']
                desc = art.select_one('p').get_text(strip=True) if art.select_one('p') else ""
                
                # 获取用户名（从链接中提取）
                user_name = name.split('/')[0] if '/' in name else ""
                
                # 获取编程语言
                language_elem = art.select_one('span[itemprop="programmingLanguage"]')
                language = language_elem.get_text(strip=True) if language_elem else ""
                
                stats = art.select('a.Link--muted')
                total_stars = stats[0].get_text(strip=True) if len(stats) > 0 else "0"
                added_stars = art.select_one('span.d-inline-block.float-sm-right')
                added_stars = added_stars.get_text(strip=True) if added_stars else "0 stars"
                
                projects.append({
                    "name": name, 
                    "link": link, 
                    "desc": desc, 
                    "user_name": user_name,
                    "language": language,
                    "total_stars": total_stars,
                    "added_stars": added_stars
                })
            
            # 检查是否还有下一页
            next_button = soup.select_one('a.next_page')
            if not next_button:
                break
                
            page += 1
            
        except Exception as e:
            print(f"抓取失败: {e}")
            break
    
    return projects