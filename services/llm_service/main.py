from fastapi import FastAPI, Request
import logging
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="LLM Service", version="1.0.0")

@app.get("/health")
async def health_check():
    return {"status": "ok", "service_name": "llm-service"}

@app.post("/generate")
async def generate_text(request: Request):
    """根据输入生成文本响应"""
    payload = await request.json()
    
    # 记录服务的处理状态
    logger.info(f"LLM服务开始处理请求: {payload}")
    logger.info("LLM服务处理中...")
    logger.info("LLM服务处理完毕")
    
    # 这里只是模拟处理，返回一个固定的结果
    input_text = payload.get("input", "")
    return {
        "status": "success",
        "response": f"这是对'{input_text}'的LLM响应示例。",
        "model": "mock-model"
    }

@app.post("/v1/chat/completions")
async def chat_completions(request: Request):
    """OpenAI兼容的chat接口"""
    payload = await request.json()
    
    # 记录服务的处理状态
    logger.info(f"LLM服务开始处理聊天请求")
    logger.info("LLM服务处理中...")
    logger.info("LLM服务处理完毕")
    
    # 这里只是模拟处理，返回一个OpenAI格式的结果
    return {
        "id": "chatcmpl-mock-123",
        "object": "chat.completion",
        "created": 1677858242,
        "model": "mock-model",
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": "这是来自模拟LLM的响应示例。"
                },
                "finish_reason": "stop"
            }
        ],
        "usage": {
            "prompt_tokens": 10,
            "completion_tokens": 10,
            "total_tokens": 20
        }
    }

# TODO: Add LLM specific endpoints, e.g., /generate or /chat/completions 