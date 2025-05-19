from fastapi import FastAPI, HTTPException, Request, WebSocket, WebSocketDisconnect
import httpx
import os
import logging
import json
import asyncio
from typing import Dict, Any, List, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Orchestrator Service",
    description="Coordinates AI services for the platform.",
    version="1.0.0"
)

# Service URLs from environment variables
VAD_SERVICE_URL = os.getenv("VAD_SERVICE_URL", "http://vad-service:7001")
ASR_SERVICE_URL = os.getenv("ASR_SERVICE_URL", "http://asr-service:7002")
LLM_SERVICE_URL = os.getenv("LLM_SERVICE_URL", "http://llm-service:7003")
TTS_SERVICE_URL = os.getenv("TTS_SERVICE_URL", "http://tts-service:7004")
MEMORY_SERVICE_URL = os.getenv("MEMORY_SERVICE_URL", "http://memory-service:7005")
INTENT_SERVICE_URL = os.getenv("INTENT_SERVICE_URL", "http://intent-service:7006")

# WebSocket管理器
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

@app.get("/health")
async def health_check():
    return {
        "status": "ok", 
        "service_name": "orchestrator",
        "dependencies": {
            "vad_service": VAD_SERVICE_URL,
            "asr_service": ASR_SERVICE_URL,
            "llm_service": LLM_SERVICE_URL,
            "tts_service": TTS_SERVICE_URL,
            "memory_service": MEMORY_SERVICE_URL,
            "intent_service": INTENT_SERVICE_URL,
        }
    }

# WebSocket端点用于状态更新
@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket, client_id)
    try:
        while True:
            # 保持连接活跃
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(client_id)

