from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from uuid import UUID, uuid4
import datetime

class HealthResponse(BaseModel):
    status: str = "ok"
    service_name: str
    version: str = "1.0.0"

class ErrorDetail(BaseModel):
    code: str
    message: str

class ErrorResponse(BaseModel):
    request_id: UUID = Field(default_factory=uuid4)
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    error: ErrorDetail

# Example: ASR Service Schemas
class ASRRequest(BaseModel):
    audio_bytes: bytes # Or a URL, or a file path depending on design
    language: Optional[str] = "en-US"
    # Other ASR parameters

class ASRTranscriptSegment(BaseModel):
    text: str
    start_time: float
    end_time: float
    confidence: Optional[float] = None

class ASRResponse(BaseModel):
    request_id: UUID = Field(default_factory=uuid4)
    transcript: str
    language: str
    segments: Optional[List[ASRTranscriptSegment]] = None
    metadata: Optional[Dict[str, Any]] = None

# Add more shared schemas for other services (LLM, TTS, VAD, Intent, Memory) 