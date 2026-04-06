"""
示例：测试 OpenAI API 或兼容 API（如 Kimi、DeepSeek）
"""

import os
import sys
sys.path.insert(0, '/root/.cache/ai_Code')

from ai_test_suite import (
    TestRunner,
    OpenAIModel,
    ConsoleReporter,
    JSONReporter,
    MarkdownReporter,
    RuleBasedEvaluator,
)


def test_with_kimi():
    """使用 Kimi API 测试"""
    
    # 从环境变量获取 API key
    api_key = os.getenv("KIMI_API_KEY")
    if not api_key:
        print("请设置 KIMI_API_KEY 环境变量")
        return
    
    model = OpenAIModel(
        model_name="moonshot-v1-8k",
        api_key=api_key,
        base_url="https://api.moonshot.cn/v1",
    )
    
    runner = TestRunner(
        model=model,
        evaluator=RuleBasedEvaluator(),
        reporter=ConsoleReporter(verbose=True),
        temperature=0.7,
    )
    
    # 运行测试
    result = runner.run(
        categories=["logic", "language", "math"],  # 只测试这些类别
        limit=10,  # 最多10题
    )
    
    # 同时生成 JSON 和 Markdown 报告
    json_reporter = JSONReporter()
    json_reporter.report(result, "results/kimi_test_result.json")
    
    markdown_reporter = MarkdownReporter()
    markdown_reporter.report(result, "results/kimi_test_report.md")


def test_with_deepseek():
    """使用 DeepSeek API 测试"""
    
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        print("请设置 DEEPSEEK_API_KEY 环境变量")
        return
    
    model = OpenAIModel(
        model_name="deepseek-chat",
        api_key=api_key,
        base_url="https://api.deepseek.com/v1",
    )
    
    runner = TestRunner(model=model)
    result = runner.run_quick_test(num_questions=5)


def test_with_openai():
    """使用 OpenAI API 测试"""
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("请设置 OPENAI_API_KEY 环境变量")
        return
    
    model = OpenAIModel(
        model_name="gpt-4",
        api_key=api_key,
    )
    
    runner = TestRunner(model=model)
    result = runner.run()


def main():
    print("=" * 60)
    print("AI综合能力测试 - API 模型")
    print("=" * 60)
    print("\n支持的平台:")
    print("1. OpenAI (gpt-4, gpt-3.5-turbo)")
    print("2. Kimi/Moonshot (moonshot-v1-8k/32k/128k)")
    print("3. DeepSeek (deepseek-chat)")
    print("4. 其他兼容 OpenAI API 的服务")
    print("\n请设置对应的环境变量:")
    print("- OPENAI_API_KEY")
    print("- KIMI_API_KEY")  
    print("- DEEPSEEK_API_KEY")
    print("=" * 60)
    
    # 选择要测试的平台
    # test_with_kimi()
    # test_with_deepseek()
    # test_with_openai()


if __name__ == "__main__":
    main()
