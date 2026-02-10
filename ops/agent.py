"""
AI Agent 主模块 - 基于多 Agent 协作的选型引擎
"""
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import json
import logging
import asyncio

from .config import Config
from .search import SearchEngine
from .parser import DatasheetParser
from .knowledge import VectorStore
from . import database

logger = logging.getLogger(__name__)


class PartCategory(Enum):
    """元器件分类"""
    POWER = "power"
    MCU = "mcu"
    SENSOR = "sensor"
    INTERFACE = "interface"
    ANALOG = "analog"
    DISCRETE = "discrete"
    MEMORY = "memory"
    PASSIVE = "passive"
    UNKNOWN = "unknown"


@dataclass
class PartSpec:
    """元器件规格"""
    voltage: Optional[str] = None
    current: Optional[str] = None
    power: Optional[str] = None
    package: Optional[str] = None
    temperature: Optional[str] = None
    speed: Optional[str] = None
    interface: Optional[str] = None
    additional: Dict[str, str] = field(default_factory=dict)


@dataclass
class SearchResult:
    """搜索结果"""
    part_number: str
    description: str
    manufacturer: str
    category: str
    specs: PartSpec
    price: Optional[float] = None
    stock: Optional[int] = None
    vendors: List[Dict] = field(default_factory=list)
    datasheet_url: Optional[str] = None
    compatibility_score: float = 0.0
    matched_constraints: List[str] = field(default_factory=list)
    alternatives: List[str] = field(default_factory=list)


@dataclass
class SelectionResult:
    """选型结果"""
    query: str
    recommended_parts: List[SearchResult]
    analysis_report: str
    compatibility_warnings: List[str]
    bom_items: List[Dict]
    generated_at: str


