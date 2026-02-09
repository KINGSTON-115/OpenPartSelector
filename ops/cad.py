"""
🔌 CAD库集成模块 - 解决工程师最大痛点之一！
SamacSys / Ultra Librarian / SnapMagic 集成
一站式下载 Symbol / Footprint / 3D Model
"""
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import re

# ==================== CAD库资源 ====================

CAD_LIBRARIES = {
    "samacsys": {
        "name": "SamacSys",
        "url": "https://www.samacsys.com",
        "free": True,
        "formats": ["Altium", "KiCad", "Eagle", "CircuitMaker", "Cadence", "PADS"],
        "description": "完全免费的CAD库，120万+器件",
        "api_url": "https://api.samacsys.com"
    },
    "ultra_librarian": {
        "name": "ultra_librarian",
        "url": "https://www.ultralibrarian.com",
        "free": True,
        "formats": ["Altium", "KiCad", "Eagle", "CircuitMaker", "Cadence", "PADS", "Mentor"],
        "description": "300万+ CAD库，支持所有主流EDA",
        "api_url": "https://api.ultralibrarian.com"
    },
    "snapmagic": {
        "name": "SnapMagic (原SnapEDA)",
        "url": "https://www.snapmagic.com",
        "free": True,
        "formats": ["Altium", "KiCad", "Eagle", "CircuitMaker"],
        "description": "百万级符号/封装/3D模型",
        "api_url": "https://api.snapmagic.com"
    },
    "kicad_packages": {
        "name": "KiCad 官方库",
        "url": "https://gitlab.com/kicad/libraries",
        "free": True,
        "formats": ["KiCad"],
        "description": "KiCad官方符号/封装库，持续更新",
        "api_url": "https://api.kicad.org"
    },
    "grabcad": {
        "name": "GrabCAD",
        "url": "https://grabcad.com",
        "free": True,
        "formats": ["STEP", "IGES", "SolidWorks"],
        "description": "机械3D模型库，可导出为PCB 3D",
        "api_url": None
    }
}

# ==================== 常见器件CAD信息 ====================

KNOWN_CAD_PARTS = {
    "STM32F103C8T6": {
        "samacsys": "https://www.samacsys.com/st-microelectronics/STM32F103C8T6",
        "ultra_librarian": "https://www.ultralibrarian.com/st/STM32F103C8T6",
        "packages": ["LQFP-48"],
        "symbol": "Available",
        "footprint": "Available", 
        "model_3d": "Available"
    },
    "ESP32-WROOM-32": {
        "samacsys": "https://www.samacsys.com/espressif/ESP32-WROOM-32",
        "ultra_librarian": None,
        "packages": ["Module"],
        "symbol": "Available",
        "footprint": "Available",
        "model_3d": "Available"
    },
    "CH340G": {
        "samacsys": "https://www.samacsys.com/wch/CH340G",
        "ultra_librarian": "https://www.ultralibrarian.com/wch/CH340G",
        "packages": ["SOP-16"],
        "symbol": "Available",
        "footprint": "Available",
        "model_3d": "Available"
    },
    "AMS1117-3.3": {
        "samacsys": "https://www.samacsys.com/advanced-monolithic/AMS1117",
        "ultra_librarian": None,
        "packages": ["SOT-223"],
        "symbol": "Available",
        "footprint": "Available",
        "model_3d": "Available"
    },
    "LM358": {
        "samacsys": "https://www.samacsys.com/texas-instruments/LM358",
        "ultra_librarian": "https://www.ultralibrarian.com/ti/LM358",
        "packages": ["SOIC-8", "DIP-8"],
        "symbol": "Available",
        "footprint": "Available",
        "model_3d": "Available"
    },
    "NE555": {
        "samacsys": "https://www.samacsys.com/texas-instruments/NE555",
        "ultra_librarian": "https://www.ultralibrarian.com/ti/NE555",
        "packages": ["DIP-8", "SOIC-8"],
        "symbol": "Available",
        "footprint": "Available",
        "model_3d": "Available"
    },
    "LD1117V33": {
        "samacsys": "https://www.samacsys.com/st-microelectronics/LD1117",
        "ultra_librarian": "https://www.ultralibrarian.com/st/LD1117",
        "packages": ["SOT-223", "TO-220"],
        "symbol": "Available",
        "footprint": "Available",
        "model_3d": "Available"
    }
}


@dataclass
class CADResource:
    """CAD资源信息"""
    part_number: str
    library: str
    library_url: str
    formats: List[str]
    symbol: str  # Available/Not Available
    footprint: str
    model_3d: str
    download_url: str


