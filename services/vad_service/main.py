from fastapi import FastAPI, UploadFile, File, Request
from providers.silero.silero import SileroVADProvider
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="VAD Service", version="1.0.0")

# Initialize VAD provider
vad_provider = SileroVADProvider()

@app.get("/health")
async def health_check():
    return {"status": "ok", "service_name": "vad-service"}

@app.post("/v1/detect")
async def detect_voice(request: Request):
    """检测音频中的语音活动"""
    try:
        audio_data = await request.body()
        
        # 记录服务的处理状态
        logger.info(f"VAD服务开始处理 {len(audio_data)} 字节的音频数据")
        
        # 使用 SileroVAD 处理音频
        result = vad_provider.detect(audio_data)
        
        logger.info(f"VAD服务处理完毕，检测到 {len(result['speech_segments'])} 个语音片段")
        return result
        
    except Exception as e:
        logger.error(f"VAD服务处理失败: {str(e)}")
        return {
            "status": "error",
            "error": str(e)
        }

# TODO: Add VAD specific endpoints, e.g., /detect 