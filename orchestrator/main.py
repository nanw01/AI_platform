from fastapi import FastAPI, HTTPException, Request
import httpx
import os
import logging

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

# Example workflow endpoint (to be expanded)
@app.post("/api/v1/process_audio")
async def process_audio_workflow(request: Request):
    logger.info("Received request for audio processing workflow.")
    # Placeholder: Actual workflow will call other services
    try:
        audio_data = await request.body() # Assuming raw audio data for now
        logger.info(f"Received audio data, size: {len(audio_data)} bytes")
        
        async with httpx.AsyncClient() as client:
            # 1. Call VAD (example)
            # response_vad = await client.post(f"{VAD_SERVICE_URL}/detect", content=audio_data, timeout=10.0)
            # response_vad.raise_for_status()
            # vad_results = response_vad.json()
            # logger.info(f"VAD results: {vad_results}")
            pass # Add more steps here
            
        return {"message": "Workflow started", "status": "processing"} # Simplified response
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error communicating with a service: {e.response.status_code} - {e.response.text}")
        raise HTTPException(status_code=e.response.status_code, detail=f"Error with service: {e.response.text}")
    except Exception as e:
        logger.error(f"Error in process_audio_workflow: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7000, reload=True) 