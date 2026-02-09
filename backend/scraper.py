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
from datetime import datetime
from urllib.parse import quote

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


def search_lcsc(keyword):
    """
    搜索 LCSC 获取器件信息
    """
    try:
        encoded_keyword = quote(keyword, safe='')
        url = f"{SEARCH_URL}?q={encoded_keyword}"
        
        print(f"🔍 正在搜索: {keyword}...")
        
        response = requests.get(url, headers=HEADERS, timeout=30)
        
        if response.status_code != 200:
            print(f"❌ 请求失败: {response.status_code}")
            return []
        
        # 解析搜索结果
        soup = BeautifulSoup(response.text, 'lxml')
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
                continue
        
        print(f"✅ 找到 {len(results)} 个结果")
        return results
        
    except Exception as e:
        print(f"❌ 搜索出错: {e}")
        return []


def extract_product_info(card):
    """
    从产品卡片中提取信息
    """
    try:
        # 尝试多种选择器
        selectors = [
            ('a', 'product-name'),
            ('a', 'goods-name'),
            ('a', 'name'),
            ('a', 'product-title'),
        ]
        
        name_elem = None
        for tag, cls in selectors:
            elem = card.find(tag, class_=re.compile(cls))
            if elem:
                name_elem = elem
                break
        
        if not name_elem:
            # 查找任何链接
            name_elem = card.find('a')
        
        name = name_elem.get_text(strip=True) if name_elem else ""
        
        # 提取价格
        price_elem = card.find(class_=re.compile(r'price|current-price'))
        price = ""
        if price_elem:
            price = price_elem.get_text(strip=True)
        
        # 提取库存
        stock_elem = card.find(class_=re.compile(r'stock|inventory'))
        stock = ""
        if stock_elem:
            stock = stock_elem.get_text(strip=True)
        
        # 提取型号
        part_elem = card.find(class_=re.compile(r'model|part-number'))
        part = ""
        if part_elem:
            part = part_elem.get_text(strip=True)
        
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
        return None


def get_product_detail(url):
    """
    获取产品详情页
    """
    try:
        response = requests.get(url, headers=HEADERS, timeout=30)
        
        if response.status_code != 200:
            return None
        
        soup = BeautifulSoup(response.text, 'lxml')
        
        # 提取详情
        data = {}
        
        # 制造商
        mfr_elem = soup.find(class_=re.compile(r'manufacturer|mfr'))
        if mfr_elem:
            data['manufacturer'] = mfr_elem.get_text(strip=True)
        
        # 描述
        desc_elem = soup.find(class_=re.compile(r'description|detail-desc'))
        if desc_elem:
            data['description'] = desc_elem.get_text(strip=True)[:200]
        
        # 封装
        pkg_elem = soup.find(class_=re.compile(r'package|footprint'))
        if pkg_elem:
            data['package'] = pkg_elem.get_text(strip=True)
        
        # 价格区间
        price_table = soup.find('table', class_=re.compile(r'price-table'))
        if price_table:
            prices = []
            for row in price_table.find_all('tr'):
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 2:
                    qty = cells[0].get_text(strip=True)
                    price = cells[1].get_text(strip=True)
                    prices.append({"qty": qty, "price": price})
            data['pricing'] = prices
        
        return data
        
    except Exception as e:
        print(f"❌ 获取详情失败: {e}")
        return None


def scrape_all_popular():
    """
    爬取所有热门器件
    """
    print("=" * 60)
    print("🤖 LCSC 电子元器件数据爬虫")
    print("=" * 60)
    print(f"⏰ 开始时间: {datetime.now().isoformat()}")
    print(f"📦 将爬取 {len(POPULAR_PARTS)} 个热门器件")
    print("=" * 60)
    
    all_data = {
        "meta": {
            "updated": datetime.now().isoformat(),
            "source": "LCSC (立创商城)",
            "version": "1.0.0",
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
                "timestamp": datetime.now().isoformat(),
                "status": "not_found"
            })
        
        # 礼貌性延迟
        time.sleep(1)
    
    print("\n" + "=" * 60)
    print(f"✅ 爬取完成! 共获取 {len(all_data['parts'])} 个器件")
    print(f"⏰ 结束时间: {datetime.now().isoformat()}")
    print("=" * 60)
    
    return all_data


def save_to_json(data, filename="parts.json"):
    """
    保存数据到 JSON 文件
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"💾 数据已保存到: {filename}")


def main():
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
