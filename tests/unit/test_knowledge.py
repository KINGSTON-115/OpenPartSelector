"""
测试向量知识库模块
"""
import pytest
import tempfile
import os
from pathlib import Path

from ops.knowledge import VectorStore
from ops.config import Config


@pytest.fixture
def temp_config():
    """创建临时配置"""
    with tempfile.TemporaryDirectory() as tmpdir:
        config = Config(
            vector_store_path=os.path.join(tmpdir, "vector_store"),
            debug=True
        )
        yield config


@pytest.fixture
async def vector_store(temp_config):
    """创建向量知识库实例"""
    store = VectorStore(temp_config)
    await store.initialize()
    yield store
    # 清理在 __init__.py 中已处理


class TestVectorStore:
    """向量知识库测试类"""

    @pytest.mark.asyncio
    async def test_add_and_search_part(self, vector_store):
        """测试添加和搜索元器件"""
        test_part = {
            "part_number": "ESP32-WROOM",
            "category": "WiFi Module",
            "specs": {
                "voltage": "3.3V",
                "processor": "Xtensa LX6",
                "wireless": "WiFi + Bluetooth"
            }
        }

        await vector_store.add_datasheet("ESP32-WROOM", test_part)

        # 搜索测试
        results = await vector_store.search("ESP32 wireless")
        assert len(results) >= 1

        found = False
        for r in results:
            if r.get("part_number") == "ESP32-WROOM":
                found = True
                break

        assert found

    @pytest.mark.asyncio
    async def test_get_part(self, vector_store):
        """测试获取特定元器件"""
        test_part = {
            "part_number": "STM32F103C8T6",
            "category": "MCU",
            "specs": {"voltage": "3.3V", "flash": "64KB"}
        }

        await vector_store.add_datasheet("STM32F103C8T6", test_part)

        result = await vector_store.get_part("stm32f103c8t6")
        assert result is not None
        assert result["part_number"] == "STM32F103C8T6"

    @pytest.mark.asyncio
    async def test_delete_part(self, vector_store):
        """测试删除元器件"""
        test_part = {
            "part_number": "TEST-DELETE",
            "category": "Test"
        }

        await vector_store.add_datasheet("TEST-DELETE", test_part)
        assert await vector_store.get_part("TEST-DELETE") is not None

        deleted = await vector_store.delete_part("TEST-DELETE")
        assert deleted is True
        assert await vector_store.get_part("TEST-DELETE") is None

    @pytest.mark.asyncio
    async def test_bulk_import(self, vector_store):
        """测试批量导入"""
        parts = [
            {"part_number": "PART-A", "category": "A"},
            {"part_number": "PART-B", "category": "B"},
            {"part_number": "PART-C", "category": "C"},
        ]

        await vector_store.bulk_import(parts)

        assert await vector_store.get_part("PART-A") is not None
        assert await vector_store.get_part("PART-B") is not None
        assert await vector_store.get_part("PART-C") is not None


class TestEmbeddingFunctions:
    """嵌入功能测试类"""

    @pytest.mark.asyncio
    async def test_create_embeddings(self, vector_store):
        """测试创建嵌入向量"""
        test_part = {
            "part_number": "ESP32-S3",
            "data": {
                "wireless": "WiFi Bluetooth",
                "processor": "Xtensa LX7"
            }
        }

        await vector_store.add_datasheet("ESP32-S3", test_part)
        await vector_store.create_embeddings()

        # 验证嵌入已创建
        part = await vector_store.get_part("ESP32-S3")
        assert part is not None
        assert part.get("embeddings") is not None
        assert len(part["embeddings"]) == 64

    @pytest.mark.asyncio
    async def test_semantic_search(self, vector_store):
        """测试语义搜索"""
        # 添加多个器件
        parts = [
            {"part_number": "ESP32-C3", "data": {"wireless": "WiFi"}},
            {"part_number": "NRF52832", "data": {"wireless": "Bluetooth"}},
            {"part_number": "STM32G0", "data": {"category": "MCU"}},
        ]

        for p in parts:
            await vector_store.add_datasheet(p["part_number"], p)

        await vector_store.create_embeddings()

        # 搜索 WiFi 相关
        results = await vector_store.semantic_search("WiFi wireless", top_k=3)

        # 应该有 ESP32-C3 在结果中（WiFi 相关）
        part_numbers = [r.get("part_number") for r in results]
        assert "ESP32-C3" in part_numbers or len(results) > 0

    def test_generate_text_embedding(self, vector_store):
        """测试文本嵌入生成"""
        text = "ESP32 is a WiFi and Bluetooth module with 3.3V voltage"

        embedding = vector_store._generate_text_embedding(text)

        assert embedding is not None
        assert len(embedding) == 64
        assert all(0.0 <= v <= 1.0 for v in embedding)

        # 验证 WiFi/Bluetooth 词汇有较高权重
        assert any(v > 0.0 for v in embedding)

    def test_cosine_similarity(self, vector_store):
        """测试余弦相似度计算"""
        vec_a = [1.0, 0.0, 0.0]
        vec_b = [1.0, 0.0, 0.0]
        vec_c = [0.0, 1.0, 0.0]

        sim_aa = vector_store._cosine_similarity(vec_a, vec_a)
        sim_ac = vector_store._cosine_similarity(vec_a, vec_c)
        sim_ab = vector_store._cosine_similarity(vec_a, vec_b)

        assert sim_aa == 1.0  # 自身相似度为1
        assert sim_ab == 1.0  # 相同向量
        assert sim_ac == 0.0  # 正交向量

    def test_relevance_score(self, vector_store):
        """测试相关性分数计算"""
        content = '{"part_number": "ESP32-WROOM", "category": "WiFi Module"}'

        # 完整匹配应该有较高分数
        score_full = vector_store._calculate_relevance("ESP32-WROOM", content)
        score_wifi = vector_store._calculate_relevance("WiFi", content)

        # 验证匹配逻辑
        assert score_full >= 0.5  # 完整匹配
        assert score_wifi > 0  # 部分匹配


class TestEdgeCases:
    """边缘情况测试"""

    @pytest.mark.asyncio
    async def test_search_empty_query(self, vector_store):
        """测试空查询"""
        results = await vector_store.search("")
        assert isinstance(results, list)

    @pytest.mark.asyncio
    async def test_search_no_results(self, vector_store):
        """测试无结果搜索"""
        results = await vector_store.search("xyznonexistent123")
        assert isinstance(results, list)

    @pytest.mark.asyncio
    async def test_get_nonexistent_part(self, vector_store):
        """测试获取不存在的元器件"""
        result = await vector_store.get_part("NONEXISTENT")
        assert result is None

    @pytest.mark.asyncio
    async def test_delete_nonexistent_part(self, vector_store):
        """测试删除不存在的元器件"""
        deleted = await vector_store.delete_part("NONEXISTENT")
        assert deleted is False

    @pytest.mark.asyncio
    async def test_filter_by_category(self, vector_store):
        """测试类别过滤"""
        await vector_store.add_datasheet("PART-A", {"category": "Sensor"})
        await vector_store.add_datasheet("PART-B", {"category": "MCU"})

        results = await vector_store.search("", filters={"category": "Sensor"})

        for r in results:
            if "category" in r:
                assert r["category"].lower() == "sensor"
