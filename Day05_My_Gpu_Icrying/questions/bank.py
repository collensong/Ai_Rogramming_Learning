"""
题目库管理
"""

import json
import random
from typing import List, Optional, Dict, Any
from pathlib import Path

from .base import Question, QuestionCategory, DifficultyLevel


class QuestionBank:
    """
    题目库管理类
    
    支持添加、删除、筛选题目，以及从文件加载/保存
    """
    
    def __init__(self):
        self.questions: List[Question] = []
    
    def add(self, question: Question) -> "QuestionBank":
        """添加题目"""
        # 检查ID是否重复
        for q in self.questions:
            if q.id == question.id:
                raise ValueError(f"Question with id '{question.id}' already exists")
        self.questions.append(question)
        return self
    
    def add_many(self, questions: List[Question]) -> "QuestionBank":
        """批量添加题目"""
        for q in questions:
            self.add(q)
        return self
    
    def remove(self, question_id: str) -> bool:
        """删除题目"""
        for i, q in enumerate(self.questions):
            if q.id == question_id:
                self.questions.pop(i)
                return True
        return False
    
    def get(self, question_id: str) -> Optional[Question]:
        """根据ID获取题目"""
        for q in self.questions:
            if q.id == question_id:
                return q
        return None
    
    def filter(
        self,
        category: Optional[QuestionCategory] = None,
        difficulty: Optional[DifficultyLevel] = None,
        min_difficulty: Optional[DifficultyLevel] = None,
        max_difficulty: Optional[DifficultyLevel] = None,
    ) -> List[Question]:
        """
        筛选题目
        
        Args:
            category: 指定类别
            difficulty: 指定难度
            min_difficulty: 最小难度
            max_difficulty: 最大难度
        """
        result = self.questions.copy()
        
        if category:
            result = [q for q in result if q.category == category]
        
        if difficulty:
            result = [q for q in result if q.difficulty == difficulty]
        else:
            if min_difficulty:
                result = [q for q in result if q.difficulty.value >= min_difficulty.value]
            if max_difficulty:
                result = [q for q in result if q.difficulty.value <= max_difficulty.value]
        
        return result
    
    def sample(
        self,
        n: int,
        category: Optional[QuestionCategory] = None,
        difficulty: Optional[DifficultyLevel] = None,
        shuffle: bool = True
    ) -> List[Question]:
        """
        随机抽取题目
        
        Args:
            n: 抽取数量
            category: 指定类别
            difficulty: 指定难度
            shuffle: 是否打乱顺序
        """
        candidates = self.filter(category=category, difficulty=difficulty)
        
        if len(candidates) < n:
            raise ValueError(
                f"Not enough questions (requested {n}, have {len(candidates)})"
            )
        
        if shuffle:
            return random.sample(candidates, n)
        return candidates[:n]
    
    def create_test_set(
        self,
        categories: Optional[Dict[QuestionCategory, int]] = None,
        total: Optional[int] = None,
        shuffle: bool = True
    ) -> List[Question]:
        """
        创建测试集
        
        Args:
            categories: 各类别题目数量，如 {QuestionCategory.LOGIC: 5, ...}
            total: 总题目数（如果指定，会平均分配到各类别）
            shuffle: 是否打乱顺序
        """
        if categories is None:
            # 默认每个类别抽取相同数量
            all_categories = list(QuestionCategory)
            if total:
                per_category = total // len(all_categories)
                categories = {cat: per_category for cat in all_categories}
            else:
                categories = {cat: 2 for cat in all_categories}
        
        result = []
        for category, count in categories.items():
            available = self.filter(category=category)
            if len(available) < count:
                raise ValueError(
                    f"Not enough questions for {category.value} "
                    f"(requested {count}, have {len(available)})"
                )
            result.extend(random.sample(available, count))
        
        if shuffle:
            random.shuffle(result)
        
        return result
    
    def load_from_json(self, path: str) -> "QuestionBank":
        """从JSON文件加载题目"""
        path = Path(path)
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for item in data:
            self.add(Question.from_dict(item))
        
        return self
    
    def save_to_json(self, path: str):
        """保存题目到JSON文件"""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        data = [q.to_dict() for q in self.questions]
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def __len__(self) -> int:
        return len(self.questions)
    
    def __iter__(self):
        return iter(self.questions)
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        stats = {
            "total": len(self.questions),
            "by_category": {},
            "by_difficulty": {},
        }
        
        for cat in QuestionCategory:
            count = len(self.filter(category=cat))
            stats["by_category"][cat.value] = count
        
        for diff in DifficultyLevel:
            count = len(self.filter(difficulty=diff))
            stats["by_difficulty"][diff.name] = count
        
        return stats
