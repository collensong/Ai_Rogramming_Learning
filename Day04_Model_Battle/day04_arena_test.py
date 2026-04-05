#!/usr/bin/env python3
"""
Day04 模型竞技场测试脚本
============================
本地运行多模型对比测试，评估不同参数规模的 LLM 在边缘设备上的表现。

支持的模型：
- Qwen2.5-0.5B-Instruct: 超轻量级，极速推理
- Qwen2.5-1.5B-Instruct: 平衡性能与质量
- Phi-2 (2.7B): 微软出品，英文能力强
- TinyLlama-1.1B: 小巧精悍

硬件要求：
- CPU: 建议 8 核以上（测试环境：Intel i9）
- 内存: 8GB+
- 磁盘: 4GB+ 用于存放模型文件
"""

from llama_cpp import Llama
import time
import os
import json
from datetime import datetime

# ============== 配置区域 ==============

# 模型配置
MODELS = {
    "Qwen0.5B": {
        "path": "/home/song/ai/edge_ai/qwen2.5-0.5b-instruct-q4_k_m.gguf",
        "desc": "极速 (62 tok/s)",
        "color": "\033[32m",  # 绿色
        "params": "0.5B"
    },
    "Qwen1.5B": {
        "path": "/home/song/ai/edge_ai/qwen2.5-1.5b-instruct-q4_k_m.gguf",
        "desc": "平衡 (25 tok/s)",
        "color": "\033[34m",  # 蓝色
        "params": "1.5B"
    },
    "Phi-2": {
        "path": "/home/song/ai/edge_ai/phi-2-q4.gguf",
        "desc": "微软出品 (英文强)",
        "color": "\033[33m",  # 黄色
        "params": "2.7B"
    },
    "TinyLlama": {
        "path": "/home/song/ai/edge_ai/tinyllama-1.1b-chat-q4.gguf",
        "desc": "小巧 (1.1B)",
        "color": "\033[35m",  # 紫色
        "params": "1.1B"
    }
}

RESET = "\033[0m"

# 测试题库
TEST_QUESTIONS = {
    "basic": [
        "什么是人工智能？",
        "用 Python 写个 Hello World 程序",
        "讲个程序员笑话",
    ],
    "logic": [
        "9.11 和 9.9 哪个大？",
        "逻辑题：如果我昨天是明天，那么今天就是周五。请问今天实际上是周几？",
    ],
    "code": [
        "写一个快速排序算法，用 Python",
        "解释什么是递归，并给出一个例子",
    ],
    "math": [
        "计算 23 × 47 = ?",
        "一个长方形长 10cm，宽 5cm，求面积",
    ]
}

# ============== 核心功能 ==============

def check_model_exists(path):
    """检查模型文件是否存在"""
    return os.path.exists(path)

def load_model(config, verbose=False):
    """加载模型"""
    return Llama(
        model_path=config["path"],
        n_threads=16,
        n_ctx=2048,
        verbose=verbose
    )

def generate_response(llm, question, max_tokens=200, temperature=0.7):
    """生成回复"""
    response = llm.create_chat_completion(
        messages=[{"role": "user", "content": question}],
        max_tokens=max_tokens,
        temperature=temperature
    )
    return response['choices'][0]['message']['content']

