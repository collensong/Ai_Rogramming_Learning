"""
模型接口模块 - 统一不同AI模型的调用方式
"""

from .base import ModelInterface, ModelResponse
from .openai_model import OpenAIModel
from .huggingface_model import HuggingFaceModel
from .dummy_model import DummyModel

__all__ = [
    "ModelInterface",
    "ModelResponse",
    "OpenAIModel",
    "HuggingFaceModel",
    "DummyModel",
]
