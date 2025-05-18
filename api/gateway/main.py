from fastapi import FastAPI, Request, Response, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os
import json
import logging
from typing import Dict, Any, Optional, List

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建FastAPI应用
app = FastAPI(
    title="AI Platform API Gateway",
    description="一个支持RESTful和OpenAI兼容格式的AI服务平台",
    version="1.0.0",
)

# 添加CORS支持
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 服务地址配置
MODEL_SERVICES = {
    "model_a": os.environ.get("MODEL_A_URL", "http://model-a:8001"),
    "model_b": os.environ.get("MODEL_B_URL", "http://model-b:8002"),
}

# 异步HTTP客户端
http_client = httpx.AsyncClient()

# 辅助函数：根据模型名称确定服务URL
def get_model_url(model_name: str) -> str:
    """根据模型名称确定对应的服务URL"""
    if model_name in MODEL_SERVICES:
        return MODEL_SERVICES[model_name]
    raise HTTPException(status_code=404, detail=f"模型 '{model_name}' 不存在")

# RESTful API路由
@app.post("/api/v1/{model_name}/predict")
async def predict(model_name: str, request: Request):
    """RESTful风格的模型推理API"""
    model_url = get_model_url(model_name)
    payload = await request.json()
    
    try:
        response = await http_client.post(
            f"{model_url}/predict",
            json=payload,
            timeout=60.0
        )
        return Response(
            content=response.content,
            status_code=response.status_code,
            media_type=response.headers.get("content-type", "application/json")
        )
    except httpx.RequestError as e:
        logger.error(f"请求模型服务出错: {str(e)}")
        raise HTTPException(status_code=503, detail="模型服务暂时不可用")

# OpenAI兼容API路由
@app.post("/v1/completions")
async def openai_completions(request: Request):
    """OpenAI兼容的completions API"""
    payload = await request.json()
    model = payload.get("model", "model_a")  # 默认使用model_a
    
    # 将OpenAI格式转换为内部格式
    internal_payload = {
        "prompt": payload.get("prompt", ""),
        "max_tokens": payload.get("max_tokens", 100),
        "temperature": payload.get("temperature", 0.7),
    }
    
    model_url = get_model_url(model)
    
    try:
        response = await http_client.post(
            f"{model_url}/openai/completions",
            json=internal_payload,
            timeout=60.0
        )
        return Response(
            content=response.content,
            status_code=response.status_code,
            media_type=response.headers.get("content-type", "application/json")
        )
    except httpx.RequestError as e:
        logger.error(f"请求OpenAI兼容服务出错: {str(e)}")
        raise HTTPException(status_code=503, detail="模型服务暂时不可用")

@app.post("/v1/chat/completions")
async def openai_chat_completions(request: Request):
    """OpenAI兼容的chat completions API"""
    payload = await request.json()
    model = payload.get("model", "model_a")  # 默认使用model_a
    
    model_url = get_model_url(model)
    
    try:
        response = await http_client.post(
            f"{model_url}/openai/chat/completions",
            json=payload,
            timeout=60.0
        )
        return Response(
            content=response.content,
            status_code=response.status_code,
            media_type=response.headers.get("content-type", "application/json")
        )
    except httpx.RequestError as e:
        logger.error(f"请求OpenAI兼容服务出错: {str(e)}")
        raise HTTPException(status_code=503, detail="模型服务暂时不可用")

# 健康检查
@app.get("/health")
async def health_check():
    """API网关健康检查"""
    return {"status": "ok", "services": MODEL_SERVICES}

# 获取可用模型列表
@app.get("/api/v1/models")
async def list_models():
    """获取所有可用模型列表"""
    models = []
    
    for model_name, model_url in MODEL_SERVICES.items():
        try:
            response = await http_client.get(f"{model_url}/info")
            if response.status_code == 200:
                model_info = response.json()
                models.append({
                    "id": model_name,
                    "name": model_info.get("name", model_name),
                    "status": "available",
                    "description": model_info.get("description", "")
                })
            else:
                models.append({
                    "id": model_name,
                    "name": model_name,
                    "status": "unavailable"
                })
        except httpx.RequestError:
            models.append({
                "id": model_name,
                "name": model_name,
                "status": "error"
            })
    
    return {"models": models}

# 应用启动和关闭事件
@app.on_event("startup")
async def startup():
    """应用启动时的初始化操作"""
    logger.info("API网关服务启动中...")

@app.on_event("shutdown")
async def shutdown():
    """应用关闭时的清理操作"""
    await http_client.aclose()
    logger.info("API网关服务已关闭") 