# 完整的音频处理工作流
@app.post("/api/v1/process_audio")
async def process_audio_workflow(request: Request):
    logger.info("收到音频处理工作流请求.")
    
    try:
        # 获取音频数据和客户端ID
        audio_data = await request.body()
        client_id = request.headers.get("X-Client-ID", "unknown")
        logger.info(f"收到来自客户端 {client_id} 的 {len(audio_data)} 字节的音频数据")
        
        # 异步执行工作流，这样可以立即返回响应
        asyncio.create_task(
            execute_workflow_with_status(client_id, audio_data)
        )
        
        return {"status": "processing", "client_id": client_id}
    except Exception as e:
        logger.error(f"处理音频工作流时出错: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"服务器内部错误: {str(e)}")

# 实际执行工作流并发送状态更新
async def execute_workflow_with_status(client_id: str, audio_data: bytes):
    """执行音频处理工作流并通过WebSocket发送状态更新"""
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            # 通知开始处理工作流
            await manager.send_status(client_id, {
                "status": "start",
                "message": "开始处理音频工作流"
            })
            
            # 1. 调用VAD服务检测语音
            await manager.send_status(client_id, {
                "status": "service_start",
                "service": "vad",
                "message": "开始调用VAD服务检测语音活动"
            })
            
            vad_response = await client.post(
                f"{VAD_SERVICE_URL}/detect",
                content=audio_data
            )
            vad_response.raise_for_status()
            vad_result = vad_response.json()
            
            await manager.send_status(client_id, {
                "status": "service_success",
                "service": "vad",
                "message": "VAD服务处理完成",
                "result": vad_result
            })
            
            # 如果没有检测到语音，提前结束工作流
            if not vad_result.get("detected_speech", False):
                await manager.send_status(client_id, {
                    "status": "complete",
                    "message": "未检测到语音，工作流结束",
                    "result": {"error": "No speech detected"}
                })
                return
                
            # 2. 调用ASR服务进行语音识别
            await manager.send_status(client_id, {
                "status": "service_start",
                "service": "asr",
                "message": "开始调用ASR服务进行语音识别"
            })
            
            asr_response = await client.post(
                f"{ASR_SERVICE_URL}/recognize",
                content=audio_data
            )
            asr_response.raise_for_status()
            asr_result = asr_response.json()
            
            await manager.send_status(client_id, {
                "status": "service_success",
                "service": "asr",
                "message": "ASR服务处理完成",
                "result": asr_result
            })
            
            recognized_text = asr_result.get("text", "")
            
            # 3. 调用意图识别服务
            await manager.send_status(client_id, {
                "status": "service_start",
                "service": "intent",
                "message": "开始调用Intent服务进行意图识别"
            })
            
            intent_response = await client.post(
                f"{INTENT_SERVICE_URL}/detect_intent",
                json={"text": recognized_text}
            )
            intent_response.raise_for_status()
            intent_result = intent_response.json()
            
            await manager.send_status(client_id, {
                "status": "service_success",
                "service": "intent",
                "message": "Intent服务处理完成",
                "result": intent_result
            })
            
            # 4. 保存到记忆服务
            await manager.send_status(client_id, {
                "status": "service_start",
                "service": "memory",
                "message": "开始调用Memory服务存储对话"
            })
            
            memory_data = {
                "client_id": client_id,
                "text": recognized_text,
                "intent": intent_result.get("intent"),
                "type": "user_message"
            }
            
            memory_response = await client.post(
                f"{MEMORY_SERVICE_URL}/store",
                json=memory_data
            )
            memory_response.raise_for_status()
            memory_result = memory_response.json()
            
            await manager.send_status(client_id, {
                "status": "service_success",
                "service": "memory",
                "message": "Memory服务处理完成",
                "result": memory_result
            })
            
            # 5. 调用LLM服务生成回复
            await manager.send_status(client_id, {
                "status": "service_start",
                "service": "llm",
                "message": "开始调用LLM服务生成回复"
            })
            
            llm_payload = {
                "input": recognized_text,
                "context": {
                    "intent": intent_result.get("intent"),
                    "client_id": client_id
                }
            }
            
            llm_response = await client.post(
                f"{LLM_SERVICE_URL}/generate",
                json=llm_payload
            )
            llm_response.raise_for_status()
            llm_result = llm_response.json()
            
            await manager.send_status(client_id, {
                "status": "service_success",
                "service": "llm",
                "message": "LLM服务处理完成",
                "result": llm_result
            })
            
            llm_response_text = llm_result.get("response", "抱歉，我无法生成回复。")
            
            # 6. 将LLM回复保存到记忆
            await client.post(
                f"{MEMORY_SERVICE_URL}/store",
                json={
                    "client_id": client_id,
                    "text": llm_response_text,
                    "type": "assistant_message"
                }
            )
            
            # 7. 调用TTS服务生成语音
            await manager.send_status(client_id, {
                "status": "service_start",
                "service": "tts",
                "message": "开始调用TTS服务生成语音"
            })
            
            tts_payload = {
                "text": llm_response_text
            }
            
            tts_response = await client.post(
                f"{TTS_SERVICE_URL}/synthesize",
                json=tts_payload
            )
            tts_response.raise_for_status()
            tts_result = tts_response.json()
            
            await manager.send_status(client_id, {
                "status": "service_success",
                "service": "tts",
                "message": "TTS服务处理完成",
                "result": tts_result
            })
            
            # 8. 通知工作流处理完成
            final_result = {
                "recognized_text": recognized_text,
                "intent": intent_result.get("intent"),
                "response_text": llm_response_text,
                "audio_url": tts_result.get("audio_url")
            }
            
            await manager.send_status(client_id, {
                "status": "complete",
                "message": "工作流处理完成",
                "result": final_result
            })
            
        except httpx.HTTPStatusError as e:
            error_message = f"调用服务出错: {e.response.status_code} - {e.response.text}"
            logger.error(error_message)
            await manager.send_status(client_id, {
                "status": "error",
                "message": error_message
            })
        except Exception as e:
            error_message = f"工作流执行出错: {str(e)}"
            logger.error(error_message, exc_info=True)
            await manager.send_status(client_id, {
                "status": "error",
                "message": error_message
            })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7000, reload=True) 