class Agent:
    """
    主选型 Agent
    
    负责协调搜索、分析、比较 Agent 完成选型任务
    """
    
    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config.load()
        self.search_engine = SearchEngine(self.config)
        self.datasheet_parser = DatasheetParser()
        self.knowledge_base = VectorStore(self.config)
        self._initialized = False
    
    async def initialize(self):
        """初始化 Agent"""
        self._initialized = True
        logger.info("Agent initialized (using built-in DB + async engines)")
    
    def parse_query(self, query: str) -> Dict[str, Any]:
        """
        解析自然语言查询
        
        Args:
            query: 自然语言描述，如"为 ESP32 项目找一个 3.3V LDO"
            
        Returns:
            解析后的结构化查询
        """
        parsed = {
            "original_query": query,
            "search_keywords": [],  # 用于数据库搜索的关键词
            "constraints": {},
            "category_hint": None,
            "target_voltage": None,
            "target_package": None,
            "target_current": None,
        }
        
        query_lower = query.lower()
        
        # 完整关键词映射 - 中英文
        keyword_mappings = {
            # 电压关键词
            "3.3v": "3.3V", "5v": "5V", "12v": "12V", "24v": "24V", "1.8v": "1.8V",
            # 电流关键词  
            "1a": "1A", "500ma": "500mA", "2a": "2A", "200ma": "200mA",
            # 封装关键词
            "sop-8": "SOP-8", "sop-16": "SOP-16", "qfn": "QFN", "bga": "BGA",
            "dip": "DIP", "soic": "SOIC", "sot-23": "SOT-23", "sot-223": "SOT-223",
            "lqfp-48": "LQFP-48", "qfn-24": "QFN-24", "vson-14": "VSON-14",
            # 品类关键词 - 英文
            "ldo": "ldo", "dc-dc": "dc-dc", "power": "power",
            "mcu": "mcu", "microcontroller": "mcu",
            "stm32": "stm32", "esp32": "esp32", "arduino": "arduino", "rp2040": "rp2040", "avr": "avr",
            "sensor": "sensor", "temperature": "temperature",
            "usb": "usb", "uart": "uart", "i2c": "i2c", "spi": "spi",
            "opamp": "opamp", "运放": "opamp", "amplifier": "amplifier", "双运放": "dual opamp",
            "mosfet": "mosfet", "三极管": "transistor", "flash": "flash",
            # 中文品类
            "单片机": "单片机", "传感器": "传感器", "电源": "电源",
        }
        
        # 品类映射 - 英文缩写到标准分类
        category_map = {
            "ldo": "power",
            "dc-dc": "power",
            "power": "power",
            "mcu": "mcu",
            "microcontroller": "mcu",
            "sensor": "sensor",
            "usb": "interface",
            "uart": "interface",
            "i2c": "interface",
            "spi": "interface",
            "opamp": "analog",
            "amplifier": "analog",
            "mosfet": "discrete",
            "flash": "memory",
            "memory": "memory",
            "transistor": "discrete",
        }
        
        # 提取关键词和参数
        for eng_kw, mapped_val in keyword_mappings.items():
            if eng_kw in query_lower:
                # 如果是参数类型，存储到对应字段
                if mapped_val in ["3.3V", "5V", "12V", "24V", "1.8V"]:
                    parsed["target_voltage"] = mapped_val
                elif mapped_val in ["1A", "500mA", "2A", "200mA"]:
                    parsed["target_current"] = mapped_val
                elif mapped_val in ["SOP-8", "SOP-16", "QFN", "SOT-223", "LQFP-48", "QFN-24", "VSON-14"]:
                    parsed["target_package"] = mapped_val
                # 品类关键词 - 转换为标准分类
                elif mapped_val in category_map:
                    parsed["category_hint"] = category_map[mapped_val]
                    parsed["search_keywords"].append(mapped_val)
                # 中文品类关键词
                if eng_kw == "单片机":
                    parsed["category_hint"] = "mcu"
                    parsed["search_keywords"].append("mcu")
                elif eng_kw == "传感器":
                    parsed["category_hint"] = "sensor"
                    parsed["search_keywords"].append("sensor")
                elif eng_kw == "运放":
                    parsed["category_hint"] = "analog"
                    parsed["search_keywords"].append("opamp")
        
        # 特殊处理常见型号
        model_patterns = ["stm32", "esp32", "ch340", "rp2040", "ld1117", "ams1117", "lm358", "ao3400"]
        for model in model_patterns:
            if model in query_lower:
                parsed["search_keywords"].append(model)
        
        # 如果没有品类关键词但有其他参数，搜索该参数作为关键词
        if not parsed["search_keywords"]:
            if parsed["target_voltage"]:
                parsed["search_keywords"].append(parsed["target_voltage"])
            if parsed["target_current"]:
                parsed["search_keywords"].append(parsed["target_current"])
        
        return parsed
    
    async def select(
        self, 
        query: str, 
        constraints: Optional[Dict] = None,
        top_k: int = 5
    ) -> SelectionResult:
        """
        主选型接口
        
        Args:
            query: 自然语言选型需求
            constraints: 额外约束条件
            top_k: 返回前 N 个推荐
            
        Returns:
            SelectionResult: 选型结果
        """
        try:
            if not self._initialized:
                await self.initialize()
        except Exception as init_error:
            logger.warning(f"Agent initialization warning: {init_error}")
            # 继续执行，使用内置数据库
        
        try:
            # 1. 解析查询
            parsed_query = self.parse_query(query)
            if constraints:
                parsed_query["constraints"].update(constraints)
            
            logger.info(f"Parsed query: {json.dumps(parsed_query, ensure_ascii=False)}")
            
            # 构建搜索关键词 - 使用解析后的关键词
            search_query = " ".join(parsed_query.get("search_keywords", [])) or parsed_query.get("original_query", "")
            
            # 构建搜索约束
            search_constraints = {}
            if parsed_query.get("target_voltage"):
                search_constraints["voltage"] = parsed_query["target_voltage"]
            if parsed_query.get("target_package"):
                search_constraints["package"] = parsed_query["target_package"]
            
            logger.info(f"Search query: '{search_query}', constraints: {search_constraints}")
            
            # 2. 搜索候选元器件 (增加错误处理)
            try:
                candidates = await self.search_engine.search(
                    query=search_query,
                    category=parsed_query.get("category_hint"),
                    constraints=search_constraints,
                    limit=top_k * 3
                )
            except Exception as search_error:
                logger.error(f"Search failed: {search_error}")
                candidates = []
            
            # 3. 分析与排序
            results = await self._analyze_and_rank(candidates, parsed_query)
            
            # 4. 获取替代料
            for result in results:
                try:
                    alternatives = await self.search_engine.get_alternatives(result.part_number)
                    result.alternatives = [a["part_number"] for a in alternatives[:3]]
                except Exception as alt_error:
                    logger.debug(f"Could not fetch alternatives: {alt_error}")
            
            # 5. 生成分析报告
            report = self._generate_report(results[:top_k], query)
            
            # 6. 生成 BOM
            bom = self._generate_bom(results[:top_k])
            
            return SelectionResult(
                query=query,
                recommended_parts=results[:top_k],
                analysis_report=report,
                compatibility_warnings=self._check_compatibility(results[:top_k], parsed_query),
                bom_items=bom,
                generated_at=self._timestamp()
            )
            
        except Exception as e:
            logger.error(f"Selection failed: {e}")
            # 返回空结果而不是崩溃
            return SelectionResult(
                query=query,
                recommended_parts=[],
                analysis_report=f"❌ 选型失败: {str(e)}\n\n请尝试简化搜索关键词。",
                compatibility_warnings=[],
                bom_items=[],
                generated_at=self._timestamp()
            )
    
    async def _analyze_and_rank(
        self, 
        candidates: List[Dict], 
        query: Dict
    ) -> List[SearchResult]:
        """分析并排序候选元器件"""
        results = []
        
        for candidate in candidates:
            specs_dict = candidate.get("specs", {})
            specs = self._parse_specs_dict(specs_dict)
            
            # 获取价格信息
            price_info = await self.search_engine.compare_prices(candidate.get("part_number", ""))
            price = price_info.get("best_price")
            stock = price_info.get("total_stock", 0)
            
            result = SearchResult(
                part_number=candidate.get("part_number", ""),
                description=candidate.get("description", ""),
                manufacturer=candidate.get("manufacturer", ""),
                category=candidate.get("category", ""),
                specs=specs,
                price=price,
                stock=stock,
                vendors=candidate.get("prices", []),
                datasheet_url=None,
            )
            
            # 计算兼容性分数
            result.compatibility_score = self._calculate_compatibility(result, query)
            result.matched_constraints = self._find_matched_constraints(result, query)
            
            results.append(result)
        
        # 按分数排序
        results.sort(key=lambda x: x.compatibility_score, reverse=True)
        
        return results
    
    def _parse_specs_dict(self, specs_dict: Dict) -> PartSpec:
        """解析规格字典"""
        return PartSpec(
            voltage=specs_dict.get("voltage"),
            current=specs_dict.get("current"),
            power=specs_dict.get("power"),
            package=specs_dict.get("package"),
            temperature=specs_dict.get("temperature"),
            speed=specs_dict.get("speed"),
            interface=specs_dict.get("interface"),
            additional={k: v for k, v in specs_dict.items() 
                       if k not in ["voltage", "current", "power", "package", 
                                   "temperature", "speed", "interface"]}
        )
    
    def _calculate_compatibility(self, result: SearchResult, query: Dict) -> float:
        """计算兼容性分数"""
        score = 0.5  # 基础分
        
        target_v = (query.get("target_voltage", "") or "").upper()
        target_p = (query.get("target_package", "") or "").upper()
        target_c = (query.get("target_current", "") or "")
        
        # 电压匹配 (最重要)
        if result.specs.voltage and target_v:
            if target_v in result.specs.voltage.upper():
                score += 0.3
            elif "3.3V" in target_v and "3.3" in result.specs.voltage:
                score += 0.3
        
        # 封装匹配
        if result.specs.package and target_p:
            if target_p in result.specs.package.upper():
                score += 0.2
        
        # 电流匹配
        if result.specs.current and target_c:
            if target_c.upper() in result.specs.current.upper():
                score += 0.1
        
        # 库存充足加分
        if result.stock and result.stock > 10000:
            score += 0.1
        elif result.stock and result.stock > 1000:
            score += 0.05
        
        return min(score, 1.0)
    
    def _find_matched_constraints(self, result: SearchResult, query: Dict) -> List[str]:
        """找出匹配的约束条件"""
        matched = []
        
        if result.specs.voltage and query.get("target_voltage"):
            if query["target_voltage"].upper() in result.specs.voltage.upper():
                matched.append(f"✓ 电压: {result.specs.voltage}")
        
        if result.specs.package and query.get("target_package"):
            if query["target_package"].upper() in result.specs.package.upper():
                matched.append(f"✓ 封装: {result.specs.package}")
        
        if result.specs.current and query.get("target_current"):
            if query["target_current"].upper() in result.specs.current.upper():
                matched.append(f"✓ 电流: {result.specs.current}")
        
        return matched
    
    def _generate_report(self, results: List[SearchResult], query: str) -> str:
        """生成选型分析报告"""
        report_lines = [
            f"## 📊 选型报告",
            f"",
            f"**查询需求**: {query}",
            f"**推荐数量**: {len(results)} 款器件",
            f"",
        ]
        
        if not results:
            report_lines.append("未找到匹配的元器件，请尝试放宽搜索条件。")
            return "\n".join(report_lines)
        
        for i, result in enumerate(results, 1):
            price_str = f"¥{result.price:.2f}" if result.price else "暂无报价"
            stock_str = f"{result.stock:,}" if result.stock else "未知"
            
            report_lines.extend([
                f"### 🔹 {i}. {result.part_number}",
                f"",
                f"| 厂商 | {result.manufacturer} |",
                f"| 描述 | {result.description} |",
                f"| 电压 | {result.specs.voltage or 'N/A'} |",
                f"| 电流 | {result.specs.current or 'N/A'} |",
                f"| 封装 | {result.specs.package or 'N/A'} |",
                f"| 价格 | {price_str} |",
                f"| 库存 | {stock_str} |",
                f"| 匹配度 | {result.compatibility_score:.0%} |",
                f"",
            ])
            
            if result.matched_constraints:
                report_lines.append("**匹配条件:**")
                for c in result.matched_constraints:
                    report_lines.append(f"  - {c}")
                report_lines.append("")
            
            if result.alternatives:
                report_lines.append(f"**替代料:** `{', '.join(result.alternatives)}`")
                report_lines.append("")
            
            report_lines.append("---")
            report_lines.append("")
        
        return "\n".join(report_lines)
    
    def _check_compatibility(self, results: List[SearchResult], query: Dict) -> List[str]:
        """检查兼容性问题"""
        warnings = []
        
        for result in results:
            # 检查电压范围
            if result.specs.voltage:
                if "-" in result.specs.voltage or "~" in result.specs.voltage:
                    warnings.append(f"⚠️ {result.part_number}: 输入电压范围较宽，需注意实际使用场景")
            
            # 检查封装兼容性
            if result.specs.package:
                if "module" in result.specs.package.lower():
                    warnings.append(f"📦 {result.part_number}: 为模块产品，需注意安装方式")
        
        return warnings
    
    def _generate_bom(self, results: List[SearchResult]) -> List[Dict]:
        """生成 BOM 清单"""
        bom = []
        
        for i, result in enumerate(results, 1):
            bom.append({
                "part_number": result.part_number,
                "manufacturer": result.manufacturer,
                "quantity": 1,
                "reference": f"U{i}",
                "description": result.description,
                "price_estimate": result.price,
            })
        
        return bom
    
    def _timestamp(self) -> str:
        """生成时间戳"""
        from datetime import datetime
        return datetime.utcnow().isoformat() + "Z"


# 便捷函数
def create_agent(config_path: Optional[str] = None) -> Agent:
    """创建 Agent 实例"""
    config = Config.load(config_path)
    return Agent(config)


# 同步版本的选型函数 (方便简单使用)
def quick_select(query: str, top_k: int = 5) -> SelectionResult:
    """
    快速选型 (同步版本)
    
    Args:
        query: 自然语言查询
        top_k: 返回结果数量
        
    Returns:
        选型结果
    """
    import asyncio
    
    agent = Agent()
    
    # 检查是否已在事件循环中
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # 在已有循环中，创建新任务
            async def do_select():
                await agent.initialize()
                return await agent.select(query, top_k=top_k)
            return asyncio.run_coroutine_threadsafe(do_select(), loop).result()
    except RuntimeError:
        # 无运行中的循环，直接使用 run
        pass
    
    return asyncio.run(agent.select(query, top_k=top_k))
