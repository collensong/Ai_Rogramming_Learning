"""
基于LLM的评分器 - 使用另一个AI来评估
"""

from typing import Optional, Any
import json

from .base import Evaluator, EvaluationResult, ScoreLevel


class LLMBasedEvaluator(Evaluator):
    """
    使用LLM作为评判的评分器
    
    适合评估开放性问题和创造性回答
    
    Usage:
        judge_model = OpenAIModel("gpt-4")
        evaluator = LLMBasedEvaluator(judge_model)
    """
    
    DEFAULT_PROMPT_TEMPLATE = """你是一个严格的评分专家。请评估以下AI回答的质量。

【题目】
{title}

【题目内容】
{content}

【参考答案】
{answer}

【AI的回答】
{response}

【评分标准】
满分：{max_score}分

请从以下维度进行评估：
1. 准确性：回答是否正确
2. 完整性：是否覆盖所有要点
3. 清晰度：表达是否清晰易懂
4. 深度：是否有深入分析

请以JSON格式输出评分结果：
{{
    "score": <0到{max_score}之间的分数>,
    "percentage": <百分比，0-100>,
    "feedback": "详细评价",
    "strengths": ["优点1", "优点2"],
    "weaknesses": ["不足1", "不足2"],
    "suggestions": "改进建议"
}}
"""
    
    def __init__(
        self,
        judge_model,
        name: str = "llm_based",
        prompt_template: Optional[str] = None,
        temperature: float = 0.1,
    ):
        """
        初始化LLM评分器
        
        Args:
            judge_model: 用于评判的模型（需实现generate方法）
            prompt_template: 自定义提示模板
            temperature: 评判时的温度参数（建议低温度以保证一致性）
        """
        super().__init__(name)
        self.judge_model = judge_model
        self.prompt_template = prompt_template or self.DEFAULT_PROMPT_TEMPLATE
        self.temperature = temperature
    
    def evaluate(
        self,
        answer: str,
        question,
        model_response: Optional[Any] = None
    ) -> EvaluationResult:
        """使用LLM评估回答"""
        
        # 构建提示
        prompt = self.prompt_template.format(
            title=question.title,
            content=question.content,
            answer=question.answer or "无（开放性问题）",
            response=answer,
            max_score=question.score,
        )
        
        # 调用评判模型
        judge_response = self.judge_model.generate(
            prompt=prompt,
            temperature=self.temperature,
            max_tokens=1000,
        )
        
        # 解析JSON结果
        try:
            # 尝试提取JSON部分
            text = judge_response.text
            # 寻找JSON块
            start = text.find('{')
            end = text.rfind('}') + 1
            if start >= 0 and end > start:
                json_str = text[start:end]
                result_data = json.loads(json_str)
            else:
                raise ValueError("No JSON found in response")
            
            score = float(result_data.get("score", 0))
            percentage = float(result_data.get("percentage", score / question.score * 100))
            feedback = result_data.get("feedback", "")
            suggestions = result_data.get("suggestions", "")
            
            details = {
                "strengths": result_data.get("strengths", []),
                "weaknesses": result_data.get("weaknesses", []),
                "judge_raw_response": text,
            }
            
        except (json.JSONDecodeError, ValueError) as e:
            # 解析失败，返回默认评分
            score = 0
            percentage = 0
            feedback = f"评分解析失败: {str(e)}"
            suggestions = None
            details = {"error": str(e), "raw_response": judge_response.text}
        
        return EvaluationResult(
            score=round(score, 2),
            max_score=question.score,
            percentage=round(percentage, 2),
            level=ScoreLevel.PASS,
            feedback=feedback,
            details=details,
            suggestions=suggestions,
        )
