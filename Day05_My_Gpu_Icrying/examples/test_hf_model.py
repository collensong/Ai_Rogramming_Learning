"""
示例：测试本地 HuggingFace 模型
"""

import sys
sys.path.insert(0, '/root/.cache/ai_Code')

from ai_test_suite import (
    TestRunner,
    HuggingFaceModel,
    ConsoleReporter,
    RuleBasedEvaluator,
)


def main():
    """测试本地模型示例"""
    
    # 1. 加载模型
    print("=" * 60)
    print("AI综合能力测试 - HuggingFace模型")
    print("=" * 60)
    
    # 使用一个小型模型进行快速测试
    model = HuggingFaceModel(
        model_name="Qwen/Qwen2.5-0.5B-Instruct",  # 可以换成其他模型
        device="auto",  # 自动选择设备
        # load_in_8bit=True,  # 如果显存不足可以启用量化
    )
    
    # 2. 创建测试运行器
    runner = TestRunner(
        model=model,
        evaluator=RuleBasedEvaluator(),
        reporter=ConsoleReporter(verbose=True, use_color=True),
        temperature=0.7,
        max_tokens=1024,
    )
    
    # 3. 运行快速测试（随机5题）
    print("\n开始快速测试...")
    result = runner.run_quick_test(num_questions=5)
    
    # 4. 也可以运行完整测试
    # result = runner.run()
    
    # 5. 或按类别测试
    # result = runner.run_category_test("logic", num_questions=3)
    
    print("\n测试完成!")


if __name__ == "__main__":
    main()
