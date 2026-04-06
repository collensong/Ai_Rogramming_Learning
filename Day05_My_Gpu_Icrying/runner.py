"""
测试运行器 - 协调整个测试流程
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
import time

from .models import ModelInterface, ModelResponse
from .questions import QuestionBank, Question, get_builtin_questions
from .evaluator import Evaluator, RuleBasedEvaluator
from .reporters import Reporter, ConsoleReporter, TestResult, TestSuiteResult


class TestRunner:
    """
    AI综合能力测试运行器
    
    负责协调整个测试流程：加载题目 -> 运行测试 -> 评估结果 -> 生成报告
    
    Usage:
        # 快速开始
        model = HuggingFaceModel("Qwen/Qwen2.5-0.5B-Instruct")
        runner = TestRunner(model)
        result = runner.run()
        
        # 自定义配置
        bank = QuestionBank()
        bank.add_many(get_builtin_questions())
        bank.load_from_json("custom_questions.json")
        
        runner = TestRunner(
            model=model,
            question_bank=bank,
            evaluator=RuleBasedEvaluator(),
            reporter=ConsoleReporter(verbose=True),
        )
        result = runner.run(
            categories=["logic", "math"],  # 只测试特定类别
            shuffle=True,
            delay=1.0,  # 题目间隔
        )
    """
    
    def __init__(
        self,
        model: ModelInterface,
        question_bank: Optional[QuestionBank] = None,
        evaluator: Optional[Evaluator] = None,
        reporter: Optional[Reporter] = None,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ):
        """
        初始化测试运行器
        
        Args:
            model: 要测试的AI模型
            question_bank: 题目库（默认使用内置题目）
            evaluator: 评分器（默认使用RuleBasedEvaluator）
            reporter: 报告生成器（默认使用ConsoleReporter）
            system_prompt: 系统提示词
            temperature: 生成温度
            max_tokens: 最大token数
        """
        self.model = model
        self.question_bank = question_bank or self._create_default_bank()
        self.evaluator = evaluator or RuleBasedEvaluator()
        self.reporter = reporter or ConsoleReporter()
        self.system_prompt = system_prompt
        self.temperature = temperature
        self.max_tokens = max_tokens
    
    def _create_default_bank(self) -> QuestionBank:
        """创建默认题目库"""
        bank = QuestionBank()
        bank.add_many(get_builtin_questions())
        return bank
    
    def run(
        self,
        questions: Optional[List[Question]] = None,
        question_ids: Optional[List[str]] = None,
        categories: Optional[List[str]] = None,
        difficulties: Optional[List[int]] = None,
        shuffle: bool = False,
        limit: Optional[int] = None,
        delay: float = 0.0,
        progress_callback: Optional[Any] = None,
    ) -> TestSuiteResult:
        """
        运行测试
        
        Args:
            questions: 直接指定题目列表
            question_ids: 指定题目ID列表
            categories: 指定类别列表（如 ["logic", "math"]）
            difficulties: 指定难度列表（如 [1, 2]）
            shuffle: 是否打乱顺序
            limit: 限制题目数量
            delay: 每题之间的延迟（秒）
            progress_callback: 进度回调函数
            
        Returns:
            TestSuiteResult: 测试结果
        """
        # 获取题目列表
        if questions:
            test_questions = questions
        else:
            test_questions = list(self.question_bank.questions)
            
            # 应用筛选
            if question_ids:
                test_questions = [q for q in test_questions if q.id in question_ids]
            
            if categories:
                from .questions import QuestionCategory
                cat_enums = [QuestionCategory(c) for c in categories]
                test_questions = [q for q in test_questions if q.category in cat_enums]
            
            if difficulties:
                test_questions = [q for q in test_questions 
                                if q.difficulty.value in difficulties]
        
        # 打乱顺序
        if shuffle:
            import random
            random.shuffle(test_questions)
        
        # 限制数量
        if limit and limit < len(test_questions):
            test_questions = test_questions[:limit]
        
        print(f"\n准备测试 {len(test_questions)} 道题目...")
        print(f"模型: {self.model.model_name}")
        print("-" * 50)
        
        # 重置模型统计
        self.model.reset_stats()
        
        # 开始测试
        start_time = datetime.now()
        results: List[TestResult] = []
        
        for i, question in enumerate(test_questions, 1):
            print(f"\n[{i}/{len(test_questions)}] 正在测试: {question.title}")
            
            # 调用模型
            try:
                model_response = self.model.generate(
                    prompt=question.get_full_prompt(),
                    system_prompt=self.system_prompt,
                    temperature=self.temperature,
                    max_tokens=self.max_tokens,
                )
                answer = model_response.text
            except Exception as e:
                print(f"  ⚠️ 调用失败: {e}")
                answer = f"[错误: {str(e)}]"
                model_response = ModelResponse(
                    text=answer,
                    model_name=self.model.model_name,
                    latency=0,
                    tokens_input=0,
                    tokens_output=0,
                )
            
            # 评估回答
            evaluation = self.evaluator.evaluate(answer, question, model_response)
            
            # 创建结果
            result = TestResult(
                question_id=question.id,
                question_title=question.title,
                question_category=question.category.value,
                question_difficulty=question.difficulty.value,
                question_content=question.content[:200] + "..." if len(question.content) > 200 else question.content,
                answer=answer,
                evaluation=evaluation,
                latency=model_response.latency,
                tokens_input=model_response.tokens_input,
                tokens_output=model_response.tokens_output,
            )
            results.append(result)
            
            print(f"  得分: {evaluation.score:.1f}/{evaluation.max_score} ({evaluation.percentage:.1f}%)")
            
            # 进度回调
            if progress_callback:
                progress_callback(i, len(test_questions), result)
            
            # 延迟
            if delay > 0 and i < len(test_questions):
                time.sleep(delay)
        
        end_time = datetime.now()
        total_duration = (end_time - start_time).total_seconds()
        
        # 组装结果
        suite_result = TestSuiteResult(
            model_name=self.model.model_name,
            start_time=start_time.isoformat(),
            end_time=end_time.isoformat(),
            total_duration=total_duration,
            results=results,
            model_stats=self.model.get_stats(),
        )
        
        # 生成报告
        self.reporter.report(suite_result)
        
        return suite_result
    
    def run_quick_test(self, num_questions: int = 5) -> TestSuiteResult:
        """
        快速测试 - 随机抽取少量题目
        
        Args:
            num_questions: 题目数量
        """
        questions = self.question_bank.sample(num_questions)
        return self.run(questions=questions)
    
    def run_category_test(
        self,
        category: str,
        num_questions: Optional[int] = None
    ) -> TestSuiteResult:
        """
        按类别测试
        
        Args:
            category: 类别名称
            num_questions: 题目数量（默认全部）
        """
        from .questions import QuestionCategory
        questions = self.question_bank.filter(category=QuestionCategory(category))
        
        if num_questions and num_questions < len(questions):
            import random
            questions = random.sample(questions, num_questions)
        
        return self.run(questions=questions)
    
    def benchmark(
        self,
        models: List[ModelInterface],
        questions: Optional[List[Question]] = None,
    ) -> Dict[str, TestSuiteResult]:
        """
        多模型对比测试
        
        Args:
            models: 要对比的模型列表
            questions: 测试题目（默认使用全部）
            
        Returns:
            Dict[model_name, TestSuiteResult]: 各模型结果
        """
        if questions is None:
            questions = list(self.question_bank.questions)
        
        results = {}
        for model in models:
            print(f"\n{'='*50}")
            print(f"测试模型: {model.model_name}")
            print(f"{'='*50}")
            
            # 临时切换模型
            original_model = self.model
            self.model = model
            
            result = self.run(questions=questions)
            results[model.model_name] = result
            
            # 恢复模型
            self.model = original_model
        
        # 输出对比报告
        self._print_benchmark_summary(results)
        
        return results
    
    def _print_benchmark_summary(self, results: Dict[str, TestSuiteResult]):
        """打印对比摘要"""
        print("\n" + "=" * 70)
        print("🏆 多模型对比结果")
        print("=" * 70)
        
        # 按总分排序
        sorted_results = sorted(
            results.items(),
            key=lambda x: x[1].overall_percentage,
            reverse=True
        )
        
        print(f"\n{'排名':<4} {'模型':<30} {'总分':<10} {'百分比':<10}")
        print("-" * 70)
        
        for i, (name, result) in enumerate(sorted_results, 1):
            print(f"{i:<4} {name:<30} {result.total_score:>6.1f} {result.overall_percentage:>8.1f}%")
        
        print("\n各类别得分对比:")
        print("-" * 70)
        
        # 获取所有类别
        all_categories = set()
        for result in results.values():
            all_categories.update(result.get_category_stats().keys())
        
        print(f"{'类别':<15}", end="")
        for name, _ in sorted_results:
            print(f"{name[:12]:<15}", end="")
        print()
        
        for cat in sorted(all_categories):
            print(f"{cat:<15}", end="")
            for name, result in sorted_results:
                cat_stats = result.get_category_stats()
                pct = cat_stats.get(cat, {}).get("percentage", 0)
                print(f"{pct:>6.1f}%       ", end="")
            print()
        
        print("=" * 70)
