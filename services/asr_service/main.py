from fastapi import FastAPI

app = FastAPI(title="ASR Service", version="1.0.0")

@app.get("/health")
async def health_check():
    return {"status": "ok", "service_name": "asr-service"}

# TODO: Add ASR specific endpoints, e.g., /recognize 