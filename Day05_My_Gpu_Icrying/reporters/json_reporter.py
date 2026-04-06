"""
JSON报告生成器
"""

import json
from datetime import datetime
from typing import Optional
from pathlib import Path

from .base import Reporter, TestSuiteResult


class JSONReporter(Reporter):
    """生成JSON格式的报告"""
    
    def __init__(self, indent: int = 2):
        self.indent = indent
    
    def report(self, result: TestSuiteResult, output_path: Optional[str] = None):
        """生成JSON报告"""
        
        data = {
            "meta": {
                "model_name": result.model_name,
                "start_time": result.start_time,
                "end_time": result.end_time,
                "total_duration": result.total_duration,
                "generated_at": datetime.now().isoformat(),
            },
            "summary": {
                "total_score": result.total_score,
                "max_score": result.max_score,
                "overall_percentage": round(result.overall_percentage, 2),
                "total_questions": len(result.results),
            },
            "category_stats": result.get_category_stats(),
            "model_stats": result.model_stats,
            "results": [
                {
                    "question_id": r.question_id,
                    "question_title": r.question_title,
                    "question_category": r.question_category,
                    "question_difficulty": r.question_difficulty,
                    "question_content": r.question_content,
                    "answer": r.answer,
                    "evaluation": r.evaluation.to_dict(),
                    "latency": r.latency,
                    "tokens_input": r.tokens_input,
                    "tokens_output": r.tokens_output,
                }
                for r in result.results
            ],
        }
        
        json_str = json.dumps(data, ensure_ascii=False, indent=self.indent)
        
        if output_path:
            path = Path(output_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(json_str)
            print(f"报告已保存到: {path.absolute()}")
        else:
            print(json_str)
        
        return data
