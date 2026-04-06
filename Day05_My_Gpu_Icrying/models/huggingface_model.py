"""
Hugging Face Transformers 本地模型接口
支持加载本地或 HuggingFace Hub 上的模型
"""

import time
import torch
from typing import Optional, Dict, Any

try:
    from transformers import AutoModelForCausalLM, AutoTokenizer
except ImportError:
    AutoModelForCausalLM = None
    AutoTokenizer = None

from .base import ModelInterface, ModelResponse


class HuggingFaceModel(ModelInterface):
    """
    HuggingFace Transformers 模型封装
    
    支持本地加载或从 Hub 下载模型
    
    Usage:
        # 加载小型模型（适合测试）
        model = HuggingFaceModel("Qwen/Qwen2.5-0.5B-Instruct")
        
        # 指定设备
        model = HuggingFaceModel(
            "meta-llama/Llama-2-7b-chat-hf",
            device="cuda",
            load_in_8bit=True  # 量化加载节省显存
        )
    """
    
    def __init__(
        self,
        model_name: str,
        device: Optional[str] = None,
        torch_dtype: Optional[Any] = None,
        load_in_8bit: bool = False,
        load_in_4bit: bool = False,
        trust_remote_code: bool = True,
        cache_dir: Optional[str] = None,
        **kwargs
    ):
        """
        初始化 HuggingFace 模型
        
        Args:
            model_name: 模型名称或本地路径
            device: 运行设备 ('cuda', 'cpu', 'auto')
            torch_dtype: 数据类型 (torch.float16, torch.bfloat16, etc.)
            load_in_8bit: 是否使用 8bit 量化
            load_in_4bit: 是否使用 4bit 量化
            trust_remote_code: 是否信任远程代码
            cache_dir: 模型缓存目录
        """
        super().__init__(model_name, **kwargs)
        
        if AutoModelForCausalLM is None:
            raise ImportError(
                "transformers not installed. "
                "Install with: pip install transformers torch"
            )
        
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.torch_dtype = torch_dtype
        
        print(f"正在加载模型 {model_name}...")
        
        # 加载tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            trust_remote_code=trust_remote_code,
            cache_dir=cache_dir
        )
        
        # 设置pad_token
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        
        # 加载模型
        model_kwargs = {
            "trust_remote_code": trust_remote_code,
            "cache_dir": cache_dir,
        }
        
        if device == "auto":
            model_kwargs["device_map"] = "auto"
        
        if torch_dtype:
            model_kwargs["torch_dtype"] = torch_dtype
            
        if load_in_8bit:
            model_kwargs["load_in_8bit"] = True
        elif load_in_4bit:
            model_kwargs["load_in_4bit"] = True
        
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            **model_kwargs
        )
        
        if device != "auto":
            self.model = self.model.to(self.device)
        
        self.model.eval()
        print(f"模型加载完成，使用设备: {self.device}")
    
    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
        top_p: float = 0.9,
        repetition_penalty: float = 1.0,
        **kwargs
    ) -> ModelResponse:
        """生成回答"""
        
        # 构建消息
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        # 应用chat template
        if hasattr(self.tokenizer, "apply_chat_template"):
            text = self.tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True
            )
        else:
            # 简单拼接
            text = ""
            if system_prompt:
                text += f"System: {system_prompt}\n\n"
            text += f"User: {prompt}\nAssistant:"
        
        # 编码输入
        model_inputs = self.tokenizer(
            [text],
            return_tensors="pt",
            padding=True
        ).to(self.model.device)
        
        input_tokens = model_inputs.input_ids.shape[1]
        
        # 生成参数
        generate_kwargs = {
            "max_new_tokens": max_tokens,
            "do_sample": temperature > 0,
            "temperature": temperature if temperature > 0 else 1.0,
            "top_p": top_p,
            "repetition_penalty": repetition_penalty,
            "pad_token_id": self.tokenizer.pad_token_id,
            "eos_token_id": self.tokenizer.eos_token_id,
        }
        
        # 温度=0时使用贪婪解码
        if temperature == 0:
            generate_kwargs["do_sample"] = False
        
        generate_kwargs.update(kwargs)
        
        start_time = time.time()
        
        with torch.no_grad():
            output = self.model.generate(**model_inputs, **generate_kwargs)
        
        latency = time.time() - start_time
        
        # 解码输出（只取新生成的部分）
        generated_tokens = output[0][input_tokens:]
        response_text = self.tokenizer.decode(
            generated_tokens,
            skip_special_tokens=True
        )
        
        output_tokens = len(generated_tokens)
        
        result = ModelResponse(
            text=response_text.strip(),
            model_name=self.model_name,
            latency=latency,
            tokens_input=input_tokens,
            tokens_output=output_tokens,
            raw_response=output,
        )
        
        self.update_stats(result)
        return result
