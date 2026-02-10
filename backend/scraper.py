#!/usr/bin/env python3
"""
LCSC 电子元器件爬虫
定时从 LCSC 抓取器件数据，提供实时价格和库存查询
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import re
import logging
from datetime import datetime
from typing import List, Dict, Optional, Any
from urllib.parse import quote
from functools import wraps

# 配置
BASE_URL = "https://www.lcsc.com"
SEARCH_URL = f"{BASE_URL}/search"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
}

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# 重试配置
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds

# 热门搜索列表
POPULAR_PARTS = [
    "STM32F103C8T6",
    "GD32F103C8T6",
    "ESP32-WROOM-32",
    "ESP32-C3FH4",
    "CH340N",
    "CH340G",
    "LD1117V33",
    "AMS1117-3.3",
    "LM358",
    "SGM358",
    "AO3400",
    "2N7000",
    "IRF540N",
    "NE555",
    "ATMEGA328P",
    "74HC595",
    "74HC04",
    "MAX232",
    "LM317",
    "AMS1117",
]


# 重试装饰器
def retry_on_failure(max_retries: int = MAX_RETRIES, delay: int = RETRY_DELAY):
    """请求失败时自动重试的装饰器"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    logger.warning(f"第 {attempt}/{max_retries} 次尝试失败: {e}")
                    if attempt < max_retries:
                        time.sleep(delay)
            logger.error(f"重试 {max_retries} 次后仍然失败")
            raise last_exception
        return wrapper
    return decorator


def safe_find(element: BeautifulSoup, selectors: List[tuple]) -> Optional[Any]:
    """
    尝试多种选择器查找元素
    
    Args:
        element: BeautifulSoup 元素
        selectors: 选择器列表 [(tag, class_name), ...]
    
    Returns:
        找到的元素或 None
    """
    for tag, cls in selectors:
        result = element.find(tag, class_=re.compile(cls, re.I))
        if result:
            return result
    return element.find('a') or element.find()


def get_text_safe(element: Optional[Any], default: str = "") -> str:
    """安全获取元素文本"""
    if element:
        return element.get_text(strip=True)
    return default


@retry_on_failure(max_retries=3, delay=2)
def fetch_url(url: str, timeout: int = 30) -> Optional[str]:
    """
    获取 URL 内容（带重试机制）
    
    Args:
        url: 目标 URL
        timeout: 超时时间（秒）
    
    Returns:
        响应文本，失败返回 None
    """
    logger.info(f"Fetching: {url}")
    response = requests.get(url, headers=HEADERS, timeout=timeout)
    response.raise_for_status()
    return response.text


def search_lcsc(keyword: str) -> List[Dict[str, Any]]:
    """
    搜索 LCSC 获取器件信息
    
    Args:
        keyword: 搜索关键词
    
    Returns:
        器件信息列表
    """
    try:
        encoded_keyword = quote(keyword, safe='')
        url = f"{SEARCH_URL}?q={encoded_keyword}"
        
        logger.info(f"🔍 正在搜索: {keyword}...")
        print(f"🔍 正在搜索: {keyword}...")
        
        # 使用带重试的 fetch
        html_content = fetch_url(url, timeout=30)
        if not html_content:
            logger.error(f"获取搜索结果失败: {keyword}")
            return []
        
        # 解析搜索结果
        soup = BeautifulSoup(html_content, 'lxml')
        results = []
        
        # 查找产品列表 - LCSC 的结构可能变化
        product_cards = soup.find_all('div', class_='search-product-list') or \
                       soup.find_all('div', class_='product-list') or \
                       soup.find_all('div', class_='goods-list')
        
        if not product_cards:
            # 备选方案：查找所有可能的产品容器
            product_cards = soup.find_all('div', class_=re.compile(r'product|goods|item'))
        
        for card in product_cards[:10]:  # 最多取 10 个结果
            try:
                part_info = extract_product_info(card)
                if part_info:
                    results.append(part_info)
            except Exception as e:
                logger.debug(f"解析产品卡片失败: {e}")
                continue
        
        logger.info(f"✅ 找到 {len(results)} 个结果")
        print(f"✅ 找到 {len(results)} 个结果")
        return results
        
    except Exception as e:
        logger.error(f"❌ 搜索出错: {e}")
        print(f"❌ 搜索出错: {e}")
        return []


def extract_product_info(card) -> Optional[Dict[str, Any]]:
    """
    从产品卡片中提取信息
    
    Args:
        card: BeautifulSoup 产品卡片元素
    
    Returns:
        器件信息字典，失败返回 None
    """
    try:
        # 尝试多种选择器
        selectors = [
            ('a', 'product-name'),
            ('a', 'goods-name'),
            ('a', 'name'),
            ('a', 'product-title'),
        ]
        
        name_elem = safe_find(card, selectors)
        
        if not name_elem:
            # 查找任何链接
            name_elem = card.find('a')
        
        name = get_text_safe(name_elem)
        
        # 提取价格
        price_elem = card.find(class_=re.compile(r'price|current-price'))
        price = get_text_safe(price_elem)
        
        # 提取库存
        stock_elem = card.find(class_=re.compile(r'stock|inventory'))
        stock = get_text_safe(stock_elem)
        
        # 提取型号
        part_elem = card.find(class_=re.compile(r'model|part-number'))
        part = get_text_safe(part_elem)
        
        if not part and name:
            part = name.split()[0] if name.split() else name
        
        # 提取链接
        link = ""
        if name_elem and name_elem.get('href'):
            link = name_elem['href']
            if not link.startswith('http'):
                link = BASE_URL + link
        
        return {
            "part": part or "Unknown",
            "name": name or "",
            "price": price,
            "stock": stock,
            "link": link,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"提取产品信息失败: {e}")
        return None


