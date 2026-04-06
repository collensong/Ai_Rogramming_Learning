"""
报告生成模块 - 输出测试结果
"""

from .base import Reporter, TestResult, TestSuiteResult
from .console import ConsoleReporter
from .json_reporter import JSONReporter
from .markdown import MarkdownReporter

__all__ = [
    "Reporter",
    "TestResult",
    "TestSuiteResult",
    "ConsoleReporter",
    "JSONReporter",
    "MarkdownReporter",
]
