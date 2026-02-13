# GitHub Trending 日报系统

自动抓取 GitHub Trending 数据，通过 AI 生成深度分析报告，并推送至多个平台。

## 🌟 项目简介

本项目是一个自动化工具，每天定时从 GitHub Trending 页面抓取热门项目数据，利用 AI 技术为每个项目生成深度分析报告，然后将日报推送到微信公众号和飞书机器人，并通过 GitHub Pages 展示历史数据。

## 🚀 核心功能

- **自动化数据采集**：定时抓取 GitHub Trending 的日榜、周榜、月榜数据
- **AI 深度分析**：使用通义千问大模型为每个项目生成背景介绍、核心特性和技术亮点
- **多平台推送**：
  - 微信公众号推送
  - 飞书机器人推送
- **静态网站展示**：通过 GitHub Pages 展示历史日报数据
- **响应式设计**：支持 PC 和移动端浏览

## 📁 项目结构

```
github_trending/
├── .github/workflows/      # GitHub Actions 工作流
├── public/                 # 静态网页文件（GitHub Pages）
├── scripts/                # 核心脚本
│   ├── main.py            # 主程序入口
│   ├── github_trending.py # GitHub 数据抓取
│   ├── ai_processor.py    # AI 分析处理
│   ├── cache_manager.py   # LLM摘要缓存管理
│   ├── page_generator.py  # 页面生成
│   ├── wechat_publisher.py# 微信推送
│   └── feishu_publisher.py# 飞书推送
└── README.md
```

## 🔧 技术架构

### 数据采集层
- 使用 `requests` 和 `BeautifulSoup` 抓取 GitHub Trending 页面
- 支持分页抓取，获取完整的热门项目列表
- 提取项目名称、链接、描述、星标数等关键信息

### AI 分析层
- 集成阿里云 DashScope 平台的通义千问大模型
- 为每个项目生成标准化的分析报告：
  - **项目背景**：解决的行业痛点
  - **核心介绍**：技术实现方案
  - **关键特性**：核心技术亮点

### 智能缓存层
- **缓存管理**：实现LLM摘要缓存，避免重复调用并定期刷新（7天有效期）
  - 首次调用时通过LLM生成项目摘要并缓存
  - 后续调用优先使用缓存内容
  - 缓存超过7天自动刷新，确保信息新鲜度
  - 缓存文件存储在 `data/project_summaries_cache.json`
- **性能优化**：大幅减少LLM调用次数，降低成本并提升响应速度

### 内容展示层
- 生成精美的 HTML 页面
- 响应式设计，适配各种设备
- 按年月分类的历史数据导航

### 推送分发层
- 微信公众号推送（需配置服务器）
- 飞书机器人推送（Webhook 方式）
- GitHub Pages 静态网站展示

## ⚙️ 部署配置

### 环境要求
- Python 3.9+（推荐 3.10，与 GitHub Actions 保持一致）
- 依赖包：`requests`, `beautifulsoup4`, `dashscope`

### 目录结构说明
- `data/`：缓存数据目录（自动生成）
  - `project_summaries_cache.json`：LLM摘要缓存文件

### GitHub Actions 配置

在仓库的 Settings > Secrets 中配置以下环境变量：

#### AI 分析配置
- `DASHSCOPE_API_KEY`：阿里云 DashScope API 密钥

#### 微信推送配置（可选）
- `SERVER_URL`：微信推送服务器地址
- `SERVER_API_KEY`：服务器 API 密钥
- `THUMB_ID`：微信素材 ID

#### 飞书推送配置（可选）

##### 方式一：Webhook机器人推送
- `FEISHU_WEBHOOK_URL`：飞书机器人 Webhook URL
- `FEISHU_SIGN_KEY`：飞书机器人签名密钥（可选）

##### 方式二：应用API推送（推荐）
- `FEISHU_APP_ID`：飞书应用 App ID
- `FEISHU_APP_SECRET`：飞书应用 App Secret
- `FEISHU_RECEIVE_IDS`：接收者ID列表（JSON数组格式，如：["oc_xxx", "chat_yyy"]）

### 飞书机器人配置步骤

#### Webhook机器人配置
1. 在飞书群聊中添加自定义机器人
2. 获取 Webhook URL
3. 在 GitHub 仓库的 Settings > Secrets 中添加：
   - Name: `FEISHU_WEBHOOK_URL`
   - Value: 从飞书获取的 Webhook URL
4. （可选）如需签名验证，还需添加：
   - Name: `FEISHU_SIGN_KEY`
   - Value: 从飞书获取的签名密钥

#### 应用API推送配置（推荐）
1. 在飞书开放平台创建自建应用
2. 获取 App ID 和 App Secret
3. 获取需要推送的群聊或用户的 ID
4. 在 GitHub 仓库的 Settings > Secrets 中添加：
   - Name: `FEISHU_APP_ID`
   - Value: 从飞书获取的 App ID
   - Name: `FEISHU_APP_SECRET`
   - Value: 从飞书获取的 App Secret
   - Name: `FEISHU_RECEIVE_IDS`
   - Value: 接收者ID列表，格式为JSON数组，例如：`["oc_xxxxxxxxxxxx", "chat_yyyyyyyyyyyy"]`

## 📅 使用说明

### 手动运行
```bash
# 安装依赖
pip install -r scripts/requirements.txt

# 运行主程序
python scripts/main.py
```

### 自动运行
项目配置了每日自动运行的 GitHub Actions 工作流，默认在北京时间 07:30 执行（对应 UTC 23:30）。

## 🛡️ 安全性

- 所有敏感信息通过环境变量和 GitHub Secrets 管理
- 不在代码中硬编码任何密钥
- 使用 `.gitignore` 防止敏感文件被提交

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目。

## 📄 许可证

MIT License
