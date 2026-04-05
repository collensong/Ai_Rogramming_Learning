#!/usr/bin/env python3
"""
Day04 TinyLlama 简单 API 封装
=============================
提供便捷的聊天接口，支持单轮和多轮对话。

使用示例:
    from chat_api import chat, chat_with_history
    
    # 单轮对话
    reply = chat("你好，请介绍一下自己")
    print(reply)
    
    # 多轮对话
    session = ChatSession()
    print(session.chat("你好"))
    print(session.chat("刚才我说了什么？"))  # 记住上下文
"""

from llama_cpp import Llama
import time

# ============== 配置 ==============
MODEL_PATH = "/home/song/ai/edge_ai/tinyllama-1.1b-chat-q4.gguf"
DEFAULT_CONFIG = {
    "n_threads": 8,
    "n_ctx": 2048,  # 使用模型最大上下文长度
    "verbose": False
}
GENERATION_CONFIG = {
    "temperature": 0.6,
    "max_tokens": 512,
    "top_p": 0.9,
    "stop": ["</s>", "Human:", "Assistant:", "User:"]
}

# ============== 全局模型实例（懒加载）==============
_llm_instance = None

def get_llm():
    """获取或创建 LLM 实例（单例模式）"""
    global _llm_instance
    if _llm_instance is None:
        print("🔄 正在加载 TinyLlama 模型...")
        start = time.time()
        _llm_instance = Llama(
            model_path=MODEL_PATH,
            **DEFAULT_CONFIG
        )
        print(f"✅ 模型加载完成！耗时 {time.time()-start:.2f}s\n")
    return _llm_instance

def reset_llm():
    """重置模型实例（释放内存后重新加载）"""
    global _llm_instance
    _llm_instance = None
    print("🔄 模型已重置")

# ============== 核心 API ==============

def chat(message, temperature=None, max_tokens=None):
    """
    单轮对话 API
    
    Args:
        message: 用户输入的消息
        temperature: 温度参数（默认 0.6）
        max_tokens: 最大生成 token 数（默认 512）
    
    Returns:
        str: 模型的回复内容
    
    Example:
        >>> reply = chat("什么是人工智能？")
        >>> print(reply)
    """
    llm = get_llm()
    
    config = GENERATION_CONFIG.copy()
    if temperature is not None:
        config["temperature"] = temperature
    if max_tokens is not None:
        config["max_tokens"] = max_tokens
    
    response = llm.create_chat_completion(
        messages=[{"role": "user", "content": message}],
        **config
    )
    
    return response['choices'][0]['message']['content']

def chat_with_history(messages, temperature=None, max_tokens=None):
    """
    带历史记录的多轮对话 API
    
    Args:
        messages: 消息列表，格式为 [{"role": "user"/"assistant", "content": "..."}, ...]
        temperature: 温度参数
        max_tokens: 最大生成 token 数
    
    Returns:
        str: 模型的回复内容
    
    Example:
        >>> messages = [
        ...     {"role": "user", "content": "你好"},
        ...     {"role": "assistant", "content": "你好！很高兴见到你。"},
        ...     {"role": "user", "content": "刚才我说了什么？"}
        ... ]
        >>> reply = chat_with_history(messages)
    """
    llm = get_llm()
    
    config = GENERATION_CONFIG.copy()
    if temperature is not None:
        config["temperature"] = temperature
    if max_tokens is not None:
        config["max_tokens"] = max_tokens
    
    response = llm.create_chat_completion(
        messages=messages,
        **config
    )
    
    return response['choices'][0]['message']['content']

# ============== 对话会话类 ==============

class ChatSession:
    """
    对话会话类，自动维护历史记录
    
    Example:
        >>> session = ChatSession()
        >>> print(session.chat("你好"))
        >>> print(session.chat("北京今天天气怎么样？"))  # 记住上下文
        >>> print(session.history)  # 查看完整历史
        >>> session.clear()  # 清空历史
    """
    
    def __init__(self, system_prompt=None):
        """
        初始化会话
        
        Args:
            system_prompt: 可选的系统提示词，用于设定助手角色
        """
        self.history = []
        if system_prompt:
            self.history.append({"role": "system", "content": system_prompt})
    
    def chat(self, message, temperature=None, max_tokens=None):
        """
        发送消息并获取回复
        
        Args:
            message: 用户消息
            temperature: 可选的温度参数
            max_tokens: 可选的最大 token 数
        
        Returns:
            str: 助手回复
        """
        # 添加用户消息
        self.history.append({"role": "user", "content": message})
        
        # 获取回复
        reply = chat_with_history(self.history, temperature, max_tokens)
        
        # 添加助手回复到历史
        self.history.append({"role": "assistant", "content": reply})
        
        # 简单的上下文长度管理：保留最近 10 轮对话
        if len(self.history) > 20:  # 10 轮 = 20 条消息
            # 如果有 system prompt，保留它
            if self.history[0].get("role") == "system":
                self.history = [self.history[0]] + self.history[-18:]
            else:
                self.history = self.history[-20:]
        
        return reply
    
    def clear(self):
        """清空对话历史"""
        # 保留 system prompt（如果有）
        if self.history and self.history[0].get("role") == "system":
            system_msg = self.history[0]
            self.history = [system_msg]
        else:
            self.history = []
        print("🗑️  对话历史已清空")
    
    def set_system_prompt(self, prompt):
        """设置/修改系统提示词"""
        # 移除旧的 system 消息
        self.history = [m for m in self.history if m.get("role") != "system"]
        # 插入新的 system prompt
        self.history.insert(0, {"role": "system", "content": prompt})
    
    def get_history_text(self):
        """获取格式化的历史对话文本"""
        lines = []
        for msg in self.history:
            role = msg.get("role", "unknown")
            content = msg.get("content", "")
            if role == "user":
                lines.append(f"👤 用户: {content}")
            elif role == "assistant":
                lines.append(f"🤖 助手: {content}")
            elif role == "system":
                lines.append(f"⚙️  系统: {content}")
        return "\n".join(lines)

# ============== 命令行交互模式 ==============

def interactive_chat():
    """命令行交互式聊天"""
    print("=" * 60)
    print("🤖 TinyLlama 聊天机器人")
    print("=" * 60)
    print("命令: /quit 退出, /clear 清空历史, /history 查看历史\n")
    
    session = ChatSession()
    
    while True:
        try:
            user_input = input("👤 你: ").strip()
            
            if not user_input:
                continue
            
            if user_input == "/quit":
                print("👋 再见！")
                break
            
            if user_input == "/clear":
                session.clear()
                continue
            
            if user_input == "/history":
                print("\n📜 对话历史:")
                print(session.get_history_text())
                print()
                continue
            
            # 获取回复
            print("🤖 助手: ", end="", flush=True)
            reply = session.chat(user_input)
            print(reply)
            print()
            
        except KeyboardInterrupt:
            print("\n👋 再见！")
            break
        except Exception as e:
            print(f"❌ 错误: {e}\n")

# ============== 主程序 ==============

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # 命令行直接提问模式
        question = " ".join(sys.argv[1:])
        print(f"👤 问题: {question}\n")
        print(f"🤖 回答: {chat(question)}")
    else:
        # 交互式模式
        interactive_chat()
