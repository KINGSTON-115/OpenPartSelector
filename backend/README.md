# OpenPartSelector - 电子元器件在线搜索后端

## 架构设计

```
┌─────────────────────────────────────────────────────────────┐
│                    OpenPartSelector                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   ┌──────────────┐    ┌──────────────┐    ┌────────────┐  │
│   │ GitHub       │    │   Python     │    │   JSON     │  │
│   │ Actions      │───▶│   Scraper    │───▶│   API      │  │
│   │ (定时爬取)    │    │   (LCSC)     │    │   数据     │  │
│   └──────────────┘    └──────────────┘    └────────────┘  │
│           │                                        │       │
│           │                                        │       │
│           ▼                                        ▼       │
│   ┌──────────────┐                        ┌───────────┐ │
│   │  每6小时      │                        │  前端      │ │
│   │  自动更新     │                        │  fetch()   │ │
│   └──────────────┘                        └───────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 文件结构

```
OpenPartSelector/
├── backend/
│   ├── scraper.py           # LCSC 爬虫核心
│   └── requirements.txt     # Python 依赖
├── data/
│   └── parts.json           # 实时器件数据 (GitHub Actions 更新)
├── frontend/
│   └── index.html           # 在线搜索界面
└── .github/workflows/
    └── scrape.yml           # GitHub Actions 配置
```

## 快速开始

### 1. 本地运行爬虫

```bash
cd backend
pip install -r requirements.txt
python scraper.py
```

### 2. 启动本地服务器

```bash
# Python
python -m http.server 8080

# 或 Node.js
npx serve
```

### 3. 访问在线搜索

打开 `frontend/index.html` 或访问本地服务器

## 依赖

```
requests>=2.28.0
beautifulsoup4>=4.11.0
lxml>=4.9.0
```

## API 接口

### 获取所有器件

```bash
GET /data/parts.json
```

### 按关键词搜索

```bash
GET /data/parts.json?q=STM32
```

### 示例响应

```json
{
  "timestamp": "2026-02-09T14:30:00Z",
  "count": 150,
  "results": [
    {
      "part": "STM32F103C8T6",
      "mfr": "STMicroelectronics",
      "category": "MCU",
      "price": 0.95,
      "currency": "CNY",
      "stock": 15000,
      "package": "LQFP-48",
      "description": "ARM Cortex-M3 64KB Flash",
      "link": "https://www.lcsc.com/product-detail/STM32F103C8T6",
      "alternatives": ["GD32F103C8T6", "HK32F103C8T6"]
    }
  ]
}
```

## GitHub Actions 自动更新

- **触发**: 每 6 小时自动运行
- **手动触发**: GitHub Actions 页面点击 "Run workflow"
- **数据源**: LCSC (立创商城)

## 许可证

MIT License
