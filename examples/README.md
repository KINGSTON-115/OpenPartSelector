# OpenPartSelector 使用示例

本目录包含各种使用场景的示例代码。

## 快速示例

### 1. 基础选型查询

```python
from openpartselector import Agent

agent = Agent()

# 自然语言查询
result = agent.select("找一个 3.3V LDO，输出电流 500mA")
print(result.recommended_parts)
```

### 2. 批量 BOM 生成

```python
from ops.bom import BOMBuilder

bom = BOMBuilder()
bom.add_part("STM32F103C8T6", quantity=5)
bom.add_part("CH340N", quantity=5)
bom.add_part("AMS1117-3.3", quantity=5)

# 导出 CSV
bom.export_csv("bom.csv")

# 导出 Excel
bom.export_excel("bom.xlsx")
```

### 3. 国产替代查询

```python
from ops.features import find_alternatives

# 查找国产替代
alts = find_alternatives("STM32F103C8T6")
for alt in alts:
    print(f"{alt.name}: {alt.compatibility}% 兼容, ¥{alt.price}")
```

### 4. 立创商城搜索

```python
from ops.jlc import search_jlc

# 搜索器件
results = search_jlc("ESP32")
for r in results:
    print(f"{r.part_number}: ¥{r.price} (库存: {r.stock})")
```

### 5. CLI 使用

```bash
# 自然语言选型
ops select "ESP32 最小系统需要哪些器件"

# 价格对比
ops price "STM32F103C8T6"

# 生成 BOM
ops bom --add "LD1117:10" "ESP32:5"

# 导出 BOM
ops bom --export csv --file my_bom.csv
```

## 高级用法

### 自定义搜索约束

```python
from openpartselector import Agent, PartCriteria

agent = Agent()

criteria = PartCriteria(
    voltage="3.3V",
    current="500mA",
    package="SOP-8",
    price_max=2.0,
    in_stock=True
)

result = agent.select("LDO 稳压器", constraints=criteria)
```

### 批量查询

```python
from ops.database import PartDatabase

db = PartDatabase()

# 批量搜索
queries = ["STM32F103", "ESP32", "CH340N"]
results = db.batch_search(queries)

for q, parts in results.items():
    print(f"{q}: {len(parts)} 个结果")
```

### 导出格式

```python
from ops.bom import BOMBuilder

bom = BOMBuilder()
bom.add("STM32F_part103", quantity=10)

# 支持多种格式
bom.export_csv("bom.csv")
bom.export_excel("bom.xlsx")
bom.export_json("bom.json")
bom.export_markdown("bom.md")
```

## 示例文件

| 文件 | 说明 |
|------|------|
| `basic_usage.py` | 基础使用示例 |
| `batch_query.py` | 批量查询示例 |
| `bom_export.py` | BOM 导出示例 |
| `jlc_search.py` | 立创商城搜索示例 |
| `alternatives.py` | 国产替代查询示例 |
