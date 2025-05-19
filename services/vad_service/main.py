from fastapi import FastAPI, Request
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="VAD Service", version="1.0.0")

@app.get("/health")
async def health_check():
    return {"status": "ok", "service_name": "vad-service"}

@app.post("/detect")
async def detect_voice(request: Request):
    """检测音频中的语音活动"""
    audio_data = await request.body()
    
    # 记录服务的处理状态
    logger.info(f"VAD服务开始处理 {len(audio_data)} 字节的音频数据")
    logger.info("VAD服务处理中...")
    logger.info("VAD服务处理完毕")
    
    # 这里只是模拟处理，返回一个固定的结果
    return {
        "status": "success",
        "detected_speech": True,
        "speech_segments": [{"start": 0.0, "end": 2.5}, {"start": 3.2, "end": 5.8}]
    }

# TODO: Add VAD specific endpoints, e.g., /detect 