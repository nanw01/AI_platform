from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import os
import logging
import time
from typing import List, Dict, Any, Optional

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 获取环境变量
MODEL_NAME = os.environ.get("MODEL_NAME", "model_a")
MODEL_PORT = int(os.environ.get("MODEL_PORT", 8001))

# 创建FastAPI应用
app = FastAPI(
    title=f"AI Model Service - {MODEL_NAME}",
    description=f"提供{MODEL_NAME}模型的推理服务，支持标准预测和OpenAI兼容格式",
    version="1.0.0",
)

# 模型信息
MODEL_INFO = {
    "name": "示例模型A",
    "description": "这是一个用于演示的AI模型服务A",
    "version": "1.0.0",
    "capabilities": ["text-generation", "completion"],
}

# 模型请求数据结构
class PredictionRequest(BaseModel):
    text: str
    parameters: Optional[Dict[str, Any]] = {}

# 预测响应数据结构
class PredictionResponse(BaseModel):
    result: str
    model: str
    processing_time: float

# 模拟推理函数
def predict_text(text: str, parameters: Dict[str, Any] = {}) -> str:
    """模拟模型推理，这里仅作为示例"""
    # 这里应该是实际的模型推理代码
    prefix = parameters.get("prefix", "Model A says: ")
    return f"{prefix}{text}"

# 标准RESTful API端点
@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """标准模型预测API"""
    try:
        # 进行模型推理
        result = predict_text(request.text, request.parameters)
        
        # 返回结果
        return PredictionResponse(
            result=result,
            model=MODEL_NAME,
            processing_time=0.1  # 模拟处理时间
        )
    except Exception as e:
        logger.error(f"预测过程出错: {str(e)}")
        raise HTTPException(status_code=500, detail="模型推理失败")

# OpenAI兼容的completions端点
@app.post("/openai/completions")
async def openai_completions(request: Request):
    """OpenAI兼容的completions API"""
    try:
        data = await request.json()
        prompt = data.get("prompt", "")
        max_tokens = data.get("max_tokens", 100)
        temperature = data.get("temperature", 0.7)
        
        # 模拟推理
        result = predict_text(prompt, {"temperature": temperature})
        
        # 构造OpenAI格式响应
        response = {
            "id": f"cmpl-{MODEL_NAME}-{id(request)}",
            "object": "text_completion",
            "created": int(time.time()),
            "model": MODEL_NAME,
            "choices": [
                {
                    "text": result,
                    "index": 0,
                    "logprobs": None,
                    "finish_reason": "length"
                }
            ],
            "usage": {
                "prompt_tokens": len(prompt.split()),
                "completion_tokens": len(result.split()),
                "total_tokens": len(prompt.split()) + len(result.split())
            }
        }
        return response
    except Exception as e:
        logger.error(f"OpenAI completions 出错: {str(e)}")
        raise HTTPException(status_code=500, detail="模型推理失败")

# OpenAI兼容的chat completions端点
@app.post("/openai/chat/completions")
async def openai_chat_completions(request: Request):
    """OpenAI兼容的chat completions API"""
    try:
        data = await request.json()
        messages = data.get("messages", [])
        temperature = data.get("temperature", 0.7)
        
        # 提取最后一条消息作为输入
        last_message = messages[-1]["content"] if messages else ""
        
        # 模拟推理
        result = predict_text(last_message, {"temperature": temperature})
        
        # 构造OpenAI格式响应
        response = {
            "id": f"chatcmpl-{MODEL_NAME}-{id(request)}",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": MODEL_NAME,
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": result
                    },
                    "finish_reason": "stop"
                }
            ],
            "usage": {
                "prompt_tokens": sum(len(m.get("content", "").split()) for m in messages),
                "completion_tokens": len(result.split()),
                "total_tokens": sum(len(m.get("content", "").split()) for m in messages) + len(result.split())
            }
        }
        return response
    except Exception as e:
        logger.error(f"OpenAI chat completions 出错: {str(e)}")
        raise HTTPException(status_code=500, detail="模型推理失败")

# 服务信息端点
@app.get("/info")
async def get_info():
    """获取模型服务信息"""
    return MODEL_INFO

# 健康检查
@app.get("/health")
async def health_check():
    """健康检查端点"""
    return {"status": "ok", "model": MODEL_NAME}

# 主函数
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=MODEL_PORT, reload=True) 