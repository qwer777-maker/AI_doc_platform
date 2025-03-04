from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from typing import List
import uuid
from datetime import datetime
import os
from pydantic import ValidationError
import asyncio
from fastapi.responses import JSONResponse, StreamingResponse, FileResponse
import json
import logging
from fastapi.staticfiles import StaticFiles

from ..models.schemas import DocumentRequest, DocumentResponse, GenerationStatus
from ..services.deepseek_service import DeepSeekService
from ..services.ppt_generator import PPTGenerator
from ..services.word_generator import WordGenerator

router = APIRouter()
deepseek_service = DeepSeekService()

# 存储生成任务的状态
generation_tasks = {}

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 在 main.py 中添加静态文件挂载
# app.mount("/downloads", StaticFiles(directory="generated_docs"), name="downloads")
# app.mount("/previews", StaticFiles(directory="generated_docs"), name="previews")

@router.post("/documents/", response_model=DocumentResponse)
async def create_document(
    request: DocumentRequest, 
    background_tasks: BackgroundTasks
):
    """
    创建新的文档生成任务
    """
    # 确保 doc_type 是有效值
    if request.doc_type not in ["ppt", "word", "pdf"]:
        raise HTTPException(status_code=400, detail="Invalid document type")
    
    # 生成唯一ID
    doc_id = str(uuid.uuid4())
    
    # 创建初始响应
    response = DocumentResponse(
        id=doc_id,
        topic=request.topic,
        doc_type=request.doc_type,
        status="queued",
        created_at=datetime.now().isoformat()
    )
    
    # 存储任务状态
    generation_tasks[doc_id] = {
        "status": "queued",
        "progress": 0.0,
        "message": "任务已加入队列"
    }
    
    # 添加后台任务
    background_tasks.add_task(
        generate_document_background, 
        doc_id, 
        request.topic, 
        request.doc_type,
        request.additional_info,
        request.template_id
    )
    
    return response

@router.get("/documents/{doc_id}/status", response_model=GenerationStatus)
async def get_document_status(doc_id: str):
    """
    获取文档生成任务的状态
    """
    if doc_id not in generation_tasks:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    task_info = generation_tasks[doc_id]
    return GenerationStatus(
        id=doc_id,
        status=task_info["status"],
        progress=task_info["progress"],
        message=task_info.get("message")
    )

@router.get("/documents/{document_id}", response_model=DocumentResponse)
async def get_document(document_id: str):
    """
    获取生成的文档信息
    """
    print(f"Fetching document with ID: {document_id}")
    print(f"Available document IDs: {list(generation_tasks.keys())}")
    
    if document_id not in generation_tasks:
        # 返回更友好的错误信息
        return JSONResponse(
            status_code=404,
            content={"detail": f"文档不存在，可用的文档ID: {list(generation_tasks.keys())}"}
        )
    
    task_info = generation_tasks[document_id]
    
    if task_info["status"] != "completed":
        return DocumentResponse(
            id=document_id,
            topic=task_info.get("topic", "未知"),
            doc_type="ppt",  # 使用有效的默认值，而不是 "unknown"
            status=task_info["status"],
            created_at=datetime.now().isoformat()
        )
    
    # 确保 doc_type 是有效的枚举值
    doc_type = task_info.get("doc_type")
    if doc_type not in ["ppt", "word", "pdf"]:
        doc_type = "ppt"  # 设置默认值
    
    return DocumentResponse(
        id=document_id,
        topic=task_info.get("topic", "未知"),
        doc_type=doc_type,
        status=task_info["status"],
        download_url=task_info.get("download_url"),
        preview_url=task_info.get("preview_url"),
        created_at=task_info.get("created_at", datetime.now().isoformat())
    )

@router.get("/documents/{document_id}/stream")
async def stream_document_status(document_id: str):
    """
    使用 SSE 流式传输文档生成状态
    """
    if document_id not in generation_tasks:
        raise HTTPException(status_code=404, detail="文档不存在")
    
    async def event_generator():
        # 发送初始状态
        task_info = generation_tasks[document_id]
        yield f"data: {json.dumps(task_info)}\n\n"
        
        # 持续发送更新
        last_status = task_info.get("status")
        last_progress = task_info.get("progress", 0)
        
        while True:
            await asyncio.sleep(0.5)  # 更频繁地检查更新
            
            if document_id not in generation_tasks:
                yield f"data: {json.dumps({'error': '文档不存在'})}\n\n"
                break
            
            task_info = generation_tasks[document_id]
            current_status = task_info.get("status")
            current_progress = task_info.get("progress", 0)
            
            # 只在状态或进度变化时发送更新
            if (current_status != last_status or 
                abs(current_progress - last_progress) >= 0.01):  # 进度变化超过1%
                
                yield f"data: {json.dumps(task_info)}\n\n"
                
                last_status = current_status
                last_progress = current_progress
            
            # 如果任务已完成或失败，发送最终状态并结束流
            if current_status in ['completed', 'failed']:
                # 确保发送最终状态
                yield f"data: {json.dumps(task_info)}\n\n"
                break
    
    return StreamingResponse(
        event_generator(), 
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"  # 禁用 Nginx 缓冲
        }
    )

