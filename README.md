# OpenPartSelector 🤖🔌

**AI-Driven Open-Source Electronic Component Selection Engine**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](CONTRIBUTING.md)

> **核心价值**：用 AI Agent 自动化解决电子工程师的元器件选型痛点——搜索、对比、验证、一键生成采购清单

---

## 🎓 中国特色功能

### 嘉立创/立创商城集成
```python
from ops.jlc import search_jlc, calculate_jlc_smt

# 🎓 学生常用器件搜索
results = search_jlc('ESP32')
# → 返回: 立创货号C14663, ¥9.8/10pcs, 库存8500
# → 直接生成采购链接

# 📐 封装查询 (嘉立创EDA)
fp = get_jlc_footprint('SOP-8')
# → 返回: JLC封装ID: SOP-8-3.9

# 🔧 SMT费用计算
smt = calculate_jlc_smt(bom)
# → 返回: 单面SMT ¥9.2 (80点起)
```

### 支持的器件
| 器件类型 | 型号 | 立创货号 | 价格/10pcs |
|----------|------|----------|------------|
| WiFi模块 | ESP-12F | C10047 | ¥7.50 |
| WiFi模块 | ESP32-C3 | C14663 | ¥9.80 |
| USB转串口 | CH340C | C10488 | ¥1.80 |
| 国产替代 | GD32F103 | C11449 | ¥8.50 |
| 时基电路 | NE555P | C8580 | ¥0.50 |

### 嘉立创EDA封装库
支持常用封装: SOP-8, SOT-223, LQFP-48, QFN-24, ESP-12F 等

| 痛点 | OpenPartSelector 方案 |
|------|------------------------|
| 📚 datasheet 晦涩难懂 | AI 自动解析关键参数，生成通俗解释 |
| 🔍 多平台比价耗时 | 一键查询 DigiKey/Mouser/LCSC/云汉价格与库存 |
| 🔄 兼容性问题难发现 | 自动验证封装、电压、电流兼容性 |
| 📝 选型文档繁琐 | 自动生成规格书、BOM 清单 |
| ⏰ 供应链风险 | 实时监控交期、停产状态 |

---

## 🏗️ 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                    OpenPartSelector Core                     │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │ Agent       │  │ Agent       │  │ Agent               │ │
│  │ Search 🔍   │→ │ Analyze 📊  │→ │ Compare 🔄         │ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
│         ↓                ↓                   ↓             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │           Multi-Source Data Integration Layer        │   │
│  │  DigiKey │ Mouser │ LCSC │ Octopart │ EasyEDA       │   │
│  └─────────────────────────────────────────────────────┘   │
│                           ↓                                 │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Vector Knowledge Base                   │   │
│  │  Datasheets │ App Notes │ Footprints │ Standards    │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 快速开始

### 安装

```bash
git clone https://github.com/KINGSTON-115/OpenPartSelector.git
cd OpenPartSelector
pip install -r requirements.txt
```

### 配置 API Keys

```bash
cp .env.example .env
# 编辑 .env 添加您的 API keys
```

### 使用 CLI

```bash
# 自然语言选型查询
python -m ops select "为 ESP32 项目找一个 3.3V LDO，输出电流 500mA，封装 SOP-8"

# 比价查询
python -m ops price "STM32F103C8T6"

# datasheet 解析
python -m ops parse "tps63000.pdf"

# 生成 BOM
python -m ops bom --file circuit.json
```

### Python API

```python
from openpartselector import Agent, PartCriteria

# 创建选型 Agent
agent = Agent()

# 自然语言查询
result = agent.select(
    query="为 Arduino 项目找一个 USB-UART 转换芯片",
    constraints={
        "voltage": "5V",
        "package": "TSSOP-20",
        "price_range": "<$2"
    }
)

print(result.recommended_parts)
print(result.compatibility_analysis)
```

---

## 📁 项目结构

```
OpenPartSelector/
├── ops/                          # 核心模块
│   ├── __init__.py
│   ├── agent.py                  # AI Agent 主逻辑
│   ├── search/                   # 搜索引擎
│   │   ├── digikey.py
│   │   ├── mouser.py
│   │   └── lcsc.py
│   ├── parser/                   # 文档解析
│   │   ├── datasheet.py
│   │   └── footprint.py
│   ├── knowledge/               # 知识库
│   │   ├── vector_store.py
│   │   └── embeddings.py
│   └── utils/
│       ├── config.py
│       └── logger.py
├── tests/                        # 测试用例
├── examples/                     # 示例脚本
├── docs/                         # 文档
├── scripts/                      # 工具脚本
├── config/                       # 配置文件
├── data/                         # 数据存储
├── prompts/                      # Prompt 模板
├── tools/                        # CLI 工具
├── requirements.txt
├── README.md
├── LICENSE
└── .env.example
```

---

## 🔧 支持的元器件类型

- **电源管理**: LDO, DC-DC, Charge Pump
- **微控制器**: MCU, FPGA, SoC
- **传感器**: 温度、湿度、加速度、陀螺仪
- **接口芯片**: USB, Ethernet, UART, I2C, SPI
- **模拟电路**: OpAmp, ADC, DAC
- **分立器件**: MOSFET, BJT, 二极管

---

## 🌐 集成平台

| 平台 | 状态 | 功能 |
|------|------|------|
| DigiKey | ✅ | 库存/价格/参数 |
| Mouser | ✅ | 库存/价格/参数 |
| LCSC | ✅ | 库存/价格/参数 |
| Octopart | 🔄 | 跨平台比价 |
| EasyEDA | 🔄 | 封装/原理图 |

---

## 🤝 贡献指南

欢迎贡献代码！请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。

### 贡献方式
- 🐛 报告 Bug
- 💡 提出新功能
- 📝 完善文档
- 🔧 提交 Pull Request

---

## 📄 许可证

MIT License - 开源商用皆可。

---

## 👨‍💻 作者

**Maintainer:** [KINGSTON-115](https://github.com/KINGSTON-115)

---

> **Built with AI Agents, for Engineers** 🛠️
