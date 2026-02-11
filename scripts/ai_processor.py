import os
import re
import dashscope
from dashscope import Generation

def clean_md_to_html(text):
    """
    处理 AI 可能返回的 Markdown 加粗格式为微信识别的 HTML
    
    Args:
        text (str): 包含Markdown格式的文本
    
    Returns:
        str: 转换后的HTML格式文本
    """
    # 处理 **加粗** 为 <strong>加粗</strong>
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong style="color:#000;">\1</strong>', text)
    # 处理【标题】为加粗
    text = text.replace('【项目背景】', '<strong style="color:#1a1a1a;">【项目背景】</strong>')
    text = text.replace('【核心介绍】', '<strong style="color:#1a1a1a;">【核心介绍】</strong>')
    text = text.replace('【关键特性】', '<strong style="color:#1a1a1a;">【关键特性】</strong>')
    return text

def get_rich_summary(p):
    """
    使用DashScope模型为GitHub项目生成详细摘要
    
    Args:
        p (dict): 包含项目信息的字典
    
    Returns:
        str: 项目摘要
    """
    dashscope.api_key = os.environ.get("DASHSCOPE_API_KEY")
    prompt = (
        f"你是一个资深架构师。请深入分析GitHub项目 '{p['name']}'。描述：{p['desc']}。\n"
        "请严格按以下格式输出（中文）：\n"
        "【项目背景】一句话说明该项目解决了什么行业痛点。\n"
        "【核心介绍】两句话说明其技术实现方案或定位。\n"
        "【关键特性】列举2个核心技术亮点，重要词汇请用双星号加粗。"
    )
    try:
        resp = Generation.call(model="qwen-max", prompt=prompt, result_format='message')
        if resp.status_code == 200:
            return resp.output.choices[0].message.content
        return f"【项目背景】{p['desc']}"
    except:
        return f"【项目背景】{p['desc']}"