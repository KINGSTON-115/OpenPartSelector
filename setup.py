"""
📦 Python 包配置 - 支持 pip 安装
"""
from setuptools import setup, find_packages

setup(
    name="OpenPartSelector",
    version="1.1.28",
    description="AI-Driven Electronic Component Selection Engine",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="KINGSTON-115",
    author_email="zhenweisi@openclaw.ai",
    url="https://github.com/KINGSTON-115/OpenPartSelector",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)",
    ],
    keywords=[
        "electronics", "component selection", "EDA", "BOM", 
        "circuit design", "open source", "AI", "CAD"
    ],
    packages=find_packages(exclude=["tests*", "docs*", "examples*"]),
    python_requires=">=3.10",
    install_requires=[
        "openai>=1.0.0",
        "anthropic>=0.3.0",
        "aiohttp>=3.9.0",
        "httpx>=0.25.0",
        "pyyaml>=6.0",
        "pydantic>=2.0.0",
        "loguru>=0.7.0",
    ],
    extras_require={
        "gui": [
            "streamlit>=1.28.0",
        ],
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "ops=tools.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "ops": [
            "prompts/*",
            "data/*",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/KINGSTON-115/OpenPartSelector/issues",
        "Source": "https://github.com/KINGSTON-115/OpenPartSelector",
        "Documentation": "https://github.com/KINGSTON-115/OpenPartSelector/tree/main/docs",
    },
)
