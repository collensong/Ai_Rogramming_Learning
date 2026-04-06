"""
报告生成器基类
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field


@dataclass
class TestResult:
    """单个测试的结果"""
    question_id: str
    question_title: str
    question_category: str
    question_difficulty: int
    question_content: str
    answer: str                      # AI的回答
    evaluation: Any                  # EvaluationResult
    latency: float                   # 响应时间
    tokens_input: int
    tokens_output: int


@dataclass
class TestSuiteResult:
    """整个测试集的结果"""
    model_name: str
    start_time: str
    end_time: str
    total_duration: float
    results: List[TestResult]
    model_stats: Dict[str, Any]
    
    @property
    def total_score(self) -> float:
        return sum(r.evaluation.score for r in self.results)
    
    @property
    def max_score(self) -> float:
        return sum(r.evaluation.max_score for r in self.results)
    
    @property
    def overall_percentage(self) -> float:
        if self.max_score == 0:
            return 0
        return (self.total_score / self.max_score) * 100
    
    def get_category_stats(self) -> Dict[str, Dict[str, Any]]:
        """按类别统计"""
        stats = {}
        for r in self.results:
            cat = r.question_category
            if cat not in stats:
                stats[cat] = {
                    "count": 0,
                    "total_score": 0,
                    "max_score": 0,
                    "avg_latency": 0,
                }
            stats[cat]["count"] += 1
            stats[cat]["total_score"] += r.evaluation.score
            stats[cat]["max_score"] += r.evaluation.max_score
            stats[cat]["avg_latency"] += r.latency
        
        for cat in stats:
            stats[cat]["avg_latency"] /= stats[cat]["count"]
            stats[cat]["percentage"] = (
                stats[cat]["total_score"] / stats[cat]["max_score"] * 100
            )
        
        return stats


class Reporter(ABC):
    """报告生成器基类"""
    
    @abstractmethod
    def report(self, result: TestSuiteResult, output_path: Optional[str] = None):
        """生成报告"""
        pass
