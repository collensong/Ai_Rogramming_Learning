"""
OpenAI API 模型接口
支持 OpenAI、Azure OpenAI 以及兼容的 API（如 kimi、deepseek 等）
"""

import os
import time
from typing import Optional, Dict, Any

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

from .base import ModelInterface, ModelResponse


class OpenAIModel(ModelInterface):
    """
    OpenAI API 模型封装
    
    支持:
    - OpenAI 官方 API (gpt-4, gpt-3.5-turbo 等)
    - 兼容 OpenAI API 格式的第三方服务
    
    Usage:
        # OpenAI 官方
        model = OpenAIModel("gpt-4", api_key="sk-...")
        
        # Kimi (Moonshot)
        model = OpenAIModel(
            "moonshot-v1-8k",
            api_key="...",
            base_url="https://api.moonshot.cn/v1"
        )
        
        # DeepSeek
        model = OpenAIModel(
            "deepseek-chat",
            api_key="...",
            base_url="https://api.deepseek.com/v1"
        )
    """
    
    def __init__(
        self,
        model_name: str,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: float = 60.0,
        **kwargs
    ):
        """
        初始化 OpenAI 模型
        
        Args:
            model_name: 模型名称，如 "gpt-4", "moonshot-v1-8k"
            api_key: API 密钥，默认从环境变量 OPENAI_API_KEY 读取
            base_url: API 基础 URL，用于第三方兼容服务
            timeout: 请求超时时间
        """
        super().__init__(model_name, **kwargs)
        
        if OpenAI is None:
            raise ImportError(
                "openai package not installed. "
                "Install with: pip install openai"
            )
        
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key not provided. "
                "Set OPENAI_API_KEY environment variable or pass api_key parameter."
            )
        
        self.base_url = base_url
        self.timeout = timeout
        
        # 初始化客户端
        client_kwargs = {"api_key": self.api_key, "timeout": timeout}
        if base_url:
            client_kwargs["base_url"] = base_url
            
        self.client = OpenAI(**client_kwargs)
    
    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
        **kwargs
    ) -> ModelResponse:
        """生成回答"""
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        start_time = time.time()
        
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )
            
            latency = time.time() - start_time
            
            result = ModelResponse(
                text=response.choices[0].message.content,
                model_name=self.model_name,
                latency=latency,
                tokens_input=response.usage.prompt_tokens if response.usage else 0,
                tokens_output=response.usage.completion_tokens if response.usage else 0,
                raw_response=response,
            )
            
            self.update_stats(result)
            return result
            
        except Exception as e:
            latency = time.time() - start_time
            raise RuntimeError(f"API call failed: {str(e)}") from e
    
    def chat(
        self,
        messages,
        temperature: float = 0.7,
        max_tokens: int = 2048,
        **kwargs
    ) -> ModelResponse:
        """对话模式"""
        
        start_time = time.time()
        
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )
            
            latency = time.time() - start_time
            
            result = ModelResponse(
                text=response.choices[0].message.content,
                model_name=self.model_name,
                latency=latency,
                tokens_input=response.usage.prompt_tokens if response.usage else 0,
                tokens_output=response.usage.completion_tokens if response.usage else 0,
                raw_response=response,
            )
            
            self.update_stats(result)
            return result
            
        except Exception as e:
            latency = time.time() - start_time
            raise RuntimeError(f"API call failed: {str(e)}") from e
