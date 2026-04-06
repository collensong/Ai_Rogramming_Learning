"""
快速开始脚本 - 最简单的使用示例
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from ai_test_suite import (
    TestRunner,
    DummyModel,
    ConsoleReporter,
)


def quick_demo():
    """演示：使用虚拟模型快速测试框架"""
    
    print("🚀 AI综合能力测试 - 快速演示")
    print("=" * 50)
    
    # 1. 创建虚拟模型（无需下载，立即测试）
    model = DummyModel(
        model_name="demo_model",
        capability_level="high",  # 模拟高能力回答
    )
    
    # 2. 创建测试运行器
    runner = TestRunner(
        model=model,
        reporter=ConsoleReporter(verbose=True),
    )
    
    # 3. 运行测试（3道随机题目）
    print("\n正在运行快速测试（3道题目）...\n")
    result = runner.run_quick_test(num_questions=3)
    
    print("\n✅ 测试完成！")
    return result


def test_hf_model():
    """使用真实 HuggingFace 模型测试"""
    
    from ai_test_suite import HuggingFaceModel
    
    print("🚀 AI综合能力测试 - HuggingFace模型")
    print("=" * 50)
    
    # 加载一个小型模型
    model = HuggingFaceModel(
        model_name="Qwen/Qwen2.5-0.5B-Instruct",
        device="auto",
    )
    
    runner = TestRunner(model=model)
    
    # 运行5道随机题目
    result = runner.run_quick_test(num_questions=5)
    
    return result


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--real":
        # 使用真实模型
        test_hf_model()
    else:
        # 使用虚拟模型演示
        quick_demo()
