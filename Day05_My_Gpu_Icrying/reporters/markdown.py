"""
Markdown报告生成器 - 生成美观的Markdown报告
"""

from datetime import datetime
from typing import Optional
from pathlib import Path

from .base import Reporter, TestSuiteResult


class MarkdownReporter(Reporter):
    """生成Markdown格式的报告"""
    
    def report(self, result: TestSuiteResult, output_path: Optional[str] = None):
        """生成Markdown报告"""
        
        lines = []
        
        # 标题
        lines.append("# 🤖 AI 综合能力测试报告")
        lines.append("")
        
        # 元信息
        lines.append("## 📋 测试信息")
        lines.append("")
        lines.append(f"| 项目 | 值 |")
        lines.append(f"|------|-----|")
        lines.append(f"| 模型名称 | {result.model_name} |")
        lines.append(f"| 测试时间 | {result.start_time} ~ {result.end_time} |")
        lines.append(f"| 总用时 | {result.total_duration:.2f}秒 |")
        lines.append("")
        
        # 总体得分
        lines.append("## 📊 总体得分")
        lines.append("")
        
        total_pct = result.overall_percentage
        if total_pct >= 90:
            grade = "🌟 卓越 (90-100)"
            grade_emoji = "🌟"
        elif total_pct >= 70:
            grade = "✅ 良好 (70-89)"
            grade_emoji = "✅"
        elif total_pct >= 60:
            grade = "⚠️ 及格 (60-69)"
            grade_emoji = "⚠️"
        else:
            grade = "❌ 不及格 (0-59)"
            grade_emoji = "❌"
        
        lines.append(f"| 指标 | 数值 |")
        lines.append(f"|------|------|")
        lines.append(f"| 总分 | **{result.total_score:.1f}** / {result.max_score:.1f} |")
        lines.append(f"| 百分比 | **{total_pct:.1f}%** |")
        lines.append(f"| 等级 | {grade} |")
        lines.append("")
        
        # 进度条可视化
        bar_len = int(total_pct / 2)
        bar = "█" * bar_len + "░" * (50 - bar_len)
        lines.append(f"```")
        lines.append(f"总体进度: [{bar}] {total_pct:.1f}%")
        lines.append(f"```")
        lines.append("")
        
        # 分类统计
        lines.append("## 📈 分类统计")
        lines.append("")
        
        cat_stats = result.get_category_stats()
        lines.append(f"| 类别 | 题目数 | 得分 | 百分比 | 平均响应 |")
        lines.append(f"|------|--------|------|--------|----------|")
        
        for cat, stats in sorted(cat_stats.items()):
            pct = stats["percentage"]
            pct_str = f"{pct:.1f}%"
            lines.append(
                f"| {cat} | {stats['count']} | "
                f"{stats['total_score']:.1f}/{stats['max_score']:.1f} | "
                f"{pct_str} | {stats['avg_latency']:.2f}s |"
            )
        
        lines.append("")
        
        # 详细结果
        lines.append("## 📝 详细结果")
        lines.append("")
        
        for i, r in enumerate(result.results, 1):
            ev = r.evaluation
            pct = ev.percentage
            
            # 根据得分选择图标
            if pct >= 90:
                icon = "🌟"
            elif pct >= 70:
                icon = "✅"
            elif pct >= 60:
                icon = "⚠️"
            else:
                icon = "❌"
            
            lines.append(f"### {i}. {icon} {r.question_title}")
            lines.append("")
            lines.append(f"**题目ID**: `{r.question_id}`  ")
            lines.append(f"**类别**: {r.question_category}  ")
            lines.append(f"**难度**: {'★' * r.question_difficulty}{'☆' * (4-r.question_difficulty)}  ")
            lines.append(f"**得分**: {ev.score:.1f}/{ev.max_score} ({pct:.1f}%)  ")
            lines.append(f"**响应时间**: {r.latency:.2f}s  ")
            lines.append("")
            
            lines.append("**题目内容**：")
            lines.append(f"```\n{r.question_content}\n```")
            lines.append("")
            
            lines.append("**AI回答**：")
            lines.append(f"> {r.answer.replace(chr(10), chr(10)+'> ')}")
            lines.append("")
            
            if ev.feedback:
                lines.append(f"**评价**: {ev.feedback}")
                lines.append("")
            
            if ev.suggestions:
                lines.append(f"**改进建议**: 💡 {ev.suggestions}")
                lines.append("")
            
            # 如果存在参考答案，显示对比
            if r.question_content and "【参考答案】" not in r.question_content:
                # 尝试从元数据获取参考答案
                pass
            
            lines.append("---")
            lines.append("")
        
        # 模型统计
        lines.append("## 🔧 模型统计")
        lines.append("")
        
        stats = result.model_stats
        lines.append(f"| 指标 | 数值 |")
        lines.append(f"|------|------|")
        lines.append(f"| 总调用次数 | {stats.get('total_calls', 'N/A')} |")
        lines.append(f"| 平均响应时间 | {stats.get('avg_latency', 0):.3f}s |")
        lines.append(f"| 总输入tokens | {stats.get('total_tokens_input', 'N/A')} |")
        lines.append(f"| 总输出tokens | {stats.get('total_tokens_output', 'N/A')} |")
        lines.append("")
        
        # 页脚
        lines.append("---")
        lines.append("")
        lines.append(f"*报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
        
        markdown_content = "\n".join(lines)
        
        if output_path:
            path = Path(output_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            print(f"报告已保存到: {path.absolute()}")
        else:
            print(markdown_content)
        
        return markdown_content
