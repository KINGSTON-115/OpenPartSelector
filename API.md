OpenPartSelector API
===

## 快速开始

```bash
# 安装
pip install -r requirements.txt

# 启动 API 服务器
uvicorn api.main:app --reload --port 8000

# 访问文档
http://localhost:8000/docs
```

## API 端点

### 选型查询
- `POST /api/v1/select` - 自然语言选型
- `GET /api/v1/parts/{part_number}` - 查询元器件详情

### 搜索引擎
- `GET /api/v1/search` - 搜索元器件
- `GET /api/v1/price/{part_number}` - 比价查询

### 文档解析
- `POST /api/v1/parse/datasheet` - 解析 datasheet

### BOM 管理
- `POST /api/v1/bom/generate` - 生成 BOM
- `GET /api/v1/bom/{bom_id}` - 获取 BOM
