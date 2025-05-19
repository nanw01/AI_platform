from fastapi import FastAPI, Request
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="ASR Service", version="1.0.0")

@app.get("/health")
async def health_check():
    return {"status": "ok", "service_name": "asr-service"}

@app.post("/recognize")
async def recognize_speech(request: Request):
    """将音频转换为文本"""
    audio_data = await request.body()
    
    # 记录服务的处理状态
    logger.info(f"ASR服务开始处理 {len(audio_data)} 字节的音频数据")
    logger.info("ASR服务处理中...")
    logger.info("ASR服务处理完毕")
    
    # 这里只是模拟处理，返回一个固定的结果
    return {
        "status": "success",
        "text": "这是从音频中识别出的示例文本。",
        "confidence": 0.95
    }

# TODO: Add ASR specific endpoints, e.g., /recognize 