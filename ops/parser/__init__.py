"""
📄 Datasheet 解析器
Datasheet Parser

功能:
- PDF 解析
- 参数提取
- 中文解读生成
"""
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import re


@dataclass
class ParsedDatasheet:
    """解析后的 Datasheet"""
    part_number: str
    manufacturer: str
    description: str
    specifications: Dict[str, str]
    package: str
    datasheet_url: str
    summary: str  # 中文摘要


class DatasheetParser:
    """Datasheet 解析器"""
    
    def __init__(self):
        self.pdf_available = False
        self._check_pdf_libs()
    
    def _check_pdf_libs(self):
        """检查 PDF 库是否可用"""
        try:
            import pdfplumber
            self.pdf_available = True
        except ImportError:
            print("⚠️ pdfplumber 未安装，PDF解析功能受限")
    
    async def parse_file(self, file_path: str) -> Optional[ParsedDatasheet]:
        """
        解析 Datasheet 文件
        
        Args:
            file_path: 文件路径 (PDF 或文本)
            
        Returns:
            解析结果
        """
        if file_path.endswith('.pdf') and self.pdf_available:
            return await self._parse_pdf(file_path)
        elif file_path.endswith(('.txt', '.md', '.csv')):
            return self._parse_text(file_path)
        else:
            raise ValueError(f"不支持的文件格式: {file_path}")
    
    async def _parse_pdf(self, file_path: str) -> Optional[ParsedDatasheet]:
        """解析 PDF 文件"""
        import pdfplumber
        
        try:
            with pdfplumber.open(file_path) as pdf:
                text = ""
                for page in pdf.pages[:5]:  # 只读前5页
                    text += page.extract_text() or ""
                
                return self._extract_info(text)
        except Exception as e:
            print(f"PDF 解析失败: {e}")
            return None
    
    def _parse_text(self, file_path: str) -> Optional[ParsedDatasheet]:
        """解析文本文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            return self._extract_info(text)
        except Exception as e:
            print(f"文本解析失败: {e}")
            return None
    
    def _extract_info(self, text: str) -> ParsedDatasheet:
        """从文本中提取信息"""
        text = text.lower()
        
        # 提取型号
        part_number = self._extract_part_number(text)
        
        # 提取厂商
        manufacturer = self._extract_manufacturer(text)
        
        # 提取描述
        description = self._extract_description(text)
        
        # 提取规格
        specifications = self._extract_specifications(text)
        
        # 提取封装
        package = self._extract_package(text)
        
        # 生成摘要
        summary = self._generate_summary(part_number, manufacturer, specifications)
        
        return ParsedDatasheet(
            part_number=part_number or "未知",
            manufacturer=manufacturer or "未知",
            description=description or "无描述",
            specifications=specifications,
            package=package or "未知",
            datasheet_url="",
            summary=summary
        )
    
    def _extract_part_number(self, text: str) -> Optional[str]:
        """提取型号"""
        # 常见型号模式
        patterns = [
            r'(stm32[f\d]+[a-z]*)',
            r'(esp32[-\w]*)',
            r'(ch340[ng]?)',
            r'(lm358[a-z]*)',
            r'(ams1117[-\w]*)',
            r'(ld1117[-\w]*)',
            r'(rp2040)',
            r'(atmega328[p]?)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1).upper()
        
        # 通用模式
        match = re.search(r'(?:part\s*(?:no|number)|型号)[:\s]*([a-z0-9\-]+)', text)
        if match:
            return match.group(1).upper()
        
        return None
    
    def _extract_manufacturer(self, text: str) -> Optional[str]:
        """提取厂商"""
        manufacturers = {
            "stmicroelectronics": "STMicroelectronics",
            "st.com": "STMicroelectronics",
            "espressif": "乐鑫科技",
            "wch.cn": "沁恒微电子",
            "ti.com": "Texas Instruments",
            "texas instruments": "Texas Instruments",
            "analog devices": "ADI",
            "onn": "安森美",
            "onsemi": "安森美",
            "nxp": "NXP",
            "microchip": "Microchip",
        }
        
        for pattern, name in manufacturers.items():
            if pattern in text:
                return name
        
        return None
    
    def _extract_description(self, text: str) -> str:
        """提取描述"""
        # 尝试提取第一段作为描述
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if 20 < len(line) < 200:
                return line
        
        return "无描述"
    
    def _extract_specifications(self, text: str) -> Dict[str, str]:
        """提取规格参数"""
        specs = {}
        
        # 电压范围
        voltage_match = re.search(r'(\d+\.?\d*)\s*[-~至]\s*(\d+\.?\d*)\s*v(?:dc)?', text)
        if voltage_match:
            specs["voltage"] = f"{voltage_match.group(1)}-{voltage_match.group(2)}V"
        
        # 电流
        current_match = re.search(r'(\d+\.?\d*)\s*(?:a|ma)', text)
        if current_match:
            specs["current"] = f"{current_match.group(1)}{'A' if 'a' in current_match.group(0) else 'mA'}"
        
        # 封装
        package_match = re.search(r'(?:package|封装)[:\s]*([a-z0-9\-]+)', text)
        if package_match:
            specs["package"] = package_match.group(1).upper()
        
        # 温度范围
        temp_match = re.search(r'(\-?\d+)\s*[:°]?\s*c.*?(\-?\d+)\s*[:°]?\s*c', text)
        if temp_match:
            specs["temperature"] = f"{temp_match.group(1)}°C ~ {temp_match.group(2)}°C"
        
        return specs
    
    def _extract_package(self, text: str) -> Optional[str]:
        """提取封装"""
        packages = [
            "LQFP-48", "LQFP-44", "LQFP-32",
            "SOP-8", "SOP-16", "SOIC-8",
            "QFN-20", "QFN-24", "QFN-32",
            "SOT-23", "SOT-223",
            "DIP-8", "DIP-16",
            "VSON-14", "VFQFPN-32",
        ]
        
        for pkg in packages:
            if pkg.lower() in text.lower():
                return pkg
        
        return None
    
    def _generate_summary(
        self,
        part_number: str,
        manufacturer: str,
        specifications: Dict[str, str]
    ) -> str:
        """生成中文摘要"""
        parts = []
        
        if manufacturer:
            parts.append(f"{manufacturer}")
        
        if part_number:
            parts.append(f"{part_number}")
        
        if specifications.get("voltage"):
            parts.append(f"{specifications['voltage']}电压")
        
        if specifications.get("current"):
            parts.append(f"{specifications['current']}电流")
        
        if specifications.get("package"):
            parts.append(f"{specifications['package']}封装")
        
        return " ".join(parts) if parts else "未知器件"
    
    async def parse_url(self, url: str) -> Optional[ParsedDatasheet]:
        """从 URL 解析 Datasheet"""
        # 使用 web_fetch 获取内容
        from . import web_fetch
        
        try:
            content = await web_fetch.fetch(url)
            return self._extract_info(content)
        except Exception as e:
            print(f"URL 解析失败: {e}")
            return None


# 便捷函数
async def parse_datasheet(file_path: str) -> Optional[ParsedDatasheet]:
    """解析 Datasheet"""
    parser = DatasheetParser()
    return await parser.parse_file(file_path)
