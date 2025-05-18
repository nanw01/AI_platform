from fastapi import FastAPI, Request
import os
import time

# 获取环境变量
MODEL_NAME = os.environ.get("MODEL_NAME", "model_b")
MODEL_PORT = int(os.environ.get("MODEL_PORT", 8002))

# 创建FastAPI应用
app = FastAPI(title=f"AI Model Service - {MODEL_NAME}")

# 模型信息
MODEL_INFO = {
    "name": "示例模型B",
    "description": "这是一个简单的示例模型B",
    "version": "1.0.0",
}

@app.post("/predict")
async def predict(request: Request):
    """最简单的预测实现"""
    data = await request.json()
    return {
        "result": f"Model B processed: {data.get('text', 'No input')}",
        "model": MODEL_NAME,
        "processing_time": 0.1
    }

@app.post("/openai/completions")
async def openai_completions(request: Request):
    """最小OpenAI completions实现"""
    data = await request.json()
    return {
        "id": f"cmpl-{MODEL_NAME}",
        "object": "text_completion",
        "created": int(time.time()),
        "model": MODEL_NAME,
        "choices": [{"text": f"Model B response to: {data.get('prompt', '')}", "index": 0}],
    }

@app.post("/openai/chat/completions")
async def openai_chat_completions(request: Request):
    """最小OpenAI chat completions实现"""
    return {
        "id": f"chatcmpl-{MODEL_NAME}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": MODEL_NAME,
        "choices": [{"message": {"role": "assistant", "content": "Hello from Model B!"}}],
    }

@app.get("/info")
async def get_info():
    """获取模型信息"""
    return MODEL_INFO

@app.get("/health")
async def health():
    """健康检查"""
    return {"status": "ok", "model": MODEL_NAME} 