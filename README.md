# AI_doc_platform

## 1. 项目根目录

```
document-ai-platform/
├── frontend/            # 前端Vue项目
├── backend/             # 后端服务集合
├── docker/              # Docker相关配置
├── scripts/             # 部署和工具脚本
├── docs/                # 项目文档
├── .github/             # GitHub Actions配置
├── .gitignore
├── README.md
└── docker-compose.yml
```

## 2. 前端目录结构

```
frontend/
├── public/                     # 静态资源，不经过webpack处理
│   ├── favicon.ico
│   └── index.html
├── src/                        # 源代码
│   ├── assets/                 # 静态资源
│   │   ├── images/            # 图片资源
│   │   ├── styles/            # 全局样式
│   │   └── fonts/             # 字体资源
│   ├── components/            # 组件
│   │   ├── common/            # 通用组件
│   │   │   ├── AppHeader.vue
│   │   │   ├── AppFooter.vue
│   │   │   ├── AppSidebar.vue
│   │   │   └── ...
│   │   ├── document/          # 文档相关组件
│   │   │   ├── DocumentList.vue
│   │   │   ├── DocumentUploader.vue
│   │   │   ├── DocumentPreview.vue
│   │   │   └── ...
│   │   ├── ocr/               # OCR相关组件
│   │   │   ├── OcrStatusCard.vue
│   │   │   ├── TextEditor.vue
│   │   │   └── ...
│   │   └── generator/         # 文档生成组件
│   │       ├── TemplateSelector.vue
│   │       ├── PptGenerator.vue
│   │       ├── WordGenerator.vue
│   │       └── ...
│   ├── views/                  # 页面
│   │   ├── HomeView.vue
│   │   ├── LoginView.vue
│   │   ├── RegisterView.vue
│   │   ├── DocumentsView.vue
│   │   ├── DocumentDetailView.vue
│   │   ├── GeneratorView.vue
│   │   ├── ProfileView.vue
│   │   └── ...
│   ├── router/                 # 路由配置
│   │   ├── index.js
│   │   └── routes.js
│   ├── stores/                 # Pinia状态管理
│   │   ├── auth.js
│   │   ├── documents.js
│   │   ├── ocr.js
│   │   ├── generator.js
│   │   └── index.js
│   ├── services/               # API服务
│   │   ├── api.js             # API基础配置
│   │   ├── auth.service.js
│   │   ├── document.service.js
│   │   ├── ocr.service.js
│   │   ├── generator.service.js
│   │   └── ...
│   ├── utils/                  # 工具函数
│   │   ├── validation.js
│   │   ├── formatters.js
│   │   ├── file-helpers.js
│   │   └── ...
│   ├── constants/              # 常量定义
│   │   ├── api.js
│   │   ├── status.js
│   │   └── ...
│   ├── App.vue                 # 根组件
│   ├── main.js                 # 入口文件
│   └── config.js               # 全局配置
├── .env                        # 环境变量
├── .env.development            # 开发环境变量
├── .env.production             # 生产环境变量
├── vite.config.js              # Vite配置
├── package.json                # 依赖管理
└── README.md
```


## 3. 后端目录结构

```
backend/
├── gateway/                    # API网关服务
│   ├── src/
│   │   ├── config/            # 配置文件
│   │   ├── middlewares/       # 中间件
│   │   ├── routes/            # 路由转发
│   │   ├── utils/             # 工具函数
│   │   └── app.js             # 应用入口
│   ├── Dockerfile
│   └── package.json
│
├── auth-service/               # 用户认证服务
│   ├── src/
│   │   ├── config/
│   │   ├── controllers/
│   │   ├── models/
│   │   ├── middlewares/
│   │   ├── routes/
│   │   ├── services/
│   │   ├── utils/
│   │   └── app.js
│   ├── Dockerfile
│   └── package.json
│
├── document-service/           # 文档管理服务
│   ├── src/
│   │   ├── config/
│   │   ├── controllers/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── services/
│   │   ├── utils/
│   │   └── app.js
│   ├── Dockerfile
│   └── package.json
│
├── ocr-service/                # OCR处理服务
│   ├── src/
│   │   ├── config/
│   │   ├── controllers/
│   │   ├── models/
│   │   ├── services/
│   │   │   ├── pdf-extractor.js
│   │   │   ├── ocr-processor.js
│   │   │   └── ...
│   │   ├── utils/
│   │   └── app.js
│   ├── Dockerfile
│   └── package.json
│
├── content-service/            # 内容处理服务
│   ├── src/
│   │   ├── config/
│   │   ├── controllers/
│   │   ├── models/
│   │   ├── services/
│   │   │   ├── content-analyzer.js
│   │   │   ├── text-processor.js
│   │   │   └── ...
│   │   ├── utils/
│   │   └── app.js
│   ├── Dockerfile
│   └── package.json
│
├── generator-service/          # 文档生成服务
│   ├── src/
│   │   ├── config/
│   │   ├── controllers/
│   │   ├── models/
│   │   ├── services/
│   │   │   ├── ppt-generator.js
│   │   │   ├── word-generator.js
│   │   │   ├── template-manager.js
│   │   │   └── ...
│   │   ├── templates/         # 文档模板
│   │   ├── utils/
│   │   └── app.js
│   ├── Dockerfile
│   └── package.json
│
├── task-service/               # 任务管理服务
│   ├── src/
│   │   ├── config/
│   │   ├── controllers/
│   │   ├── models/
│   │   ├── services/
│   │   ├── utils/
│   │   └── app.js
│   ├── Dockerfile
│   └── package.json
│
├── shared/                     # 共享库和工具
│   ├── models/                # 共享数据模型
│   ├── utils/                 # 共享工具函数
│   ├── middlewares/           # 共享中间件
│   └── constants/             # 共享常量
│
└── config/                     # 共享配置
    ├── dev.js
    ├── prod.js
    └── test.js
```


## 4. Docker相关目录

```
docker/
├── nginx/                     # Nginx配置
│   ├── conf.d/
│   └── nginx.conf
├── mongodb/                   # MongoDB配置
│   └── init-mongo.js
├── postgres/                  # PostgreSQL配置 (如使用)
│   └── init.sql
├── redis/                     # Redis配置
│   └── redis.conf
├── minio/                     # MinIO配置 (文件存储)
│   └── config.json
└── docker-compose.dev.yml     # 开发环境docker-compose
```


## 5. 部署脚本目录

```
scripts/
├── setup/                     # 初始化安装脚本
│   ├── setup-dev.sh
│   └── setup-prod.sh
├── deploy/                    # 部署脚本
│   ├── deploy-frontend.sh
│   └── deploy-backend.sh
├── ci/                        # CI/CD脚本
│   ├── build.sh
│   └── test.sh
└── tools/                     # 工具脚本
    ├── backup-db.sh
    └── generate-api-docs.sh
```


## 6. 文档目录

```
docs/
├── api/                       # API文档
│   ├── auth.md
│   ├── documents.md
│   ├── ocr.md
│   └── generator.md
├── architecture/              # 架构文档
│   ├── system-overview.md
│   ├── data-model.md
│   └── deployment.md
├── guides/                    # 使用指南
│   ├── development-setup.md
│   ├── user-guide.md
│   └── admin-guide.md
└── images/                    # 文档图片
```

