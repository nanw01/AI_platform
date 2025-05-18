from fastapi import FastAPI

app = FastAPI(title="LLM Service", version="1.0.0")

@app.get("/health")
async def health_check():
    return {"status": "ok", "service_name": "llm-service"}

# TODO: Add LLM specific endpoints, e.g., /generate or /chat/completions 