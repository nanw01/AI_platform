from fastapi import FastAPI, Request
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Memory Service", version="1.0.0")

# 内存中的简单存储，实际应用中会使用Redis或数据库
memory_store = {}

@app.get("/health")
async def health_check():
    return {"status": "ok", "service_name": "memory-service"}

@app.post("/store")
async def store_memory(request: Request):
    """存储记忆数据"""
    payload = await request.json()
    
    # 记录服务的处理状态
    logger.info(f"Memory服务开始存储数据: {payload}")
    logger.info("Memory服务处理中...")
    
    # 简单实现，为内存项添加时间戳和ID
    memory_id = f"mem_{len(memory_store) + 1}"
    timestamp = datetime.now().isoformat()
    
    memory_item = {
        **payload,
        "timestamp": timestamp,
        "id": memory_id
    }
    
    memory_store[memory_id] = memory_item
    logger.info("Memory服务处理完毕")
    
    return {
        "status": "success",
        "memory_id": memory_id,
        "timestamp": timestamp
    }

@app.post("/retrieve")
async def retrieve_memory(request: Request):
    """检索记忆数据"""
    payload = await request.json()
    memory_id = payload.get("memory_id")
    
    # 记录服务的处理状态
    logger.info(f"Memory服务开始检索数据: {memory_id}")
    logger.info("Memory服务处理中...")
    
    if memory_id in memory_store:
        result = memory_store[memory_id]
        logger.info("Memory服务处理完毕，找到记忆")
        return {
            "status": "success",
            "memory": result
        }
    else:
        logger.info("Memory服务处理完毕，未找到记忆")
        return {
            "status": "not_found",
            "message": f"Memory ID {memory_id} not found"
        }

@app.post("/search")
async def search_memory(request: Request):
    """搜索记忆数据"""
    payload = await request.json()
    query = payload.get("query", "")
    
    # 记录服务的处理状态
    logger.info(f"Memory服务开始搜索数据: {query}")
    logger.info("Memory服务处理中...")
    
    # 简单实现，只返回最新的几条记忆
    results = list(memory_store.values())[-5:]
    
    logger.info("Memory服务处理完毕")
    
    return {
        "status": "success",
        "results": results
    }

# TODO: Add Memory specific endpoints, e.g., /store, /retrieve, /search 