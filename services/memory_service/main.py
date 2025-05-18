from fastapi import FastAPI

app = FastAPI(title="Memory Service", version="1.0.0")

@app.get("/health")
async def health_check():
    return {"status": "ok", "service_name": "memory-service"}

# TODO: Add Memory specific endpoints, e.g., /store, /retrieve, /search 