#!/usr/bin/env python3
"""
逻辑谜题测试：如果我昨天是明天，那么今天就是周五。请问今天实际上是周几？
"""
from llama_cpp import Llama
import os

# 正确的逻辑分析
print("🧮 先分析一下正确的逻辑：\n")

print("设今天是 X")
print("昨天 = X-1")
print("明天 = X+1")
print()

print('"如果我昨天是明天" 有两种理解方式：')
print()

print("方式A：我的昨天变成了别人的明天")
print("  - 如果 X-1 是某人的明天")
print("  - 那么某人今天是 X-2")
print("  - 如果某人的今天是周五")
print("  - 那么 X-2 = 周五 → X = 周日")
print()

print("方式B：我的明天变成了别人的昨天")
print("  - 如果 X+1 是某人的昨天")
print("  - 那么某人今天是 X+2")
print("  - 如果某人的今天是周五")
print("  - 那么 X+2 = 周五 → X = 周三")
print()

print("=" * 60)
print("现在测试各个模型的回答...\n")

MODELS = {
    "Qwen0.5B": "/home/song/ai/edge_ai/qwen2.5-0.5b-instruct-q4_k_m.gguf",
    "Qwen1.5B": "/home/song/ai/edge_ai/qwen2.5-1.5b-instruct-q4_k_m.gguf",
    "Phi-2": "/home/song/ai/edge_ai/phi-2-q4.gguf",
    "TinyLlama": "/home/song/ai/edge_ai/tinyllama-1.1b-chat-q4.gguf"
}

QUESTION = "逻辑题：如果我昨天是明天，那么今天就是周五。请问今天实际上是周几？请详细说明推理过程。"

for name, path in MODELS.items():
    print(f"🤖 [{name}]")
    if not os.path.exists(path):
        print(f"   ❌ 模型不存在\n")
        continue
    
    try:
        llm = Llama(
            model_path=path,
            n_threads=16,
            n_ctx=2048,
            verbose=False
        )
        
        response = llm.create_chat_completion(
            messages=[{"role": "user", "content": QUESTION}],
            max_tokens=300,
            temperature=0.5
        )
        
        answer = response['choices'][0]['message']['content']
        print(f"   💬 {answer[:200]}...")
        
        # 检查答案中是否包含"周日"或"周三"
        if "周日" in answer or "星期天" in answer or "星期日" in answer:
            print("   ✅ 提到周日（可能是正确答案）")
        elif "周三" in answer or "星期三" in answer:
            print("   ✅ 提到周三（可能是正确答案）")
        else:
            print("   ⚠️ 未明确给出答案")
            
    except Exception as e:
        print(f"   ❌ 错误: {str(e)[:50]}")
    
    print()

print("=" * 60)
print("正确答案：周日 或 周三（取决于理解方式）")
