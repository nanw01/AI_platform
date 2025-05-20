import torch
import torchaudio
import numpy as np
import soundfile as sf
from io import BytesIO
from typing import Dict, List, Tuple
from ..base import BaseVADProvider

class SileroVADProvider(BaseVADProvider):
    def __init__(self):
        self.model = torch.hub.load(
            repo_or_dir='snakers4/silero-vad',
            model='silero_vad',
            force_reload=True
        )
        self.sample_rate = 16000
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = self.model.to(self.device)

    def detect(self, audio_data: bytes) -> Dict:
        """
        使用 Silero VAD 检测语音活动
        """
        try:
            # 1. 加载音频
            waveform = self._load_audio(audio_data)
            
            # 2. 检测语音
            speech_timestamps = self.model(
                waveform,
                self.sample_rate,
                min_speech_duration_ms=500,    # 最小语音片段时长
                min_silence_duration_ms=300,   # 最小静音时长
                threshold=0.5                  # 检测阈值
            )
            
            # 3. 处理结果
            segments = []
            for start, end in speech_timestamps:
                segments.append({
                    "start_time": start / 1000,  # 转换为秒
                    "end_time": end / 1000,
                    "duration": (end - start) / 1000,
                    "confidence": 0.95  # Silero 不直接提供置信度
                })
            
            # 4. 计算元数据
            total_duration = len(waveform) / self.sample_rate
            speech_duration = sum(s["duration"] for s in segments)
            
            return {
                "status": "success",
                "speech_segments": segments,
                "metadata": {
                    "total_duration": total_duration,
                    "speech_ratio": speech_duration / total_duration if total_duration > 0 else 0,
                    "num_segments": len(segments)
                }
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "speech_segments": [],
                "metadata": {}
            }

    def _load_audio(self, audio_data: bytes) -> torch.Tensor:
        """
        加载音频数据
        """
        # 使用 soundfile 读取音频数据
        with BytesIO(audio_data) as audio_buffer:
            audio, sample_rate = sf.read(audio_buffer)
            
            # 转换为单声道
            if len(audio.shape) > 1:
                audio = audio.mean(axis=1)
            
            # 重采样到目标采样率
            if sample_rate != self.sample_rate:
                audio = torchaudio.transforms.Resample(
                    sample_rate, self.sample_rate
                )(torch.from_numpy(audio))
            else:
                audio = torch.from_numpy(audio)
            
            return audio.to(self.device)

    def get_supported_formats(self) -> List[str]:
        """获取支持的音频格式"""
        return ['.wav', '.flac', '.ogg'] 