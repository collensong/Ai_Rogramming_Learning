#!/usr/bin/env python3
"""
四模型对比测试 - I9 专属
"""
from llama_cpp import Llama
import time

# 模型配置 - 专注 TinyLlama 单模型优化
MODELS = {
    "TinyLlama": {
        "path": "/home/song/ai/edge_ai/tinyllama-1.1b-chat-q4.gguf",
        "desc": "小巧精悍 (1.1B)",
        "color": "\033[35m"  # 紫色
    }
}

# 优化参数
N_THREADS = 8   # 根据 CPU 调整，8 线程通常足够
N_CTX = 1024    # 降低以节省内存，可提升至 2048 如果需要
RESET = "\033[0m"

def test_model(name, config, question):
    """测试单个模型"""
    print(f"{config['color']}")
    print(f"🤖 [{name}] {config['desc']}")
    print(f"   文件: {config['path']}")
    print(f"   问题: {question[:30]}...")
    
    if not os.path.exists(config['path']):
        print(f"   ❌ 文件不存在，跳过{RESET}")
        return
    
    try:
        # 加载（计时）
        t0 = time.time()
        llm = Llama(
            model_path=config['path'],
            n_threads=16,
            n_ctx=2048,
            verbose=False
        )
        load_time = time.time() - t0
        
        # 生成（计时）
        t0 = time.time()
        response = llm.create_chat_completion(
            messages=[{"role": "user", "content": question}],
            max_tokens=150,
            temperature=0.7
        )
        gen_time = time.time() - t0
        
        answer = response['choices'][0]['message']['content']
        tokens = len(answer) // 2  # 粗略估算
        
        print(f"   ✅ 加载: {load_time:.2f}s | 生成: {gen_time:.2f}s | 速度: {tokens/gen_time:.1f} tok/s")
        print(f"   💬 回答: {answer[:80]}...")
        
    except Exception as e:
        print(f"   ❌ 错误: {str(e)[:50]}{RESET}")
    
    print(RESET)
    time.sleep(0.5)

if __name__ == "__main__":
    import os
    
    print("🚀 I9 四模型大乱斗")
    print("=" * 60)
    
    # 测试问题（选一个）
    TEST_QUESTIONS = [
        "什么是人工智能？",
        "9.11 和 9.9 哪个大？",
        "用Python写个hello world",
        "讲个笑话"
    ]
    
    # 用第一个问题测试所有模型
    question = "9.11 和 9.9 哪个大？"
    print(f"统一问题: {question}")
    print("=" * 60)
    
    for name, config in MODELS.items():
        test_model(name, config, question)
        print()
    
    print("🏆 对比完成！哪个模型最对你的胃口？")
