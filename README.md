### AI Doc Platform
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
│   │   │   ├── config.py          # 配置管理(包含DeepSeek API配置)
│   │   │   └── security.py        # 安全相关功能
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── schemas.py         # Pydantic模型
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── deepseek_service.py # DeepSeek LLM服务
│   │   │   ├── ppt_generator.py   # PPT生成服务
│   │   │   └── word_generator.py  # Word文档生成服务
│   │   ├── agents/
│   │   │   ├── __init__.py
│   │   │   ├── doc_agent.py       # 文档生成Agent
│   │   │   └── tools/
│   │   │       ├── __init__.py
│   │   │       ├── research_tool.py    # 研究工具
│   │   │       ├── ppt_tool.py         # PPT生成工具
│   │   │       └── word_tool.py        # Word生成工具
│   │   ├── utils/
│   │   │   ├── __init__.py
│   │   │   ├── helpers.py         # 辅助函数
│   │   │   └── prompts.py         # 提示模板
│   │   ├── templates/             # 文档模板文件
│   │   │   ├── ppt_templates/
│   │   │   └── word_templates/
│   │   └── main.py                # 应用入口点
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_api.py
│   │   └── test_services.py
│   ├── .env.example               # 环境变量示例
│   ├── requirements.txt           # Python依赖
│   └── Dockerfile                 # 后端Docker构建文件
│
├── frontend/
│   ├── public/
│   │   ├── favicon.ico
│   │   └── index.html
│   ├── src/
│   │   ├── assets/
│   │   │   ├── logo.png
│   │   │   ├── css/
│   │   │   └── images/
│   │   ├── components/
│   │   │   ├── Header.vue
│   │   │   ├── Footer.vue
│   │   │   ├── DocumentForm.vue
│   │   │   ├── ProgressIndicator.vue
│   │   │   └── DocumentPreview.vue
│   │   ├── views/
│   │   │   ├── Home.vue
│   │   │   ├── Generate.vue
│   │   │   ├── Results.vue
│   │   │   └── History.vue
│   │   ├── services/
│   │   │   ├── api.js             # API调用服务
│   │   │   └── auth.js            # 认证服务
│   │   ├── store/
│   │   │   ├── index.js
│   │   │   ├── modules/
│   │   │   │   ├── documents.js
│   │   │   │   └── user.js
│   │   ├── router/
│   │   │   └── index.js           # Vue路由配置
│   │   ├── utils/
│   │   │   └── helpers.js
│   │   ├── App.vue
│   │   └── main.js
│   ├── .env.development
│   ├── .env.production
│   ├── package.json
│   ├── babel.config.js
│   ├── vue.config.js
│   └── Dockerfile                 # 前端Docker构建文件
│
├── nginx/
│   ├── nginx.conf                 # Nginx配置
│   └── Dockerfile                 # Nginx Docker构建文件
│
├── docker-compose.yml             # Docker Compose配置
├── .gitignore
└── README.md                      # 项目说明
```
