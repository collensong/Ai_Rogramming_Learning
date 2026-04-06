"""
模型接口基类 - 定义统一的模型调用规范
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Dict, Any, List
import time


@dataclass
class ModelResponse:
    """统一模型响应格式"""
    text: str
    model_name: str
    latency: float  # 响应时间（秒）
    tokens_input: int = 0
    tokens_output: int = 0
    raw_response: Optional[Any] = None
    metadata: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class ModelInterface(ABC):
    """
    AI模型接口抽象基类
    
    所有具体模型实现都应继承此类，确保统一的调用方式
    """
    
    def __init__(self, model_name: str, **kwargs):
        self.model_name = model_name
        self.config = kwargs
        self.stats = {
            "total_calls": 0,
            "total_latency": 0.0,
            "total_tokens_input": 0,
            "total_tokens_output": 0,
        }
    
    @abstractmethod
    def generate(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
        **kwargs
    ) -> ModelResponse:
        """
        生成回答
        
        Args:
            prompt: 用户问题
            system_prompt: 系统提示词
            temperature: 温度参数（创造性 vs 确定性）
            max_tokens: 最大生成token数
            **kwargs: 其他模型特定参数
            
        Returns:
            ModelResponse: 统一格式的响应
        """
        pass
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2048,
        **kwargs
    ) -> ModelResponse:
        """
        对话模式（默认使用generate实现，子类可覆盖）
        
        Args:
            messages: 消息列表，格式 [{"role": "user/system", "content": "..."}]
            temperature: 温度参数
            max_tokens: 最大生成token数
            **kwargs: 其他参数
        """
        # 默认实现：提取最后一条用户消息
        last_user_msg = None
        system_prompt = None
        
        for msg in messages:
            if msg.get("role") == "system":
                system_prompt = msg.get("content")
            elif msg.get("role") == "user":
                last_user_msg = msg.get("content")
        
        if last_user_msg is None:
            raise ValueError("No user message found in messages")
            
        return self.generate(
            prompt=last_user_msg,
            system_prompt=system_prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )
    
    def update_stats(self, response: ModelResponse):
        """更新调用统计"""
        self.stats["total_calls"] += 1
        self.stats["total_latency"] += response.latency
        self.stats["total_tokens_input"] += response.tokens_input
        self.stats["total_tokens_output"] += response.tokens_output
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        stats = self.stats.copy()
        if stats["total_calls"] > 0:
            stats["avg_latency"] = stats["total_latency"] / stats["total_calls"]
        else:
            stats["avg_latency"] = 0.0
        return stats
    
    def reset_stats(self):
        """重置统计信息"""
        self.stats = {
            "total_calls": 0,
            "total_latency": 0.0,
            "total_tokens_input": 0,
            "total_tokens_output": 0,
        }
