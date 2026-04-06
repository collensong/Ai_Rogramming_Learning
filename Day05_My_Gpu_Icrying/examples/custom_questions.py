"""
示例：添加自定义题目
"""

import sys
sys.path.insert(0, '/root/.cache/ai_Code')

from ai_test_suite import (
    TestRunner,
    DummyModel,
    Question,
    QuestionBank,
    QuestionCategory,
    DifficultyLevel,
)


def create_custom_questions():
    """创建自定义题目"""
    
    questions = [
        Question(
            id="CUSTOM_001",
            category=QuestionCategory.LOGIC,
            difficulty=DifficultyLevel.MEDIUM,
            title="自定义逻辑题",
            content="如果所有的A都是B，所有的B都是C，那么所有的A都是C吗？",
            answer="是的，这是三段论推理的传递性。",
            keywords=["是", "传递性", "三段论", "所有"],
            score=10,
        ),
        
        Question(
            id="CUSTOM_002",
            category=QuestionCategory.LANGUAGE,
            difficulty=DifficultyLevel.HARD,
            title="自定义语言理解题",
            content="请解释'画蛇添足'的含义，并造一个句子。",
            answer="画蛇添足：做多余的事反而坏事。",
            keywords=["多余", "坏事", "过度", "不必要"],
            score=10,
        ),
    ]
    
    return questions


def test_with_custom_questions():
    """使用自定义题目测试"""
    
    # 1. 创建题目库并添加自定义题目
    bank = QuestionBank()
    bank.add_many(create_custom_questions())
    
    # 2. 也可以从文件加载
    # bank.load_from_json("my_questions.json")
    
    # 3. 保存题目到文件
    # bank.save_to_json("output/questions_backup.json")
    
    # 4. 创建测试运行器
    model = DummyModel("test", capability_level="high")
    
    runner = TestRunner(
        model=model,
        question_bank=bank,
    )
    
    # 5. 运行测试
    result = runner.run()
    
    print(f"\n自定义题目测试结果: {result.overall_percentage:.1f}%")


def main():
    print("=" * 60)
    print("自定义题目测试示例")
    print("=" * 60)
    
    test_with_custom_questions()


if __name__ == "__main__":
    main()