@retry_on_failure(max_retries=2, delay=1)
def get_product_detail(url: str) -> Optional[Dict[str, Any]]:
    """
    获取产品详情页
    
    Args:
        url: 产品详情页 URL
    
    Returns:
        详情信息字典
    """
    try:
        html_content = fetch_url(url, timeout=30)
        if not html_content:
            return None
        
        soup = BeautifulSoup(html_content, 'lxml')
        
        # 提取详情
        data = {}
        
        # 制造商
        mfr_elem = soup.find(class_=re.compile(r'manufacturer|mfr'))
        if mfr_elem:
            data['manufacturer'] = get_text_safe(mfr_elem)
        
        # 描述
        desc_elem = soup.find(class_=re.compile(r'description|detail-desc'))
        if desc_elem:
            data['description'] = get_text_safe(desc_elem)[:200]
        
        # 封装
        pkg_elem = soup.find(class_=re.compile(r'package|footprint'))
        if pkg_elem:
            data['package'] = get_text_safe(pkg_elem)
        
        # 价格区间
        price_table = soup.find('table', class_=re.compile(r'price-table'))
        if price_table:
            prices = []
            for row in price_table.find_all('tr'):
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 2:
                    qty = get_text_safe(cells[0])
                    price = get_text_safe(cells[1])
                    prices.append({"qty": qty, "price": price})
            data['pricing'] = prices
        
        logger.info(f"✅ 获取详情成功: {url}")
        return data
        
    except Exception as e:
        logger.error(f"❌ 获取详情失败: {e}")
        print(f"❌ 获取详情失败: {e}")
        return None


def scrape_all_popular() -> Dict[str, Any]:
    """
    爬取所有热门器件
    
    Returns:
        包含所有器件数据的字典
    """
    print("=" * 60)
    print("🤖 LCSC 电子元器件数据爬虫")
    print("=" * 60)
    start_time = datetime.now()
    print(f"⏰ 开始时间: {start_time.isoformat()}")
    print(f"📦 将爬取 {len(POPULAR_PARTS)} 个热门器件")
    print("=" * 60)
    
    all_data = {
        "meta": {
            "updated": start_time.isoformat(),
            "source": "LCSC (立创商城)",
            "version": "1.1.0",
            "part_count": len(POPULAR_PARTS)
        },
        "parts": []
    }
    
    for i, part in enumerate(POPULAR_PARTS, 1):
        print(f"\n[{i}/{len(POPULAR_PARTS)}] ", end="")
        
        # 搜索获取基本信息
        results = search_lcsc(part)
        
        if results:
            # 取第一个结果作为主要信息
            main_result = results[0]
            
            # 如果有详情页链接，获取更多信息
            if main_result.get('link'):
                detail = get_product_detail(main_result['link'])
                if detail:
                    main_result.update(detail)
            
            all_data['parts'].append(main_result)
        else:
            # 搜索失败，添加占位数据
            all_data['parts'].append({
                "part": part,
                "name": part,
                "price": "查询中",
                "stock": "查询中",
                "link": f"{SEARCH_URL}?q={quote(part)}",
                "timestamp": start_time.isoformat(),
                "status": "not_found"
            })
        
        # 礼貌性延迟
        time.sleep(1)
    
    end_time = datetime.now()
    print("\n" + "=" * 60)
    print(f"✅ 爬取完成! 共获取 {len(all_data['parts'])} 个器件")
    print(f"⏰ 结束时间: {end_time.isoformat()}")
    print(f"⏱️ 耗时: {(end_time - start_time).total_seconds():.1f} 秒")
    print("=" * 60)
    
    return all_data


def save_to_json(data: Dict[str, Any], filename: str = "parts.json") -> None:
    """
    保存数据到 JSON 文件
    
    Args:
        data: 要保存的数据
        filename: 文件名
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"💾 数据已保存到: {filename}")


def main() -> None:
    """
    主函数
    """
    # 爬取数据
    data = scrape_all_popular()
    
    # 保存数据
    save_to_json(data, "../data/parts.json")
    
    # 同时保存一份带时间戳的版本
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_to_json(data, f"../data/parts_{timestamp}.json")
    
    print("\n📋 爬取摘要:")
    for part in data['parts']:
        status = "✅" if part.get('status') != 'not_found' else "⚠️"
        print(f"  {status} {part['part']}: {part['price']} | {part['stock']}")


if __name__ == "__main__":
    main()
