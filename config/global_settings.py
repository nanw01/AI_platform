import os

# General Settings
APP_NAME = "AI Platform"
DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

# Service URLs (can be overridden by docker-compose environments)
ORCHESTRATOR_URL = os.getenv("ORCHESTRATOR_URL", "http://orchestrator:7000")
VAD_SERVICE_URL = os.getenv("VAD_SERVICE_URL", "http://vad-service:7001")
ASR_SERVICE_URL = os.getenv("ASR_SERVICE_URL", "http://asr-service:7002")
LLM_SERVICE_URL = os.getenv("LLM_SERVICE_URL", "http://llm-service:7003")
TTS_SERVICE_URL = os.getenv("TTS_SERVICE_URL", "http://tts-service:7004")
MEMORY_SERVICE_URL = os.getenv("MEMORY_SERVICE_URL", "http://memory-service:7005")
INTENT_SERVICE_URL = os.getenv("INTENT_SERVICE_URL", "http://intent-service:7006")

# Redis Configuration
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))

# RabbitMQ Configuration
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", 5672))
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest") # Default user for RabbitMQ
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", "guest") # Default password

# Specific service configurations (examples)
class VADConfig:
    MODEL_PATH = os.getenv("VAD_MODEL_PATH", "/app/models/vad/silero_vad.onnx")
    # Add other VAD specific settings

class ASRConfig:
    DEFAULT_PROVIDER = os.getenv("ASR_PROVIDER", "funasr") # or "sherpa"
    FUNASR_MODEL_PATH = os.getenv("FUNASR_MODEL_PATH", "/app/models/asr/funasr_model")
    SHERPA_MODEL_PATH = os.getenv("SHERPA_MODEL_PATH", "/app/models/asr/sherpa_model")
    # Add other ASR specific settings

class LLMConfig:
    DEFAULT_PROVIDER = os.getenv("LLM_PROVIDER", "ollama") # "chatglm", "deepseek"
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434") # If Ollama runs separately or inside llm-service
    OLLAMA_DEFAULT_MODEL = os.getenv("OLLAMA_DEFAULT_MODEL", "llama3:latest")
    # Add other LLM specific settings

# You would typically load these into your services
# from config.global_settings import VADConfig, ASRConfig, LLMConfig, LOG_LEVEL
# import logging
# logging.basicConfig(level=LOG_LEVEL)
# current_vad_config = VADConfig() 