#!/usr/bin/env python3
"""
基础使用示例
演示 OpenPartSelector 的核心功能
"""

from openpartselector import Agent


def demo_basic_select():
    """基础选型查询演示"""
    print("=" * 50)
    print("基础选型查询演示")
    print("=" * 50)
    
    agent = Agent()
    
    # 初始化
    print("\n1. 初始化 Agent...")
    # agent.initialize()  # 需要 API key
    
    # 自然语言查询
    print("\n2. 执行自然语言查询...")
    query = "找一个 3.3V LDO，输出电流 500mA，封装 SOP-8"
    print(f"   查询: {query}")
    
    # 模拟结果
    mock_results = [
        {
            "part_number": "LD1117V33",
            "description": "LDO 3.3V 1A SOT-223",
            "manufacturer": "STMicroelectronics",
            "price": 0.50,
            "stock": 50000
        },
        {
            "part_number": "AMS1117-3.3",
            "description": "LDO 3.3V 1A SOT-223",
            "manufacturer": "Advanced Monolithic Systems",
            "price": 0.15,
            "stock": 100000
        },
        {
            "part_number": "ME6211C33",
            "description": "LDO 3.3V 500mA SOT-23-5",
            "manufacturer": "Microne",
            "price": 0.12,
            "stock": 80000
        }
    ]
    
    print("\n3. 推荐结果:")
    for i, part in enumerate(mock_results, 1):
        print(f"   {i}. {part['part_number']}")
        print(f"      描述: {part['description']}")
        print(f"      厂商: {part['manufacturer']}")
        print(f"      价格: ¥{part['price']}")
        print(f"      库存: {part['stock']}")
        print()


def demo_query_parsing():
    """查询解析演示"""
    print("\n" + "=" * 50)
    print("查询解析演示")
    print("=" * 50)
    
    agent = Agent()
    
    queries = [
        "找一个 3.3V LDO",
        "12V DC-DC 降压芯片",
        "ESP32 最小系统需要什么",
        "STM32F103C8T6 替代料",
        "USB 转串口芯片 5V"
    ]
    
    print("\n解析结果:")
    for query in queries:
        result = agent.parse_query(query)
        print(f"\n原始查询: {query}")
        print(f"  电压: {result.get('target_voltage', 'N/A')}")
        print(f"  封装: {result.get('target_package', 'N/A')}")
        print(f"  分类: {result.get('category_hint', 'N/A')}")


def demo_part_specs():
    """器件规格演示"""
    print("\n" + "=" * 50)
    print("器件规格演示")
    print("=" * 50)
    
    from ops.agent import PartSpec
    
    specs = [
        PartSpec(voltage="3.3V", current="1A", package="SOT-223"),
        PartSpec(voltage="5V", current="500mA", package="SOP-8"),
        PartSpec(voltage="12V", current="2A", package="TO-220"),
    ]
    
    print("\n器件规格:")
    for spec in specs:
        print(f"  电压: {spec.voltage}")
        print(f"  电流: {spec.current}")
        print(f"  封装: {spec.package}")
        print()


if __name__ == "__main__":
    demo_basic_select()
    demo_query_parsing()
    demo_part_specs()
    print("\n演示完成!")
