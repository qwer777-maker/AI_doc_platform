from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from .api.routes import router as api_router
from .core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该限制为前端域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载API路由
app.include_router(api_router, prefix=settings.API_V1_STR)

# 创建下载和预览目录
os.makedirs("generated_docs", exist_ok=True)

# 挂载静态文件服务
app.mount("/downloads", StaticFiles(directory="generated_docs"), name="downloads")
app.mount("/previews", StaticFiles(directory="generated_docs"), name="previews")

@app.get("/")
def read_root():
    return {"message": "Welcome to AI Doc Platform API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8001, reload=True) 