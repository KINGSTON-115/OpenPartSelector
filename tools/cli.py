#!/usr/bin/env python3
"""
OpenPartSelector CLI 入口
"""
import sys
import asyncio
from typing import Optional


async def main():
    """CLI 主入口"""
    import argparse
    from ops.config import Config
    from ops.agent import Agent
    
    parser = argparse.ArgumentParser(
        description="OpenPartSelector - AI 电子元器件智能选型引擎"
    )
    
    # 全局参数
    parser.add_argument(
        "--config", "-c",
        help="配置文件路径",
        default=None
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="详细输出"
    )
    
    # 子命令
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # select 命令
    select_parser = subparsers.add_parser("select", help="元器件选型查询")
    select_parser.add_argument(
        "query",
        help="自然语言查询，如：为 ESP32 项目找一个 3.3V LDO"
    )
    select_parser.add_argument(
        "--top", "-t",
        type=int,
        default=5,
        help="返回结果数量 (默认: 5)"
    )
    
    # price 命令
    price_parser = subparsers.add_parser("price", help="比价查询")
    price_parser.add_argument(
        "part_number",
        help="元器件型号，如：STM32F103C8T6"
    )
    
    # parse 命令
    parse_parser = subparsers.add_parser("parse", help="解析 datasheet")
    parse_parser.add_argument(
        "file",
        help="datasheet 文件路径或 URL"
    )
    
    # bom 命令
    bom_parser = subparsers.add_parser("bom", help="生成 BOM 清单")
    bom_parser.add_argument(
        "--file", "-f",
        help="电路文件路径 (JSON 格式)"
    )
    bom_parser.add_argument(
        "--parts", "-p",
        help="直接指定元器件型号 (逗号分隔)"
    )
    
    # search 命令
    search_parser = subparsers.add_parser("search", help="搜索元器件")
    search_parser.add_argument(
        "keyword",
        help="搜索关键词"
    )
    search_parser.add_argument(
        "--limit", "-l",
        type=int,
        default=10,
        help="结果数量"
    )
    
    args = parser.parse_args()
    
    # 加载配置
    config = Config.load(args.config)
    
    if args.verbose:
        import logging
        logging.basicConfig(level=logging.DEBUG)
    
    # 创建 Agent
    agent = Agent(config)
    
    try:
        if args.command == "select":
            result = await agent.select(
                query=args.query,
                top_k=args.top
            )
            print("\n" + "="*60)
            print("🎯 选型结果")
            print("="*60)
            print(f"\n📝 查询: {result.query}")
            print(f"📦 推荐数量: {len(result.recommended_parts)}")
            print("\n" + "-"*60)
            print(result.analysis_report)
            
        elif args.command == "price":
            prices = await agent.search_engine.compare_prices(args.part_number)
            print(f"\n📊 {args.part_number} 比价结果:")
            for p in prices.get("prices", []):
                print(f"  - {p}")
        
        elif args.command == "parse":
            from ops.parser import DatasheetParser
            parser_tool = DatasheetParser(config)
            result = await parser_tool.parse_file(args.file)
            print(f"\n📄 解析结果:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif args.command == "bom":
            from ops.utils import BomBuilder
            bom = BomBuilder()
            
            if args.parts:
                parts = [p.strip() for p in args.parts.split(",")]
                for part in parts:
                    bom.add_item(part_number=part)
            
            print("\n📋 BOM 清单:")
            print(json.dumps(bom.get_bom(), indent=2, ensure_ascii=False))
        
        elif args.command == "search":
            results = await agent.search_engine.search(
                query=args.keyword,
                limit=args.limit
            )
            print(f"\n🔍 搜索结果 ({len(results)} 个):")
            for r in results:
                print(f"  - {r.get('part_number')}: {r.get('description', 'N/A')}")
        
        else:
            parser.print_help()
    
    except Exception as e:
        print(f"\n❌ 错误: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    import json
    asyncio.run(main())
