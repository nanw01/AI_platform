from abc import ABC, abstractmethod
from typing import Dict, List
import numpy as np

class BaseVADProvider(ABC):
    @abstractmethod
    def detect(self, audio_data: bytes) -> Dict:
        """
        检测音频中的语音活动
        Args:
            audio_data: 音频数据（字节格式）
        Returns:
            Dict: {
                "status": str,
                "speech_segments": List[Dict],
                "metadata": Dict
            }
        """
        pass

    @abstractmethod
    def get_supported_formats(self) -> List[str]:
        """获取支持的音频格式"""
        pass 