import os
import re
from datetime import datetime

def build_refined_html(daily, weekly, monthly):
    """
    构建精美的GitHub Trending日报HTML页面（用于iframe内嵌显示，无顶部栏和侧边栏）
    
    Args:
        daily (list): 每日热门项目列表
        weekly (list): 每周热门项目列表
        monthly (list): 每月热门项目列表
    
    Returns:
        str: 完整的HTML页面内容
    """
    from ai_processor import get_rich_summary, clean_md_to_html
    
    date_str = datetime.now().strftime('%Y / %m / %d')
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GitHub Trending - {date_str}</title>
    <style>
        :root {{
            --primary-color: #0366d6;
            --background-color: #f6f8fa;
            --card-background: #ffffff;
            --text-color: #333333;
            --border-color: #e1e4e8;
        }}
        
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
            line-height: 1.6;
            color: var(--text-color);
            background-color: var(--background-color);
        }}
        
        /* 内容区域 */
        .content {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        .project {{
            background: var(--card-background);
            margin-bottom: 20px;
            padding: 20px;
            border-radius: 6px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        
        .project-title {{
            font-size: 24px;
            font-weight: 600;
            margin-bottom: 10px;
            color: #24292e;
        }}
        
        .project-stats {{
            font-size: 14px;
            color: #586069;
            margin-bottom: 15px;
        }}
        
        .project-content {{
            margin-bottom: 15px;
        }}
        
        .project-link {{
            display: inline-block;
            color: var(--primary-color);
            text-decoration: none;
            font-size: 14px;
        }}
        
        .project-link:hover {{
            text-decoration: underline;
        }}
        
        .section-title {{
            font-size: 28px;
            font-weight: 600;
            margin: 30px 0 20px 0;
            padding-bottom: 10px;
            border-bottom: 2px solid var(--border-color);
            color: #24292e;
        }}
        
        .rank-number {{
            font-size: 20px;
            font-weight: bold;
            color: #666;
            margin-right: 10px;
        }}
        
        /* 页脚 */
        .footer {{
            text-align: center;
            padding: 20px;
            color: #666;
            font-size: 14px;
            border-top: 1px solid var(--border-color);
            margin-top: 30px;
        }}
    </style>
</head>
<body>
    <div class="content">
        <div style="text-align: center; margin-bottom: 20px; color: #666;">
            <p>{date_str}</p>
        </div>'''

    sections = [("今日趋势", daily), ("本周热门", weekly), ("月度榜单", monthly)]
    
    for section_title, data in sections:
        if not data: continue
        
        html += f'<div class="section-title">{section_title}</div>'
        
        for i, p in enumerate(data):
            rich_content = get_rich_summary(p)
            # 关键：将 AI 返回内容中的 MD 语法转化为 HTML
            rich_content = clean_md_to_html(rich_content)
            
            paragraphs = rich_content.split('\n')
            indented_content = ""
            for para in paragraphs:
                if para.strip():
                    indented_content += f'<p class="project-content">&nbsp;&nbsp;&nbsp;&nbsp;{para.strip()}</p>'

            html += f'''
            <div class="project">
                <div>
                    <span class="rank-number">#{i+1}</span>
                    <span class="project-title">{p['name']}</span>
                </div>
                
                <div class="project-stats">
                    <span>总星标: {p['total_stars']}</span> | 
                    <span>新增星标: {p['added_stars']}</span>
                </div>
                
                <div>
                    {indented_content}
                </div>
                
                <div>
                    <a href="{p['link']}" class="project-link" target="_blank">查看项目详情 →</a>
                    {f' | <a href="https://github.com/{p["user_name"]}" class="project-link" target="_blank">用户主页</a>' if p.get('user_name') else ''}
                </div>
            </div>'''
            
    html += '''
            </div>
            
            <div style="text-align: center; margin: 30px 0;">
                <a href="index.html" style="display: inline-block; padding: 10px 20px; background-color: var(--primary-color); color: white; text-decoration: none; border-radius: 4px; font-size: 16px;">← 返回历史日报首页</a>
            </div>
            
            <div class="footer">
                <p>© 2026 GitHub Trending 日报 | 数据来源于 GitHub Trending</p>
            </div>
        </div>
    </div>
</body>
</html>'''
    return html

def save_html_file(html_content):
    """
    保存HTML文件到public目录
    
    Args:
        html_content (str): HTML内容
    
    Returns:
        str: 文件路径
    """
    # 创建public目录
    os.makedirs('public', exist_ok=True)
    
    # 生成文件名
    filename = f"trending-{datetime.now().strftime('%Y-%m-%d')}.html"
    filepath = os.path.join('public', filename)
    
    # 保存HTML文件
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"HTML文件已保存: {filepath}")
    return filepath

def list_trending_pages(out_dir):
    """
    列出public目录下的所有trending页面
    
    Args:
        out_dir (str): 目录路径
    
    Returns:
        list: 页面文件名列表
    """
    if not os.path.isdir(out_dir):
        return []
    files = [f for f in os.listdir(out_dir) if re.match(r'^trending-\d{4}-\d{2}-\d{2}\.html$', f)]
    files.sort(reverse=True)
    return files

def generate_index_html(out_dir, latest_file, nav_items):
    """
    生成GitHub Pages索引页面（按年/月分类导航）
    
    Args:
        out_dir (str): 输出目录
        latest_file (str): 最新文件名
        nav_items (list): 导航项列表
    """
    # 获取所有trending页面并按年月分组
    pages = list_trending_pages(out_dir)
    
    # 按年月分组
    grouped_pages = {}
    year_month_list = []  # 用于快速导航
    
    for page in pages:
        match = re.match(r'^trending-(\d{4})-(\d{2})-(\d{2})\.html$', page)
        if match:
            year, month, day = match.groups()
            year_month = f"{year}-{month}"
            date = f"{year}-{month}-{day}"
            
            if year not in grouped_pages:
                grouped_pages[year] = {}
            if month not in grouped_pages[year]:
                grouped_pages[year][month] = []
            
            # 获取星期几
            try:
                from datetime import datetime
                dt = datetime(int(year), int(month), int(day))
                weekdays = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
                weekday = weekdays[dt.weekday()]
            except:
                weekday = "未知"
            
            grouped_pages[year][month].append({
                'filename': page,
                'date': date,
                'display_date': f"{month}月{day}日",
                'weekday': weekday
            })
            
            # 添加到年月列表（去重）
            if year_month not in year_month_list:
                year_month_list.append(year_month)
    
    # 生成年月快速导航
    year_month_nav = ""
    for year_month in sorted(year_month_list, reverse=True):
        year, month = year_month.split('-')
        month_names = {
            '01': '01月', '02': '02月', '03': '03月', '04': '04月',
            '05': '05月', '06': '06月', '07': '07月', '08': '08月',
            '09': '09月', '10': '10月', '11': '11月', '12': '12月'
        }
        display_month = month_names.get(month, f"{month}月")
        year_month_nav += f'            <a href="#{year_month}" class="year-month-item">{year}年{display_month}</a>\n'
    
    # 生成按年月分组的内容
    content_html = ""
    for year in sorted(grouped_pages.keys(), reverse=True):
        content_html += f'''        <!-- 按年份分组 -->
        <div class="year-group">
            <div class="year-header" id="{year}">{year}年</div>
            
'''
        
        for month in sorted(grouped_pages[year].keys(), reverse=True):
            month_names = {
                '01': '01月', '02': '02月', '03': '03月', '04': '04月',
                '05': '05月', '06': '06月', '07': '07月', '08': '08月',
                '09': '09月', '10': '10月', '11': '11月', '12': '12月'
            }
            display_month = month_names.get(month, f"{month}月")
            
            content_html += f'''            <!-- 按月份分组 -->
            <div class="month-group">
                <div class="month-header" id="{year}-{month}">{display_month}</div>
                <div class="date-list">
'''
            
            for page_info in grouped_pages[year][month]:
                content_html += f'''                    <a href="{page_info['filename']}" class="date-item">
                        <div class="date">{page_info['display_date']}</div>
                        <div class="weekday">{page_info['weekday']}</div>
                    </a>
'''
            
            content_html += '''                </div>
            </div>
            
'''
        
        content_html += '''        </div>
        
'''
    
    index_path = os.path.join(out_dir, 'index.html')
    html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GitHub Trending - 历史日报</title>
    <style>
        :root {{
            --primary-color: #0366d6;
            --background-color: #f6f8fa;
            --card-background: #ffffff;
            --text-color: #333333;
            --border-color: #e1e4e8;
            --header-height: 60px;
        }}
        
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}
        
        html, body {{
            height: 100%;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
            line-height: 1.6;
            color: var(--text-color);
            background-color: var(--background-color);
        }}
        
        /* 响应式设计 */
        @media (max-width: 768px) {{
            :root {{
                --header-height: 80px;
            }}
            
            .header {{
                flex-direction: column;
                height: auto;
                padding: 10px;
            }}
            
            .header h1 {{
                font-size: 24px;
            }}
            
            .year-month-nav {{
                margin: 10px 0;
            }}
        }}
        
        /* 头部样式 */
        .header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 20px;
            background: var(--card-background);
            border-bottom: 1px solid var(--border-color);
            height: var(--header-height);
            min-height: var(--header-height);
            position: sticky;
            top: 0;
            z-index: 10;
        }}
        
        .header h1 {{
            font-size: 28px;
            color: var(--text-color);
        }}
        
        /* 年月导航 */
        .year-month-nav {{
            display: flex;
            gap: 15px;
            margin: 20px 0;
            flex-wrap: wrap;
        }}
        
        .year-month-item {{
            background: var(--card-background);
            border: 1px solid var(--border-color);
            border-radius: 4px;
            padding: 8px 15px;
            text-decoration: none;
            color: var(--text-color);
            transition: all 0.2s ease;
        }}
        
        .year-month-item:hover {{
            background: var(--primary-color);
            color: white;
            border-color: var(--primary-color);
        }}
        
        /* 内容区域 */
        .content {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        /* 按年份分组 */
        .year-group {{
            margin-bottom: 40px;
        }}
        
        .year-header {{
            font-size: 24px;
            font-weight: 600;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid var(--border-color);
            color: #24292e;
        }}
        
        /* 按月份分组 */
        .month-group {{
            margin-bottom: 30px;
        }}
        
        .month-header {{
            font-size: 20px;
            font-weight: 500;
            margin-bottom: 15px;
            color: #24292e;
        }}
        
        /* 日期列表 */
        .date-list {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 15px;
        }}
        
        @media (max-width: 768px) {{
            .date-list {{
                grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
            }}
        }}
        
        .date-item {{
            background: var(--card-background);
            border: 1px solid var(--border-color);
            border-radius: 6px;
            padding: 15px;
            text-align: center;
            text-decoration: none;
            color: var(--text-color);
            transition: all 0.2s ease;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        
        .date-item:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
            border-color: var(--primary-color);
        }}
        
        .date-item .date {{
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 5px;
        }}
        
        .date-item .weekday {{
            font-size: 14px;
            color: #666;
        }}
        
        /* 页脚 */
        .footer {{
            text-align: center;
            padding: 20px;
            color: #666;
            font-size: 14px;
            border-top: 1px solid var(--border-color);
            margin-top: 30px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>GitHub Trending 历史日报</h1>
    </div>
    
    <div class="content">
        <!-- 年月快速导航 -->
        <div class="year-month-nav">
{0}        </div>
        
{1}    </div>
    
    <div class="footer">
        <p>© 2026 GitHub Trending 日报 | 数据来源于 GitHub Trending</p>
    </div>
</body>
</html>'''.format(year_month_nav, content_html)
    
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(html)

def generate_pages_index():
    """
    生成GitHub Pages索引页面
    """
    out_dir = 'public'
    pages = list_trending_pages(out_dir)
    if not pages:
        print('No trending pages found in', out_dir)
        return
    latest = pages[0]
    # Create navigation items
    nav_items = []
    for p in pages:
        m = re.match(r'^trending-(\d{4}-\d{2}-\d{2})\.html$', p)
        label = m.group(1) if m else p
        nav_items.append(f'<li><a href="{p}">{label}</a></li>')
    generate_index_html(out_dir, latest, nav_items)
    print('Generated index.html with latest:', latest)