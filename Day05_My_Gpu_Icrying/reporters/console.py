"""
控制台报告生成器
"""

from typing import Optional
from .base import Reporter, TestSuiteResult


class ConsoleReporter(Reporter):
    """在控制台输出彩色报告"""
    
    # ANSI颜色代码
    COLORS = {
        "reset": "\033[0m",
        "bold": "\033[1m",
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
    }
    
    def __init__(self, use_color: bool = True, verbose: bool = True):
        self.use_color = use_color
        self.verbose = verbose
    
    def _color(self, text: str, color: str) -> str:
        """添加颜色"""
        if not self.use_color:
            return text
        return f"{self.COLORS.get(color, '')}{text}{self.COLORS['reset']}"
    
    def report(self, result: TestSuiteResult, output_path: Optional[str] = None):
        """生成控制台报告"""
        
        # 标题
        print("\n" + "=" * 70)
        print(self._color("🤖 AI 综合能力测试报告", "bold"))
        print("=" * 70)
        
        # 基本信息
        print(f"\n模型名称: {self._color(result.model_name, 'cyan')}")
        print(f"测试时间: {result.start_time} ~ {result.end_time}")
        print(f"总用时: {result.total_duration:.2f}秒")
        
        # 总体得分
        print("\n" + "-" * 70)
        print(self._color("📊 总体得分", "bold"))
        print("-" * 70)
        
        total_pct = result.overall_percentage
        if total_pct >= 90:
            grade = "🌟 卓越"
            grade_color = "green"
        elif total_pct >= 70:
            grade = "✅ 良好"
            grade_color = "cyan"
        elif total_pct >= 60:
            grade = "⚠️ 及格"
            grade_color = "yellow"
        else:
            grade = "❌ 不及格"
            grade_color = "red"
        
        print(f"\n总分: {self._color(f'{result.total_score:.1f}', 'bold')} / {result.max_score:.1f}")
        print(f"百分比: {self._color(f'{total_pct:.1f}%', grade_color)}")
        print(f"等级: {self._color(grade, grade_color)}")
        
        # 分类统计
        print("\n" + "-" * 70)
        print(self._color("📈 分类统计", "bold"))
        print("-" * 70)
        
        cat_stats = result.get_category_stats()
        for cat, stats in sorted(cat_stats.items()):
            pct = stats["percentage"]
            bar_len = int(pct / 5)  # 20字符=100%
            bar = "█" * bar_len + "░" * (20 - bar_len)
            
            if pct >= 70:
                bar_color = "green"
            elif pct >= 60:
                bar_color = "yellow"
            else:
                bar_color = "red"
            
            print(f"\n{cat:12} {self._color(bar, bar_color)} {pct:5.1f}% "
                  f"({stats['total_score']:.1f}/{stats['max_score']:.1f})")
            print(f"             题目数: {stats['count']}, 平均响应: {stats['avg_latency']:.2f}s")
        
        # 详细结果
        if self.verbose:
            print("\n" + "-" * 70)
            print(self._color("📝 详细结果", "bold"))
            print("-" * 70)
            
            for i, r in enumerate(result.results, 1):
                ev = r.evaluation
                pct = ev.percentage
                
                # 根据得分选择图标和颜色
                if pct >= 90:
                    icon = "🌟"
                    color = "green"
                elif pct >= 70:
                    icon = "✓"
                    color = "cyan"
                elif pct >= 60:
                    icon = "~"
                    color = "yellow"
                else:
                    icon = "✗"
                    color = "red"
                
                print(f"\n{self._color(f'{i}. [{icon}] {r.question_title}', color)}")
                print(f"   ID: {r.question_id} | 类别: {r.question_category} | "
                      f"难度: {'★' * r.question_difficulty}")
                print(f"   得分: {ev.score:.1f}/{ev.max_score} ({pct:.1f}%) | "
                      f"用时: {r.latency:.2f}s")
                
                if ev.feedback:
                    print(f"   评价: {ev.feedback}")
                
                if ev.suggestions:
                    print(f"   建议: {self._color(ev.suggestions, 'yellow')}")
                
                # 显示回答摘要
                answer_summary = r.answer[:150].replace('\n', ' ')
                if len(r.answer) > 150:
                    answer_summary += "..."
                print(f"   回答摘要: {answer_summary}")
        
        # 模型统计
        print("\n" + "-" * 70)
        print(self._color("🔧 模型统计", "bold"))
        print("-" * 70)
        
        stats = result.model_stats
        print(f"总调用次数: {stats.get('total_calls', 'N/A')}")
        print(f"平均响应时间: {stats.get('avg_latency', 'N/A'):.3f}s")
        print(f"总输入tokens: {stats.get('total_tokens_input', 'N/A')}")
        print(f"总输出tokens: {stats.get('total_tokens_output', 'N/A')}")
        
        # 总结
        print("\n" + "=" * 70)
        print(self._color("测试完成", "bold"))
        print("=" * 70 + "\n")
