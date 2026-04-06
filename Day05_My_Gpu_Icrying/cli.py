#!/usr/bin/env python3
"""
命令行工具 - 快速运行测试

Usage:
    python cli.py --model Qwen/Qwen2.5-0.5B-Instruct --num 5
    python cli.py --api-key $KIMI_API_KEY --base-url https://api.moonshot.cn/v1 --model moonshot-v1-8k
    python cli.py --json questions.json --report md
"""

import argparse
import os
import sys
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from ai_test_suite import (
    TestRunner,
    HuggingFaceModel,
    OpenAIModel,
    DummyModel,
    QuestionBank,
    ConsoleReporter,
    JSONReporter,
    MarkdownReporter,
    RuleBasedEvaluator,
)


def create_parser():
    """创建参数解析器"""
    parser = argparse.ArgumentParser(
        description="AI综合能力测试工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 测试本地模型
  python cli.py --model Qwen/Qwen2.5-0.5B-Instruct
  
  # 测试 API 模型
  python cli.py --api-key $KIMI_API_KEY \\
                --base-url https://api.moonshot.cn/v1 \\
                --model moonshot-v1-8k
  
  # 快速测试5道题
  python cli.py --model Qwen/Qwen2.5-0.5B-Instruct --quick --num 5
  
  # 只测试逻辑题
  python cli.py --model ... --category logic
  
  # 导出 JSON 报告
  python cli.py --model ... --report json --output result.json
        """
    )
    
    # 模型配置
    model_group = parser.add_argument_group("模型配置")
    model_group.add_argument(
        "--model", "-m",
        default="dummy",
        help="模型名称（HuggingFace模型名或API模型名）"
    )
    model_group.add_argument(
        "--api-key",
        help="API密钥（用于OpenAI兼容API）"
    )
    model_group.add_argument(
        "--base-url",
        help="API基础URL（用于第三方服务如Kimi、DeepSeek）"
    )
    model_group.add_argument(
        "--device",
        default="auto",
        help="运行设备（cuda/cpu/auto），默认auto"
    )
    
    # 测试配置
    test_group = parser.add_argument_group("测试配置")
    test_group.add_argument(
        "--quick", "-q",
        action="store_true",
        help="快速模式（随机5道题）"
    )
    test_group.add_argument(
        "--num", "-n",
        type=int,
        help="测试题目数量"
    )
    test_group.add_argument(
        "--category", "-c",
        choices=["logic", "language", "math", "common_sense", "creativity", "ethics", "meta"],
        help="只测试特定类别"
    )
    test_group.add_argument(
        "--difficulty",
        type=int,
        choices=[1, 2, 3, 4],
        help="只测试特定难度（1-简单 2-中等 3-困难 4-专家）"
    )
    test_group.add_argument(
        "--json", "-j",
        help="从JSON文件加载自定义题目"
    )
    test_group.add_argument(
        "--shuffle",
        action="store_true",
        help="打乱题目顺序"
    )
    test_group.add_argument(
        "--delay",
        type=float,
        default=0,
        help="题目间隔延迟（秒）"
    )
    
    # 输出配置
    output_group = parser.add_argument_group("输出配置")
    output_group.add_argument(
        "--report", "-r",
        choices=["console", "json", "md", "markdown", "all"],
        default="console",
        help="报告格式"
    )
    output_group.add_argument(
        "--output", "-o",
        help="输出文件路径"
    )
    output_group.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="详细输出"
    )
    output_group.add_argument(
        "--no-color",
        action="store_true",
        help="禁用彩色输出"
    )
    
    # 生成参数
    gen_group = parser.add_argument_group("生成参数")
    gen_group.add_argument(
        "--temperature", "-t",
        type=float,
        default=0.7,
        help="生成温度（0-1）"
    )
    gen_group.add_argument(
        "--max-tokens",
        type=int,
        default=2048,
        help="最大生成token数"
    )
    
    return parser


def load_model(args):
    """根据参数加载模型"""
    
    # 虚拟模型
    if args.model == "dummy":
        print("使用虚拟模型进行演示...")
        return DummyModel("demo", capability_level="high")
    
    # API 模型
    if args.api_key or args.base_url:
        api_key = args.api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("错误: 使用API模型需要提供 --api-key 或设置 OPENAI_API_KEY 环境变量")
            sys.exit(1)
        
        print(f"加载API模型: {args.model}")
        return OpenAIModel(
            model_name=args.model,
            api_key=api_key,
            base_url=args.base_url,
        )
    
    # HuggingFace 模型
    print(f"加载HuggingFace模型: {args.model}")
    print("这可能需要几分钟时间下载模型...")
    return HuggingFaceModel(
        model_name=args.model,
        device=args.device,
    )


def load_question_bank(args):
    """加载题目库"""
    bank = QuestionBank()
    
    if args.json:
        # 从JSON加载
        print(f"从 {args.json} 加载自定义题目...")
        bank.load_from_json(args.json)
    else:
        # 使用内置题目
        from ai_test_suite.questions.builtin import get_builtin_questions
        bank.add_many(get_builtin_questions())
    
    return bank


def create_reporters(args):
    """创建报告生成器"""
    reporters = []
    
    if args.report in ("console", "all"):
        reporters.append(ConsoleReporter(
            verbose=args.verbose,
            use_color=not args.no_color
        ))
    
    if args.report in ("json", "all"):
        reporters.append(("json", JSONReporter()))
    
    if args.report in ("md", "markdown", "all"):
        reporters.append(("md", MarkdownReporter()))
    
    return reporters


def main():
    parser = create_parser()
    args = parser.parse_args()
    
    print("=" * 60)
    print("🤖 AI综合能力测试工具")
    print("=" * 60)
    
    # 加载模型
    try:
        model = load_model(args)
    except Exception as e:
        print(f"加载模型失败: {e}")
        sys.exit(1)
    
    # 加载题目库
    bank = load_question_bank(args)
    print(f"题目库加载完成: {len(bank)} 道题目")
    
    # 创建测试运行器
    runner = TestRunner(
        model=model,
        question_bank=bank,
        evaluator=RuleBasedEvaluator(),
        temperature=args.temperature,
        max_tokens=args.max_tokens,
    )
    
    # 运行测试
    print("\n开始测试...\n")
    
    try:
        if args.quick:
            num = args.num or 5
            result = runner.run_quick_test(num_questions=num)
        elif args.category:
            num = args.num
            result = runner.run_category_test(args.category, num_questions=num)
        else:
            result = runner.run(
                categories=[args.category] if args.category else None,
                difficulties=[args.difficulty] if args.difficulty else None,
                shuffle=args.shuffle,
                limit=args.num,
                delay=args.delay,
            )
    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # 生成报告
    reporters = create_reporters(args)
    
    for rep in reporters:
        if isinstance(rep, tuple):
            fmt, reporter = rep
            output_path = args.output
            if output_path and fmt == "json":
                output_path = output_path.replace(".md", ".json").replace(".txt", ".json")
                if not output_path.endswith(".json"):
                    output_path += ".json"
            elif output_path and fmt in ("md", "markdown"):
                output_path = output_path.replace(".json", ".md").replace(".txt", ".md")
                if not output_path.endswith(".md"):
                    output_path += ".md"
            
            reporter.report(result, output_path)
        else:
            rep.report(result)
    
    print("\n✅ 测试完成!")


if __name__ == "__main__":
    main()
