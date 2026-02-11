import os
import re
import subprocess

def get_github_pages_url():
    """
    动态获取当前仓库的GitHub Pages URL
    
    Returns:
        str: GitHub Pages URL，如果无法获取则返回默认URL
    """
    try:
        # 获取远程仓库URL
        result = subprocess.run(['git', 'remote', 'get-url', 'origin'], 
                              capture_output=True, text=True, cwd=os.getcwd())
        
        if result.returncode == 0:
            remote_url = result.stdout.strip()
            # 支持HTTPS和SSH格式的URL
            # HTTPS格式: https://github.com/username/repository.git
            # SSH格式: git@github.com:username/repository.git
            
            # 使用正则表达式提取用户名和仓库名
            https_pattern = r'https://github\.com/([^/]+)/([^/]+)(?:\.git)?$'
            ssh_pattern = r'git@github\.com:([^/]+)/([^/]+)(?:\.git)?$'
            
            https_match = re.match(https_pattern, remote_url)
            ssh_match = re.match(ssh_pattern, remote_url)
            
            if https_match or ssh_match:
                match = https_match if https_match else ssh_match
                username = match.group(1)
                repo_name = match.group(2).replace('.git', '')
                return f"https://{username}.github.io/{repo_name}/"
        
        # 如果无法解析，返回默认URL
        return "https://sixs.github.io/github_trending/"
        
    except Exception as e:
        # 发生异常时返回默认URL
        print(f"获取GitHub Pages URL时出错: {e}")
        return "https://sixs.github.io/github_trending/"