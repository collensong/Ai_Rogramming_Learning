"""
基于规则的评分器
"""

import re
from typing import Optional, List, Any
from .base import Evaluator, EvaluationResult, ScoreLevel


class RuleBasedEvaluator(Evaluator):
    """
    基于关键词和规则的评分器
    
    评分策略：
    1. 检查是否包含正确答案（如果是客观题）
    2. 检查关键词匹配情况
    3. 评估回答长度和结构
    4. 检测常见错误模式
    """
    
    def __init__(
        self,
        name: str = "rule_based",
        keyword_weight: float = 0.4,
        answer_weight: float = 0.4,
        length_weight: float = 0.1,
        structure_weight: float = 0.1,
        case_sensitive: bool = False,
    ):
        super().__init__(name)
        self.keyword_weight = keyword_weight
        self.answer_weight = answer_weight
        self.length_weight = length_weight
        self.structure_weight = structure_weight
        self.case_sensitive = case_sensitive
    
    def evaluate(
        self,
        answer: str,
        question,
        model_response: Optional[Any] = None
    ) -> EvaluationResult:
        """评估回答"""
        
        scores = {}
        details = {}
        feedback_parts = []
        
        # 1. 关键词匹配评分
        keyword_score = self._evaluate_keywords(answer, question.keywords)
        scores["keywords"] = keyword_score * self.keyword_weight
        details["keyword_matches"] = keyword_score
        
        if keyword_score > 0.8:
            feedback_parts.append("回答包含关键概念")
        elif keyword_score > 0.5:
            feedback_parts.append("回答包含部分关键概念")
        else:
            feedback_parts.append("回答缺少关键概念")
        
        # 2. 参考答案匹配（如果有）
        if question.answer:
            answer_score = self._evaluate_answer_match(answer, question.answer)
            scores["answer_match"] = answer_score * self.answer_weight
            details["answer_similarity"] = answer_score
            
            if answer_score > 0.8:
                feedback_parts.append("回答与参考答案高度吻合")
            elif answer_score > 0.5:
                feedback_parts.append("回答部分符合参考答案")
        else:
            scores["answer_match"] = 0
            details["answer_similarity"] = None
        
        # 3. 长度评分（鼓励详细回答，但避免过度冗长）
        length_score = self._evaluate_length(answer)
        scores["length"] = length_score * self.length_weight
        details["length_score"] = length_score
        
        # 4. 结构评分
        structure_score = self._evaluate_structure(answer)
        scores["structure"] = structure_score * self.structure_weight
        details["structure_score"] = structure_score
        
        # 计算总分
        total_score = sum(scores.values()) * question.score
        percentage = (sum(scores.values()) / sum([
            self.keyword_weight, self.answer_weight, 
            self.length_weight, self.structure_weight
        ])) * 100
        
        # 生成反馈
        feedback = "；".join(feedback_parts)
        
        # 生成建议
        suggestions = self._generate_suggestions(answer, question, scores)
        
        return EvaluationResult(
            score=round(total_score, 2),
            max_score=question.score,
            percentage=round(percentage, 2),
            level=ScoreLevel.PASS,  # 会被重新计算
            feedback=feedback,
            details={
                "component_scores": scores,
                **details,
            },
            suggestions=suggestions,
        )
    
    def _evaluate_keywords(self, answer: str, keywords: List[str]) -> float:
        """评估关键词匹配度"""
        if not keywords:
            return 1.0
        
        answer_text = answer if self.case_sensitive else answer.lower()
        matched = 0
        
        for kw in keywords:
            kw_text = kw if self.case_sensitive else kw.lower()
            if kw_text in answer_text:
                matched += 1
        
        return matched / len(keywords)
    
    def _evaluate_answer_match(self, answer: str, reference: str) -> float:
        """评估与参考答案的匹配度"""
        # 简单实现：检查是否包含参考答案的关键词
        answer_text = answer if self.case_sensitive else answer.lower()
        reference_text = reference if self.case_sensitive else reference.lower()
        
        # 提取参考答案的关键词（简单分词）
        ref_words = set(reference_text.split())
        # 过滤掉常见词
        stop_words = {"的", "了", "是", "在", "和", "the", "a", "an", "is", "are", "to", "of"}
        ref_words = ref_words - stop_words
        
        if not ref_words:
            return 1.0
        
        matched = sum(1 for word in ref_words if word in answer_text)
        return matched / len(ref_words)
    
    def _evaluate_length(self, answer: str) -> float:
        """评估回答长度"""
        # 理想长度：50-500字符
        length = len(answer)
        
        if 50 <= length <= 500:
            return 1.0
        elif length < 50:
            # 太短
            return max(0, length / 50)
        else:
            # 太长，轻微惩罚
            return max(0.5, 1 - (length - 500) / 1000)
    
    def _evaluate_structure(self, answer: str) -> float:
        """评估回答结构"""
        score = 0.5  # 基础分
        
        # 有段落分隔
        if "\n\n" in answer or "\n" in answer:
            score += 0.2
        
        # 有编号或列表
        if re.search(r'(\d+[\.\)〕]|[-•·])', answer):
            score += 0.15
        
        # 有逻辑连接词
        connectives = ["首先", "其次", "因此", "所以", "因为", "但是", "however", "therefore", "first", "second"]
        if any(c in answer.lower() for c in connectives):
            score += 0.15
        
        return min(1.0, score)
    
    def _generate_suggestions(
        self, 
        answer: str, 
        question, 
        scores: dict
    ) -> Optional[str]:
        """生成改进建议"""
        suggestions = []
        
        if scores.get("keywords", 0) < 0.5:
            suggestions.append("尝试包含更多与问题相关的关键概念")
        
        if len(answer) < 50:
            suggestions.append("回答过于简短，可以尝试更详细地阐述")
        
        if scores.get("structure", 0) < 0.5:
            suggestions.append("使用段落分隔或列表可以提高回答的清晰度")
        
        return "；".join(suggestions) if suggestions else None
