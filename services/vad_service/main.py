from fastapi import FastAPI

app = FastAPI(title="VAD Service", version="1.0.0")

@app.get("/health")
async def health_check():
    return {"status": "ok", "service_name": "vad-service"}

# TODO: Add VAD specific endpoints, e.g., /detect 