@router.get("/downloads/{file_name}")
async def download_file(file_name: str):
    """
    下载生成的文件
    """
    file_path = os.path.join("generated_docs", file_name)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="文件不存在")
    
    return FileResponse(
        path=file_path, 
        filename=file_name,
        media_type="application/octet-stream"
    )

@router.get("/previews/{file_name}")
async def preview_file(file_name: str):
    """
    预览生成的文件
    """
    file_path = os.path.join("generated_docs", file_name)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="文件不存在")
    
    # 根据文件类型设置适当的媒体类型
    media_type = "application/vnd.openxmlformats-officedocument.presentationml.presentation"
    if file_name.endswith(".docx"):
        media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    
    return FileResponse(
        path=file_path,
        media_type=media_type
    )

async def generate_document_background(
    doc_id: str, 
    topic: str, 
    doc_type: str,
    additional_info: str = None,
    template_id: str = None
):
    """
    后台文档生成任务，提供更细粒度的进度更新
    """
    try:
        # 初始状态
        generation_tasks[doc_id].update({
            "status": "processing",
            "progress": 0.05,
            "message": "正在准备生成...",
            "topic": topic,
            "doc_type": doc_type,
            "created_at": datetime.now().isoformat()
        })
        
        # 步骤1: 分析主题
        generation_tasks[doc_id].update({
            "progress": 0.1,
            "message": "正在分析主题..."
        })
        await asyncio.sleep(1)  # 给前端一些时间更新UI
        
        # 步骤2: 生成文档大纲
        generation_tasks[doc_id].update({
            "progress": 0.2,
            "message": "正在生成文档大纲..."
        })
        
        # 使用 try-except 块包装大纲生成
        try:
            outline = deepseek_service.generate_document_outline(topic, doc_type)
            if not outline:
                raise ValueError("生成大纲失败")
        except Exception as e:
            logger.error(f"生成大纲时出错: {str(e)}")
            generation_tasks[doc_id].update({
                "status": "failed",
                "message": "无法生成文档大纲，请检查主题是否合适或稍后重试"
            })
            return
        
        # 步骤3: 准备内容
        generation_tasks[doc_id].update({
            "progress": 0.4,
            "message": "大纲已生成，正在准备内容..."
        })
        await asyncio.sleep(1)  # 给前端一些时间更新UI
        
        # 步骤4: 创建文档
        generation_tasks[doc_id].update({
            "progress": 0.6,
            "message": "正在创建文档..."
        })
        
        # 根据文档类型选择生成器
        file_path = None
        try:
            if doc_type == "ppt":
                generator = PPTGenerator()
                file_path = generator.generate(topic, outline, template_id)
            elif doc_type == "word":
                generator = WordGenerator()
                file_path = generator.generate(topic, outline, template_id)
            else:
                raise ValueError(f"不支持的文档类型: {doc_type}")
            
            if not file_path:
                raise ValueError("文档生成失败")
        except Exception as e:
            logger.error(f"创建文档时出错: {str(e)}")
            generation_tasks[doc_id].update({
                "status": "failed",
                "message": f"文档生成失败: {str(e)}"
            })
            return
        
        # 步骤5: 完成格式化
        generation_tasks[doc_id].update({
            "progress": 0.8,
            "message": "正在完成格式化..."
        })
        await asyncio.sleep(1)  # 给前端一些时间更新UI
        
        # 文件生成成功，更新下载链接
        base_url = "http://localhost:8001"  # 应该从配置中获取
        download_url = f"{base_url}/downloads/{os.path.basename(file_path)}"
        preview_url = f"{base_url}/previews/{os.path.basename(file_path)}"
        
        # 完成
        generation_tasks[doc_id].update({
            "status": "completed",
            "progress": 1.0,
            "message": "文档生成完成",
            "download_url": download_url,
            "preview_url": preview_url
        })
        
    except Exception as e:
        logger.error(f"文档生成过程中出错: {str(e)}")
        generation_tasks[doc_id].update({
            "status": "failed",
            "message": f"生成过程中出错: {str(e)}"
        }) 