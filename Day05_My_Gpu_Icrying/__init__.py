"""
AI综合能力测试框架

用于系统性地测试AI模型在逻辑、语言、数学、常识和创造性思维等维度的能力。
"""

__version__ = "1.0.0"
__author__ = "AI Test Suite"

from .runner import TestRunner
from .models import ModelInterface, OpenAIModel, HuggingFaceModel, DummyModel
from .questions import Question, QuestionBank, QuestionCategory, DifficultyLevel
from .evaluator import Evaluator, RuleBasedEvaluator, LLMBasedEvaluator
from .reporters import ConsoleReporter, JSONReporter, MarkdownReporter, TestResult, TestSuiteResult

__all__ = [
    "TestRunner",
    "ModelInterface",
    "OpenAIModel", 
    "HuggingFaceModel",
    "DummyModel",
    "Question",
    "QuestionBank",
    "QuestionCategory",
    "DifficultyLevel",
    "Evaluator",
    "RuleBasedEvaluator",
    "LLMBasedEvaluator",
    "ConsoleReporter",
    "JSONReporter",
    "MarkdownReporter",
    "TestResult",
    "TestSuiteResult",
]
