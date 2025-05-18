from fastapi import FastAPI

app = FastAPI(title="TTS Service", version="1.0.0")

@app.get("/health")
async def health_check():
    return {"status": "ok", "service_name": "tts-service"}

# TODO: Add TTS specific endpoints, e.g., /synthesize 