# AI 文档平台

AI 文档平台是一个基于 DeepSeek API 的智能文档生成系统，可以根据用户提供的主题自动生成 PPT 演示文稿和 Word 文档。

## 项目结构

```
ai-doc-platform/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── routes.py          # API路由定义
│   │   │   └── dependencies.py     # API依赖项
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   └── config.py          # 核心配置
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── schemas.py         # Pydantic模型
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── deepseek_service.py # DeepSeek API服务
│   │   │   ├── ppt_generator.py   # PPT生成服务
│   │   │   └── word_generator.py  # Word生成服务
│   │   ├── templates/
│   │   │   ├── ppt_templates/     # PPT模板
│   │   │   └── word_templates/    # Word模板
│   │   ├── __init__.py
│   │   └── main.py               # 应用入口
│   ├── tests/                    # 测试目录
│   └── requirements.txt          # 依赖项
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── assets/               # 静态资源
│   │   ├── components/           # Vue组件
│   │   ├── router/               # 路由配置
│   │   ├── services/             # API服务
│   │   ├── store/                # Vuex状态管理
│   │   ├── views/                # 页面视图
│   │   ├── App.vue               # 主应用组件
│   │   └── main.js               # 前端入口
│   ├── .env.development          # 开发环境配置
│   ├── .env.production           # 生产环境配置
│   ├── package.json              # 前端依赖
│   └── Dockerfile                # 前端Docker构建文件
├── nginx/
│   ├── nginx.conf                # Nginx配置
│   └── Dockerfile                # Nginx Docker构建文件
├── docker-compose.yml            # Docker Compose配置
├── .env                          # 环境变量
├── .gitignore
└── README.md                     # 项目说明
```

## 功能特性

- 基于 DeepSeek API 的智能文档生成
- 支持 PPT 演示文稿和 Word 文档生成
- 实时生成状态跟踪
- 文档历史记录管理
- 文档预览和下载

## 技术栈

### 后端
- FastAPI - 高性能 Python Web 框架
- Python-PPTX - PPT 文档生成库
- Python-DOCX - Word 文档生成库
- DeepSeek API - AI 内容生成

### 前端
- Vue.js - 前端框架
- Vuex - 状态管理
- Vue Router - 路由管理
- Axios - HTTP 客户端

### 部署
- Docker & Docker Compose - 容器化部署
- Nginx - Web 服务器和反向代理

## 环境要求

- Python 3.8+
- Node.js 14+
- Docker & Docker Compose (可选，用于容器化部署)

## 项目启动指南

### 环境配置

1. 克隆项目
```bash
git clone https://github.com/yourusername/ai-doc-platform.git
cd ai-doc-platform
```

2. 创建并配置 `.env` 文件
```
AI_API_KEY=your_deepseek_api_key
AI_API_ENDPOINT=https://api.deepseek.com/v1/chat/completions
SECRET_KEY=your_secret_key_for_jwt
```

### 后端启动

1. 进入后端目录
```bash
cd backend
```

2. 创建虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 启动服务
```bash
uvicorn app.main:app --reload
```

后端服务将在 http://localhost:8000 运行，API 文档可在 http://localhost:8000/docs 查看。

### 前端启动

1. 进入前端目录
```bash
cd frontend
```

2. 安装依赖
```bash
npm install
```

3. 启动开发服务器
```bash
npm run serve
```

前端应用将在 http://localhost:8080 运行。

### 使用 Docker Compose 启动

如果您想使用 Docker 启动整个应用：

```bash
docker-compose up -d
```

应用将在 http://localhost 运行。

## 使用指南

1. 访问首页，点击"开始创建"按钮
2. 输入文档主题，选择文档类型（PPT 或 Word）
3. 可选择添加额外信息或选择模板
4. 点击"生成文档"按钮
5. 等待文档生成完成
6. 下载或预览生成的文档

## 安全注意事项

- `.env` 文件包含 API 密钥，确保不要将其提交到版本控制系统中
- 在生产环境中，应该使用更安全的密钥管理方式
- 考虑添加用户认证和授权机制
- 对 API 请求添加速率限制以防止滥用

## 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

## 许可证

[MIT License](LICENSE)