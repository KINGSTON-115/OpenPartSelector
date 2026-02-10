# 🤝 贡献指南

感谢您有兴趣为 OpenPartSelector 贡献代码！

## 📋 目录

- [如何贡献](#如何贡献)
- [开发环境设置](#开发环境设置)
- [代码规范](#代码规范)
- [提交 Pull Request](#提交-pull-request)
- [报告 Bug](#报告-bug)

## 🛠️ 如何贡献

1. **Fork 本仓库**
2. **创建特性分支**: `git checkout -b feature/AmazingFeature`
3. **提交更改**: `git commit -m 'Add some AmazingFeature'`
4. **推送分支**: `git push origin feature/AmazingFeature`
5. **提交 Pull Request**

## 💻 开发环境设置

```bash
# 克隆仓库
git clone https://github.com/YOUR_USERNAME/OpenPartSelector.git
cd OpenPartSelector

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 安装依赖
pip install -e .

# 安装开发依赖
pip install pytest black isort mypy

# 运行测试
pytest tests/
```

## 📏 代码规范

### Python

- 使用 **Black** 格式化: `black .`
- 使用 **isort** 排序导入: `isort .`
- 类型注解: 所有公开函数需添加类型注解
- 文档字符串: 使用 Google 风格 docstring

```python
def example_function(arg1: str, arg2: int) -> bool:
    """简短的函数说明。

    详细的函数说明，可以多行。

    Args:
        arg1: 参数1的说明
        arg2: 参数2的说明

    Returns:
        返回值的说明

    Raises:
        ValueError: 异常条件说明
    """
    pass
```

### 前端代码

- HTML/CSS/JS 保持简洁
- 使用语义化标签
- CSS 使用 BEM 命名规范

## 🧪 测试规范

### 单元测试

```python
def test_feature():
    """测试功能描述"""
    # Arrange
    input_data = ...
    expected = ...
    
    # Act
    result = function(input_data)
    
    # Assert
    assert result == expected
```

### 集成测试

- 测试完整的用户流程
- 模拟外部 API 调用

## 📝 提交规范

使用 [Conventional Commits](https://www.conventionalcommits.org/):

- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式（不影响功能）
- `refactor`: 重构
- `test`: 测试相关
- `chore`: 构建/工具相关

示例:
```
feat(search): 添加模糊搜索支持

fix(database): 修复连接池泄漏

docs(readme): 更新安装说明
```

## 🐛 报告 Bug

请使用 [GitHub Issues](https://github.com/KINGSTON-115/OpenPartSelector/issues) 报告 Bug，包含：

1. **问题描述**: 清晰描述问题
2. **复现步骤**: 详细的复现步骤
3. **预期行为**: 应该发生什么
4. **实际行为**: 实际发生什么
5. **环境信息**: Python 版本、操作系统等

## 💡 提出新功能

欢迎提出新功能！请先查看 [Roadmap](ROADMAP.md) 确保功能未被规划。

## 📜 许可证

贡献的代码将使用 MIT 许可证。

---

**感谢您的贡献！** 🎉
