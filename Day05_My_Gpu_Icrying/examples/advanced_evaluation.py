"""
示例：高级评分方法 - 使用LLM作为评判
"""

import os
import sys
sys.path.insert(0, '/root/.cache/ai_Code')

from ai_test_suite import (
    TestRunner,
    OpenAIModel,
    HuggingFaceModel,
    LLMBasedEvaluator,
    RuleBasedEvaluator,
    ConsoleReporter,
)


def evaluate_with_llm_judge():
    """使用更强的LLM作为评判"""
    
    # 1. 创建被测模型（可以是较弱的模型）
    test_model = HuggingFaceModel("Qwen/Qwen2.5-0.5B-Instruct")
    
    # 2. 创建评判模型（需要更强的模型）
    judge_api_key = os.getenv("OPENAI_API_KEY") or os.getenv("KIMI_API_KEY")
    if not judge_api_key:
        print("请设置 API key 用于评判模型")
        return
    
    # 使用 OpenAI 或 Kimi 作为评判
    judge_model = OpenAIModel(
        model_name="gpt-4",  # 或 "moonshot-v1-8k"
        api_key=judge_api_key,
        # base_url="..."  # 如果使用第三方API
    )
    
    # 3. 创建基于LLM的评分器
    llm_evaluator = LLMBasedEvaluator(
        judge_model=judge_model,
        temperature=0.1,  # 低温度保证一致性
    )
    
    # 4. 运行测试
    runner = TestRunner(
        model=test_model,
        evaluator=llm_evaluator,
        reporter=ConsoleReporter(verbose=True),
    )
    
    result = runner.run_quick_test(num_questions=3)
    
    return result


def hybrid_evaluation():
    """混合评分：规则评分 + LLM评分"""
    
    # 先用规则评分快速筛选
    # 对高分回答再用LLM详细评估
    
    print("混合评分策略:")
    print("1. 规则评分快速初筛")
    print("2. LLM评分精细评估（针对开放性题目）")
    print("3. 综合两种评分结果")
    
    # 实际实现可以自定义 Evaluator 子类
    pass


def main():
    print("=" * 60)
    print("高级评分方法示例")
    print("=" * 60)
    
    # 使用LLM作为评判
    # evaluate_with_llm_judge()
    
    print("\n提示：使用LLM评判可以获得更准确的开放性题目评分")
    print("但需要消耗额外的API调用和token")


if __name__ == "__main__":
    main()
