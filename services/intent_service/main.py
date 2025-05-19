from fastapi import FastAPI, Request
import logging
from typing import Dict, List, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Intent Service", version="1.0.0")

@app.get("/health")
async def health_check():
    return {"status": "ok", "service_name": "intent-service"}

@app.post("/detect_intent")
async def detect_intent(request: Request):
    """检测用户文本中的意图"""
    payload = await request.json()
    text = payload.get("text", "")
    
    # 记录服务的处理状态
    logger.info(f"Intent服务开始处理文本: {text}")
    logger.info("Intent服务处理中...")
    
    # 简单的意图检测逻辑，实际项目中可以使用NLP模型
    intent = "unknown"
    confidence = 0.0
    
    # 模拟一些简单的意图匹配
    if "天气" in text or "温度" in text:
        intent = "查询天气"
        confidence = 0.95
    elif "时间" in text or "几点" in text:
        intent = "查询时间"
        confidence = 0.90
    elif "播放" in text or "音乐" in text or "歌曲" in text:
        intent = "播放音乐"
        confidence = 0.85
    elif "新闻" in text or "热点" in text:
        intent = "获取新闻"
        confidence = 0.80
    else:
        intent = "闲聊"
        confidence = 0.60
    
    logger.info("Intent服务处理完毕")
    
    return {
        "status": "success",
        "intent": intent,
        "confidence": confidence,
        "text": text,
        "entities": []  # 在实际应用中，这里可能包含识别出的实体
    }

@app.post("/function_call")
async def function_call(request: Request):
    """生成函数调用格式的意图"""
    payload = await request.json()
    text = payload.get("text", "")
    
    # 记录服务的处理状态
    logger.info(f"Intent服务开始处理函数调用: {text}")
    logger.info("Intent服务处理中...")
    
    # 模拟函数调用决策
    function_call = None
    
    if "天气" in text:
        function_call = {
            "name": "get_weather",
            "arguments": {
                "location": "北京",
                "unit": "celsius"
            }
        }
    elif "播放" in text and "音乐" in text:
        function_call = {
            "name": "play_music",
            "arguments": {
                "genre": "流行",
                "artist": "未指定"
            }
        }
    
    logger.info("Intent服务处理完毕")
    
    return {
        "status": "success",
        "function_call": function_call,
        "text": text
    }

# TODO: Add Intent specific endpoints, e.g., /detect_intent 