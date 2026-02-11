OpenPartSelector API v1.1.34
===

## 概述

OpenPartSelector 提供 Python API 和 REST API 两种使用方式。

## Python API

### 快速开始

```python
from openpartselector import Agent, quick_select, search_components
```

### 核心类

#### Agent

```python
from openpartselector import Agent

agent = Agent()

# 自然语言选型
result = await agent.select(
    query="为 ESP32 项目找一个 3.3V LDO，输出电流 500mA",
    constraints={"package": "SOP-8"},
    top_k=5
)

print(result.recommended_parts)
print(result.analysis_report)
```

### 快速函数

#### quick_select

```python
from openpartselector import quick_select

# 快速选型 (同步)
result = quick_select("STM32F103C8T6", top_k=3)

# 返回 SelectionResult 对象
print(result.query)              # 查询语句
print(result.recommended_parts)  # 推荐器件列表
print(result.analysis_report)    # 分析报告
```

### 搜索功能

#### search_components

```python
from openpartselector import search_components

# 搜索元器件
results = search_components(query="LDO 3.3V", limit=10)

for comp in results:
    print(f"{comp['part_number']}: {comp['description']}")
```

#### get_price_comparison

```python
from openpartselector import get_price_comparison

# 价格对比
prices = get_price_comparison("STM32F103C8T6")
# 返回各平台价格
```

#### get_alternatives

```python
from openpartselector import get_alternatives

# 国产替代
alts = get_alternatives("STM32F103C8T6")
# 返回替代器件列表
```

### 嘉立创功能

```python
from openpartselector import search_jlc, calculate_jlc_smt

# 搜索立创商城
results = search_jlc("ESP32")

# SMT 费用计算
smt_cost = calculate_jlc_smt(bom_dict)
```

### 锦上添花功能

```python
from openpartselector import (
    find_alternatives,
    get_circuit_template,
    get_datasheet_summary,
    calculate_resistor_for_led,
    calculate_voltage_divider
)

# 国产替代
alts = find_alternatives("STM32F103C8T6")

# 电路模板
tmpl = get_circuit_template("esp32_minimal")

# Datasheet 摘要
summary = get_datasheet_summary("STM32F103C8T6")

# 电阻计算
led_res = calculate_resistor_for_led(voltage=5.0, led_voltage=2.0, led_current=0.02)
```

### BOM 功能

```python
from openpartselector import analyze_bom_full, quick_bom_check

# 完整 BOM 分析
result = analyze_bom_full([
    {"part_number": "STM32F103C8T6", "quantity": 10},
    {"part_number": "LD1117V33", "quantity": 10}
])

# 快速 BOM 检查
check = quick_bom_check(bom_dict)
```

## REST API

### 启动服务器

```bash
# 安装
pip install -r requirements.txt

# 启动 API 服务器
uvicorn api.main:app --reload --port 8000

# 访问文档
http://localhost:8000/docs
```

### API 端点

#### 选型查询
| 方法 | 端点 | 说明 |
|------|------|------|
| POST | `/api/v1/select` | 自然语言选型 |
| GET | `/api/v1/parts/{part_number}` | 查询元器件详情 |

**请求示例:**
```bash
curl -X POST "http://localhost:8000/api/v1/select" \
  -H "Content-Type: application/json" \
  -d '{"query": "为 ESP32 项目找一个 3.3V LDO", "top_k": 5}'
```

#### 搜索引擎
| 方法 | 端点 | 说明 |
|------|------|------|
| GET | `/api/v1/search` | 搜索元器件 |
| GET | `/api/v1/price/{part_number}` | 比价查询 |

#### 文档解析
| 方法 | 端点 | 说明 |
|------|------|------|
| POST | `/api/v1/parse/datasheet` | 解析 datasheet |

#### BOM 管理
| 方法 | 端点 | 说明 |
|------|------|------|
| POST | `/api/v1/bom/generate` | 生成 BOM |
| GET | `/api/v1/bom/{bom_id}` | 获取 BOM |

### 响应格式

```json
{
  "success": true,
  "data": {
    "query": "ESP32 LDO",
    "results": [...],
    "total": 5
  }
}
```

## CLI 工具

```bash
# 自然语言选型查询
ops select "为 ESP32 项目找一个 3.3V LDO，输出电流 500mA"

# 多平台比价
ops price "STM32F103C8T6"

# 解析 datasheet
ops parse datasheet.pdf

# 生成 BOM 清单
ops bom --parts 'LD1117,ESP32'

# 对比元器件
ops compare 'LD1117' 'AMS1117'
```

## 错误处理

```python
from openpartselector import Agent, SelectionError

try:
    result = agent.select("不存在的器件")
except SelectionError as e:
    print(f"选型失败: {e}")
```

## 版本信息

- **API 版本**: v1.1.34
- **Python 包版本**: 1.1.34
- **最后更新**: 2026-02-11
