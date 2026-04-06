"""
虚拟模型 - 用于测试框架本身
"""

import time
import random
from typing import Optional
from .base import ModelInterface, ModelResponse


class DummyModel(ModelInterface):
    """
    虚拟模型，用于测试框架功能
    
    可以配置为返回固定回答或模拟不同能力水平
    
    Usage:
        # 固定回答
        model = DummyModel("dummy", responses={"hello": "world"})
        
        # 模拟不同能力水平
        model = DummyModel("dummy", capability_level="high")  # low/medium/high
    """
    
    def __init__(
        self,
        model_name: str = "dummy",
        responses: Optional[dict] = None,
        capability_level: str = "medium",
        delay: float = 0.1,
        **kwargs
    ):
        """
        初始化虚拟模型
        
        Args:
            model_name: 模型名称
            responses: 预定义的回答字典 {关键词: 回答}
            capability_level: 模拟的能力水平 (low/medium/high)
            delay: 模拟延迟（秒）
        """
        super().__init__(model_name, **kwargs)
        self.responses = responses or {}
        self.capability_level = capability_level
        self.delay = delay
        
        # 根据能力水平预设回答模板
        self.templates = {
            "low": [
                "我不太确定...",
                "这个问题有点难",
                "我需要更多信息",
            ],
            "medium": [
                "这是一个有趣的问题。",
                "让我思考一下...",
                "根据我的理解...",
            ],
            "high": [
                "这是一个深入的问题，我会详细分析...",
                "从多个角度来看...",
                "让我提供一个全面的回答...",
            ],
        }
    
    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
        **kwargs
    ) -> ModelResponse:
        """生成回答"""
        
        start_time = time.time()
        
        # 检查预定义回答
        for keyword, response in self.responses.items():
            if keyword.lower() in prompt.lower():
                time.sleep(self.delay)
                result = ModelResponse(
                    text=response,
                    model_name=self.model_name,
                    latency=time.time() - start_time,
                    tokens_input=len(prompt) // 4,
                    tokens_output=len(response) // 4,
                )
                self.update_stats(result)
                return result
        
        # 根据能力水平生成默认回答
        templates = self.templates.get(self.capability_level, self.templates["medium"])
        base_response = random.choice(templates)
        
        # 添加一些与问题相关的内容（简单模仿）
        response = f"{base_response}\n\n关于'{prompt[:50]}...'的问题，"
        
        if self.capability_level == "high":
            response += "我会从多个角度进行详细分析..."
        elif self.capability_level == "medium":
            response += "我认为这取决于具体情况。"
        else:
            response += "我不太确定答案。"
        
        time.sleep(self.delay)
        
        result = ModelResponse(
            text=response,
            model_name=self.model_name,
            latency=time.time() - start_time,
            tokens_input=len(prompt) // 4,
            tokens_output=len(response) // 4,
        )
        
        self.update_stats(result)
        return result