def benchmark_model(name, config, question, max_tokens=200):
    """
    对单个模型进行基准测试
    
    Returns:
        dict: 包含加载时间、生成时间、token 速度、回答内容的结果字典
    """
    result = {
        "model": name,
        "params": config["params"],
        "question": question,
        "success": False,
        "load_time": 0,
        "gen_time": 0,
        "tokens_per_sec": 0,
        "answer": "",
        "error": ""
    }
    
    print(f"{config['color']}🤖 [{name}] {config['desc']}{RESET}")
    
    if not check_model_exists(config["path"]):
        result["error"] = "模型文件不存在"
        print(f"   ❌ {result['error']}")
        return result
    
    try:
        # 加载模型
        t0 = time.time()
        llm = load_model(config)
        result["load_time"] = time.time() - t0
        
        # 生成回复
        t0 = time.time()
        answer = generate_response(llm, question, max_tokens)
        result["gen_time"] = time.time() - t0
        
        result["answer"] = answer
        result["tokens_per_sec"] = len(answer) / 2 / result["gen_time"]  # 粗略估算
        result["success"] = True
        
        print(f"   ✅ 加载: {result['load_time']:.2f}s | 生成: {result['gen_time']:.2f}s | 速度: {result['tokens_per_sec']:.1f} tok/s")
        print(f"   💬 {answer[:100]}...")
        
    except Exception as e:
        result["error"] = str(e)
        print(f"   ❌ 错误: {str(e)[:60]}")
    
    print()
    return result

def run_comparison(question=None, category="logic"):
    """
    运行模型对比测试
    
    Args:
        question: 自定义问题，为 None 时从题库选择
        category: 题库类别 (basic/logic/code/math)
    """
    if question is None:
        question = TEST_QUESTIONS[category][0]
    
    print("=" * 70)
    print("🚀 Day04 模型竞技场 - 本地 LLM 对比测试")
    print("=" * 70)
    print(f"📋 测试问题: {question}")
    print(f"📅 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    print()
    
    results = []
    for name, config in MODELS.items():
        result = benchmark_model(name, config, question)
        results.append(result)
        time.sleep(0.3)
    
    # 汇总结果
    print("=" * 70)
    print("📊 测试汇总")
    print("=" * 70)
    
    success_count = sum(1 for r in results if r["success"])
    print(f"✅ 成功: {success_count}/{len(results)} 个模型")
    
    for r in results:
        if r["success"]:
            print(f"   • {r['model']} ({r['params']}): {r['gen_time']:.2f}s, {r['tokens_per_sec']:.1f} tok/s")
    
    print("=" * 70)
    return results

def save_results(results, filename=None):
    """保存测试结果到 JSON 文件"""
    if filename is None:
        filename = f"arena_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 结果已保存到: {filename}")
    return filename

def interactive_mode():
    """交互式测试模式"""
    print("=" * 70)
    print("🎮 Day04 模型竞技场 - 交互式模式")
    print("=" * 70)
    print()
    print("可用模型:")
    for i, (name, config) in enumerate(MODELS.items(), 1):
        print(f"  {i}. {name} - {config['desc']}")
    print()
    
    # 选择模型
    while True:
        choice = input("选择模型 (1-4, 或输入 'all' 测试全部): ").strip()
        if choice.lower() == 'all':
            selected_models = list(MODELS.keys())
            break
        try:
            idx = int(choice) - 1
            selected_models = [list(MODELS.keys())[idx]]
            break
        except (ValueError, IndexError):
            print("无效选择，请重试")
    
    # 输入问题
    print()
    print("测试问题示例:")
    for cat, questions in TEST_QUESTIONS.items():
        print(f"  [{cat}] {questions[0][:40]}...")
    print()
    
    question = input("输入你的问题: ").strip()
    if not question:
        question = TEST_QUESTIONS["logic"][0]
    
    print()
    
    # 运行测试
    results = []
    for name in selected_models:
        config = MODELS[name]
        result = benchmark_model(name, config, question, max_tokens=300)
        results.append(result)
    
    # 保存结果
    save_results(results)
    
    return results

# ============== 主程序 ==============

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        # 交互式模式
        interactive_mode()
    elif len(sys.argv) > 1 and sys.argv[1] == "--test":
        # 快速测试模式
        test_types = ["logic", "code", "math"]
        for test_type in test_types:
            print(f"\n{'='*70}")
            print(f"🧪 运行 {test_type.upper()} 测试")
            print(f"{'='*70}\n")
            run_comparison(category=test_type)
    else:
        # 默认模式：逻辑题对比
        results = run_comparison(category="logic")
        save_results(results)
        print("\n🏆 对比完成！使用 --interactive 进入交互模式，--test 运行全面测试")
