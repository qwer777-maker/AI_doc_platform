# AI 文档生成器

一个基于 AI 的文档生成系统，可以根据用户提供的主题自动生成 PPT 和 Word 文档。

## 功能特点

- 根据主题自动生成文档大纲
- 支持 PPT 和 Word 文档格式
- 实时显示生成进度
- 支持文档下载和预览
- 使用 Server-Sent Events (SSE) 实现实时进度更新

## 技术栈

### 前端
- Vue.js
- Vuex
- Vue Router
- Axios

### 后端
- FastAPI
- Python-docx (Word 文档生成)
- Python-pptx (PPT 生成)
- DeepSeek API (AI 内容生成)

## 安装与运行

### 前端

```bash
cd frontend
npm install
npm run serve
```

### 后端

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

## 环境变量

创建一个 `.env` 文件在后端目录中：

```
AI_API_KEY=your_deepseek_api_key
AI_API_ENDPOINT=https://api.deepseek.com/v1/chat/completions
SECRET_KEY=your-secret-key-for-jwt
```

## 使用 Docker

```bash
docker-compose up -d
```

## 贡献指南

1. Fork 该仓库
2. 创建您的特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交您的更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 打开一个 Pull Request

## 许可证

[MIT](LICENSE)