class CADLibrary集成:
    """CAD库集成器 - 一站式获取所有CAD资源"""
    
    def __init__(self):
        self.libraries = CAD_LIBRARIES
        self.known_parts = KNOWN_CAD_PARTS
    
    def search_part(self, part_number: str) -> List[Dict]:
        """
        搜索器件的CAD资源
        
        Args:
            part_number: 器件型号
            
        Returns:
            可用CAD资源列表
        """
        results = []
        part_normalized = part_number.upper()
        
        # 1. 检查已知器件
        for known_part, info in self.known_parts.items():
            if (part_normalized in known_part.upper() or 
                known_part.upper() in part_normalized):
                
                for lib_name, lib_url in [("SamacSys", info.get("samacsys")),
                                         ("ultra_librarian", info.get("ultra_librarian"))]:
                    if lib_url:
                        results.append({
                            "library": lib_name,
                            "url": lib_url,
                            "part_number": known_part,
                            "packages": info["packages"],
                            "formats": self.libraries[lib_name.lower()]["formats"],
                            "status": {
                                "symbol": info["symbol"],
                                "footprint": info["footprint"],
                                "model_3d": info["model_3d"]
                            }
                        })
        
        # 2. 生成搜索链接
        if not results:
            for lib_name, lib_info in self.libraries.items():
                if lib_info["api_url"]:
                    search_url = f"{lib_info['url']}/search?q={part_number}"
                else:
                    search_url = f"{lib_info['url']}"
                
                results.append({
                    "library": lib_info["name"],
                    "url": search_url,
                    "part_number": part_number,
                    "packages": "Unknown",
                    "formats": lib_info["formats"],
                    "status": "请访问链接下载"
                })
        
        return results
    
    def get_download_links(self, part_number: str, cad_format: str) -> List[Dict]:
        """
        获取指定CAD格式的下载链接
        
        Args:
            part_number: 器件型号
            cad_format: CAD格式 (Altium/KiCad/Eagle)
            
        Returns:
            下载链接列表
        """
        resources = self.search_part(part_number)
        results = []
        
        for r in resources:
            if cad_format in r["formats"]:
                results.append({
                    "library": r["library"],
                    "url": r["url"],
                    "format": cad_format
                })
        
        return results
    
    def check_availability(self, part_number: str) -> Dict:
        """
        检查器件的CAD资源可用性
        
        Returns:
            可用性报告
        """
        resources = self.search_part(part_number)
        
        report = {
            "part_number": part_number,
            "total_resources": len(resources),
            "libraries": [],
            "overall_status": "Unknown"
        }
        
        available_count = 0
        for r in resources:
            status = r.get("status", {})
            if isinstance(status, dict):
                if status.get("footprint") == "Available":
                    available_count += 1
            
            report["libraries"].append({
                "name": r["library"],
                "url": r["url"],
                "packages": r.get("packages", "Unknown"),
                "symbol": status.get("symbol", "N/A") if isinstance(status, dict) else status,
                "footprint": status.get("footprint", "N/A") if isinstance(status, dict) else "N/A",
                "model_3d": status.get("model_3d", "N/A") if isinstance(status, dict) else "N/A"
            })
        
        if available_count > 0:
            report["overall_status"] = "Available"
        elif len(resources) > 0:
            report["overall_status"] = "Check Manually"
        else:
            report["overall_status"] = "Not Found"
        
        return report
    
    def get_kicad_footprint(self, package: str) -> Dict:
        """
        获取KiCad封装信息
        
        Args:
            package: 封装类型 (如 SOP-8, QFN-24)
            
        Returns:
            KiCad封装信息
        """
        # KiCad官方封装库
        KICAD_FOOTPRINTS = {
            "SOP-8": {
                "lib": "Package_SO",
                "name": "SO-8_3.9x4.9mm_P1.27mm",
                "url": "https://kicad.org/footprints/SO-8"
            },
            "SOP-16": {
                "lib": "Package_SO",
                "name": "SO-16_3.9x9.9mm_P1.27mm",
                "url": "https://kicad.org/footprints/SO-16"
            },
            "QFN-24": {
                "lib": "Package_DFN_QFN",
                "name": "QFN-24-1EP_4x4mm_P0.5mm_EP2.6x2.6mm",
                "url": "https://kicad.org/footprints/QFN"
            },
            "LQFP-48": {
                "lib": "Package_QFP",
                "name": "LQFP-48_7x7mm_P0.5mm",
                "url": "https://kicad.org/footprints/LQFP"
            },
            "SOT-23-5": {
                "lib": "Package_SOT",
                "name": "SOT-23-5",
                "url": "https://kicad.org/footprints/SOT-23"
            },
            "SOT-223": {
                "lib": "Package_SOT",
                "name": "SOT-223-3Lead_TabPin2",
                "url": "https://kicad.org/footprints/SOT-223"
            },
            "DIP-8": {
                "lib": "Package_DIP",
                "name": "DIP-8_W7.62mm_LongPads",
                "url": "https://kicad.org/footprints/DIP"
            },
            "ESP-12F": {
                "lib": "RF_Module",
                "name": "ESP-12F",
                "url": "https://kicad.org/footprints/RF_Module"
            }
        }
        
        package_upper = package.upper()
        for key, info in KICAD_FOOTPRINTS.items():
            if key in package_upper:
                return {
                    "package": package,
                    "kicad_lib": info["lib"],
                    "kicad_name": info["name"],
                    "url": info["url"],
                    "source": "KiCad Official Library"
                }
        
        return {
            "package": package,
            "kicad_lib": None,
            "kicad_name": None,
            "url": "https://kicad.org/libraries/",
            "source": "请在KiCad封装管理器中搜索",
            "suggestion": f"尝试搜索: {package}"
        }


# ==================== 便捷函数 ====================

def search_cad_library(part_number: str) -> List[Dict]:
    """搜索器件的CAD库资源"""
    engine = CADLibrary集成()
    return engine.search_part(part_number)


def check_cad_availability(part_number: str) -> Dict:
    """检查CAD资源可用性"""
    engine = CADLibrary集成()
    return engine.check_availability(part_number)


def get_kicad_footprint(package: str) -> Dict:
    """获取KiCad封装"""
    engine = CADLibrary集成()
    return engine.get_kicad_footprint(package)


def get_download_links(part_number: str, format: str) -> List[Dict]:
    """获取下载链接"""
    engine = CADLibrary集成()
    return engine.get_download_links(part_number, format)
