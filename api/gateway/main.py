from fastapi import FastAPI, Request, Response, HTTPException, Depends, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import httpx
import os
import json
import logging
import uuid
import asyncio
from typing import Dict, Any, Optional, List
from tenacity import retry, stop_after_attempt, wait_exponential, RetryError

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
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
ORCHESTRATOR_URL = os.environ.get("ORCHESTRATOR_URL", "http://orchestrator:7000")
SERVICE_URLS = {
    "vad": os.environ.get("VAD_SERVICE_URL", "http://vad-service:7001"),
    "asr": os.environ.get("ASR_SERVICE_URL", "http://asr-service:7002"),
    "llm": os.environ.get("LLM_SERVICE_URL", "http://llm-service:7003"),
    "tts": os.environ.get("TTS_SERVICE_URL", "http://tts-service:7004"),
    "memory": os.environ.get("MEMORY_SERVICE_URL", "http://memory-service:7005"),
    "intent": os.environ.get("INTENT_SERVICE_URL", "http://intent-service:7006"),
}

# 异步HTTP客户端
http_client = httpx.AsyncClient(timeout=60.0)  # 增加默认超时时间

# 重试装饰器
@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
async def call_service_with_retry(client, url, **kwargs):
    """带重试功能的服务调用"""
    try:
        logger.info(f"正在调用服务: {url}")
        response = await client.post(url, **kwargs)
        response.raise_for_status()
        return response
    except httpx.HTTPStatusError as e:
        logger.error(f"服务调用失败: {url}, 状态码: {e.response.status_code}, 错误: {e.response.text}")
        raise
    except httpx.RequestError as e:
        logger.error(f"请求错误: {url}, 错误: {str(e)}")
        raise

# WebSocket连接管理
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket
        logger.info(f"WebSocket client connected: {client_id}")

    def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]
            logger.info(f"WebSocket client disconnected: {client_id}")

    async def send_status(self, client_id: str, status: dict):
        if client_id in self.active_connections:
            await self.active_connections[client_id].send_json(status)
            logger.debug(f"Sent status to client {client_id}: {status}")

manager = ConnectionManager()

# 辅助函数：根据服务名称确定服务URL
def get_service_url(service_name: str) -> str:
    """根据服务名称确定对应的服务URL"""
    if service_name in SERVICE_URLS:
        return SERVICE_URLS[service_name]
    raise HTTPException(status_code=404, detail=f"服务 '{service_name}' 不存在")

# 挂载静态文件目录
app.mount("/static", StaticFiles(directory="static"), name="static")

# 提供主页
@app.get("/")
async def get_index():
    return FileResponse("static/index.html")

# WebSocket端点
@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket, client_id)
    try:
        while True:
            # 保持连接活跃
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(client_id)

# RESTful API路由
@app.post("/api/v1/{service_name}/process")
async def process(service_name: str, request: Request):
    """RESTful风格的服务处理API"""
    service_url = get_service_url(service_name)
    payload = await request.json()
    
    try:
        response = await call_service_with_retry(
            http_client,
            f"{service_url}/process",
            json=payload
        )
        return Response(
            content=response.content,
            status_code=response.status_code,
            media_type=response.headers.get("content-type", "application/json")
        )
    except (httpx.RequestError, RetryError) as e:
        logger.error(f"请求服务出错: {str(e)}")
        raise HTTPException(status_code=503, detail="服务暂时不可用")

# 音频处理API
@app.post("/api/v1/process_audio")
async def process_audio(request: Request):
    """处理音频数据并通过WebSocket返回状态更新"""
    # 获取音频数据
    audio_data = await request.body()
    client_id = request.headers.get("X-Client-ID", str(uuid.uuid4()))
    
    logger.info(f"接收到客户端 {client_id} 的音频数据，大小: {len(audio_data)} 字节")
    
    # 创建工作流实例
    payload = {
        "client_id": client_id
    }
    
    # 异步执行工作流，这样可以立即返回响应
    asyncio.create_task(
        execute_workflow_with_status(client_id, "process_audio", payload, audio_data)
    )
    
    return {"status": "processing", "client_id": client_id}

