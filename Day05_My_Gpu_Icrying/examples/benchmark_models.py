"""
示例：多模型对比测试
"""

import sys
sys.path.insert(0, '/root/.cache/ai_Code')

from ai_test_suite import (
    TestRunner,
    HuggingFaceModel,
    OpenAIModel,
    DummyModel,
    ConsoleReporter,
    MarkdownReporter,
)


def benchmark_local_models():
    """对比多个本地模型"""
    
    # 定义要测试的模型
    models = [
        HuggingFaceModel("Qwen/Qwen2.5-0.5B-Instruct"),
        # HuggingFaceModel("microsoft/DialoGPT-medium"),
        # 添加更多模型...
    ]
    
    # 创建 runner（模型会在 benchmark 中被切换）
    runner = TestRunner(
        model=models[0],  # 临时模型
        reporter=ConsoleReporter(),
    )
    
    # 运行对比测试
    results = runner.benchmark(models, limit=5)
    
    # 生成详细报告
    for name, result in results.items():
        reporter = MarkdownReporter()
        reporter.report(result, f"results/benchmark_{name.replace('/', '_')}.md")


def benchmark_with_dummy():
    """使用虚拟模型测试框架功能"""
    
    # 创建不同能力水平的虚拟模型
    models = [
        DummyModel("low_capability", capability_level="low"),
        DummyModel("medium_capability", capability_level="medium"),
        DummyModel("high_capability", capability_level="high"),
    ]
    
    runner = TestRunner(model=models[0])
    results = runner.benchmark(models, limit=3)
    
    print("\n对比结果:")
    for name, result in results.items():
        print(f"{name}: {result.overall_percentage:.1f}%")


def main():
    print("=" * 60)
    print("AI模型对比测试")
    print("=" * 60)
    
    # 使用虚拟模型测试框架
    benchmark_with_dummy()
    
    # 或使用真实模型对比
    # benchmark_local_models()


if __name__ == "__main__":
    main()
