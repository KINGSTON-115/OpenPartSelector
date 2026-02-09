# OpenPartSelector Examples

## API 使用示例

### Python API 示例

```python
from openpartselector import Agent, Config

# 创建 Agent
config = Config.load()
agent = Agent(config)

# 自然语言选型
result = await agent.select(
    query="为 Arduino 项目找一个 USB-UART 转换芯片",
    constraints={
        "voltage": "5V",
        "package": "TSSOP-20"
    }
)

print(result.analysis_report)
```

### 比价查询

```python
prices = await agent.search_engine.compare_prices("STM32F103C8T6")
print(f"最佳价格: {prices['best_price']}")
```

### BOM 生成

```python
bom = agent._generate_bom(results[:5])
for item in bom["items"]:
    print(f"{item['reference']}: {item['part_number']}")
```

---

## CLI 使用示例

### 选型查询

```bash
# 基础查询
python -m ops select "找一个 3.3V LDO，输出电流 500mA"

# 带约束查询
python -m ops select "STM32 单片机" --top 10
```

### 比价查询

```bash
python -m ops price "ESP32-WROOM"
python -m ops price "STM32F103C8T6" --quantity 100
```

### Datasheet 解析

```bash
python -m ops parse "datasheet.pdf"
python -m ops parse "https://example.com/datasheet.pdf"
```

### BOM 生成

```bash
# 从元器件列表生成
python -m ops bom --parts "LD1117-3.3,ESP32,CH340G"

# 从 JSON 文件生成
python -m ops bom --file circuit.json
```

---

## API 服务示例

### 启动服务

```bash
uvicorn api.main:app --reload --port 8000
```

### curl 调用示例

```bash
# 选型查询
curl -X POST "http://localhost:8000/api/v1/select" \
  -H "Content-Type: application/json" \
  -d '{"query": "找一个 3.3V LDO"}'

# 比价查询
curl "http://localhost:8000/api/v1/price/STM32F103C8T6"

# 生成 BOM
curl -X POST "http://localhost:8000/api/v1/bom/generate" \
  -H "Content-Type: application/json" \
  -d '{"parts": ["LD1117", "ESP32", "CH340G"]}'
```

---

## 配置文件示例

### config.yaml

```yaml
api_keys:
  openai: "sk-xxx"
  deepseek: "xxx"

search:
  max_results: 20
  timeout: 30

llm:
  default: "deepseek"
  temperature: 0.1

cache:
  enabled: true
  ttl_hours: 24
```