# 工作流状态跟踪
async def execute_workflow_with_status(client_id: str, workflow_name: str, payload: dict, audio_data=None):
    """将工作流请求转发到编排服务并通过WebSocket发送状态更新"""
    try:
        # 通知开始处理工作流
        await manager.send_status(client_id, {
            "status": "start",
            "message": f"开始处理工作流 {workflow_name}"
        })
        
        # 根据工作流名称转发到不同的编排服务端点
        if workflow_name == "process_audio" and audio_data:
            # 转发音频数据到编排服务
            async with httpx.AsyncClient(timeout=90.0) as client:  # 增加超时时间
                try:
                    orchestrator_response = await call_service_with_retry(
                        client,
                        f"{ORCHESTRATOR_URL}/api/v1/process_audio",
                        content=audio_data,
                        headers={"X-Client-ID": client_id}
                    )
                    logger.info(f"成功调用编排服务，状态码: {orchestrator_response.status_code}")
                except Exception as e:
                    logger.error(f"调用编排服务失败: {str(e)}")
                    raise
        else:
            # 对于其他类型的工作流，可以在这里添加处理逻辑
            await manager.send_status(client_id, {
                "status": "error",
                "message": f"未知的工作流类型: {workflow_name}"
            })
    except Exception as e:
        logger.error(f"工作流执行错误: {str(e)}", exc_info=True)
        # 通知错误
        await manager.send_status(client_id, {
            "status": "error",
            "message": f"处理错误: {str(e)}"
        })

# OpenAI兼容API路由
@app.post("/v1/completions")
async def openai_completions(request: Request):
    """OpenAI兼容的completions API"""
    payload = await request.json()
    
    # 转发到LLM服务
    try:
        response = await http_client.post(
            f"{SERVICE_URLS['llm']}/v1/completions",
            json=payload,
            timeout=60.0
        )
        return Response(
            content=response.content,
            status_code=response.status_code,
            media_type=response.headers.get("content-type", "application/json")
        )
    except httpx.RequestError as e:
        logger.error(f"请求LLM服务出错: {str(e)}")
        raise HTTPException(status_code=503, detail="LLM服务暂时不可用")

@app.post("/v1/chat/completions")
async def openai_chat_completions(request: Request):
    """OpenAI兼容的chat completions API"""
    payload = await request.json()
    
    # 转发到LLM服务
    try:
        response = await http_client.post(
            f"{SERVICE_URLS['llm']}/v1/chat/completions",
            json=payload,
            timeout=60.0
        )
        return Response(
            content=response.content,
            status_code=response.status_code,
            media_type=response.headers.get("content-type", "application/json")
        )
    except httpx.RequestError as e:
        logger.error(f"请求LLM服务出错: {str(e)}")
        raise HTTPException(status_code=503, detail="LLM服务暂时不可用")

# 健康检查
@app.get("/health")
async def health_check():
    """API网关健康检查"""
    return {"status": "ok", "services": SERVICE_URLS}

# 获取可用服务列表
@app.get("/api/v1/services")
async def list_services():
    """获取所有可用服务列表"""
    services = []
    
    for service_name, service_url in SERVICE_URLS.items():
        try:
            response = await http_client.get(f"{service_url}/health")
            if response.status_code == 200:
                service_info = response.json()
                services.append({
                    "id": service_name,
                    "name": service_info.get("service_name", service_name),
                    "status": "available",
                    "description": service_info.get("description", "")
                })
            else:
                services.append({
                    "id": service_name,
                    "name": service_name,
                    "status": "unavailable"
                })
        except httpx.RequestError:
            services.append({
                "id": service_name,
                "name": service_name,
                "status": "error"
            })
    
    return {"services": services}

# 工作流API
@app.post("/api/v1/workflows/{workflow_name}")
async def execute_workflow(workflow_name: str, request: Request):
    """执行指定工作流"""
    payload = await request.json()
    client_id = request.headers.get("X-Client-ID", str(uuid.uuid4()))
    payload["client_id"] = client_id
    
    try:
        response = await http_client.post(
            f"{ORCHESTRATOR_URL}/api/v1/{workflow_name}",
            json=payload,
            timeout=120.0
        )
        return Response(
            content=response.content,
            status_code=response.status_code,
            media_type=response.headers.get("content-type", "application/json")
        )
    except httpx.RequestError as e:
        logger.error(f"请求编排服务出错: {str(e)}")
        raise HTTPException(status_code=503, detail="编排服务暂时不可用")

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