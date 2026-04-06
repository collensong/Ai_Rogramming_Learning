"""
评分器基类
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from enum import Enum


class ScoreLevel(Enum):
    """评分等级"""
    EXCELLENT = "excellent"    # 90-100
    GOOD = "good"              # 70-89
    PASS = "pass"              # 60-69
    FAIL = "fail"              # 0-59


@dataclass
class EvaluationResult:
    """评分结果"""
    score: float                    # 原始分数（0-满分）
    max_score: float               # 满分
    percentage: float              # 百分比（0-100）
    level: ScoreLevel              # 等级
    feedback: str                  # 评价反馈
    details: Dict[str, Any] = field(default_factory=dict)
    suggestions: Optional[str] = None
    
    def __post_init__(self):
        # 自动计算等级
        if self.percentage >= 90:
            self.level = ScoreLevel.EXCELLENT
        elif self.percentage >= 70:
            self.level = ScoreLevel.GOOD
        elif self.percentage >= 60:
            self.level = ScoreLevel.PASS
        else:
            self.level = ScoreLevel.FAIL
    
    @property
    def passed(self) -> bool:
        """是否通过（>=60%）"""
        return self.percentage >= 60
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "score": self.score,
            "max_score": self.max_score,
            "percentage": round(self.percentage, 2),
            "level": self.level.value,
            "passed": self.passed,
            "feedback": self.feedback,
            "details": self.details,
            "suggestions": self.suggestions,
        }


class Evaluator(ABC):
    """
    评分器抽象基类
    """
    
    def __init__(self, name: str = "base"):
        self.name = name
    
    @abstractmethod
    def evaluate(
        self,
        answer: str,
        question,
        model_response: Optional[Any] = None
    ) -> EvaluationResult:
        """
        评估回答
        
        Args:
            answer: AI的回答文本
            question: 题目对象
            model_response: 原始模型响应（可选）
            
        Returns:
            EvaluationResult: 评分结果
        """
        pass
    
    def evaluate_batch(
        self,
        answers: list,
        questions: list,
        model_responses: Optional[list] = None
    ) -> list:
        """批量评估"""
        results = []
        model_responses = model_responses or [None] * len(answers)
        for ans, q, resp in zip(answers, questions, model_responses):
            results.append(self.evaluate(ans, q, resp))
        return results
