"""
题目基类定义
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List, Callable
from enum import Enum


class QuestionCategory(Enum):
    """题目类别"""
    LOGIC = "logic"                    # 逻辑与推理
    LANGUAGE = "language"              # 语言理解
    MATH = "math"                      # 数学与抽象思维
    COMMON_SENSE = "common_sense"      # 常识推理
    CREATIVITY = "creativity"          # 创造性思维
    ETHICS = "ethics"                  # 伦理与价值观
    META = "meta"                      # 元认知


class DifficultyLevel(Enum):
    """难度等级"""
    EASY = 1
    MEDIUM = 2
    HARD = 3
    EXPERT = 4


@dataclass
class Question:
    """
    测试题目数据类
    
    Attributes:
        id: 题目唯一标识
        category: 题目类别
        difficulty: 难度等级
        title: 题目标题
        content: 题目内容
        answer: 参考答案（可以是字符串或列表）
        keywords: 关键词列表（用于自动评分）
        score: 满分分值
        hints: 提示信息
        metadata: 其他元数据
        evaluator: 自定义评分函数
    """
    id: str
    category: QuestionCategory
    difficulty: DifficultyLevel
    title: str
    content: str
    answer: Optional[str] = None
    keywords: List[str] = field(default_factory=list)
    score: float = 10.0
    hints: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    evaluator: Optional[Callable[[str, "Question"], float]] = None
    
    def __post_init__(self):
        # 确保 category 和 difficulty 是枚举类型
        if isinstance(self.category, str):
            self.category = QuestionCategory(self.category)
        if isinstance(self.difficulty, (int, str)):
            self.difficulty = DifficultyLevel(int(self.difficulty))
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "id": self.id,
            "category": self.category.value,
            "difficulty": self.difficulty.value,
            "title": self.title,
            "content": self.content,
            "answer": self.answer,
            "keywords": self.keywords,
            "score": self.score,
            "hints": self.hints,
            "metadata": self.metadata,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Question":
        """从字典创建"""
        return cls(
            id=data["id"],
            category=QuestionCategory(data.get("category", "logic")),
            difficulty=DifficultyLevel(data.get("difficulty", 2)),
            title=data["title"],
            content=data["content"],
            answer=data.get("answer"),
            keywords=data.get("keywords", []),
            score=data.get("score", 10.0),
            hints=data.get("hints"),
            metadata=data.get("metadata", {}),
        )
    
    def get_full_prompt(self) -> str:
        """获取完整的提问文本"""
        prompt = f"【{self.title}】\n\n{self.content}"
        if self.hints:
            prompt += f"\n\n提示：{self.hints}"
        return prompt
