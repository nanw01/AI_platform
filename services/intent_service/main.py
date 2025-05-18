from fastapi import FastAPI

app = FastAPI(title="Intent Service", version="1.0.0")

@app.get("/health")
async def health_check():
    return {"status": "ok", "service_name": "intent-service"}

# TODO: Add Intent specific endpoints, e.g., /detect_intent 