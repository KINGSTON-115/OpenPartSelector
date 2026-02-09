"""
配置管理模块
"""
import os
from pathlib import Path
from typing import Optional
from dataclasses import dataclass, field
import yaml


@dataclass
class APIKeys:
    """API Keys 配置"""
    openai: str = ""
    anthropic: str = ""
    google: str = ""
    deepseek: str = ""
    
    # 电商平台 API
    digikey: str = ""
    mouser: str = ""
    octopart: str = ""


@dataclass
class Config:
    """主配置类"""
    # 基础配置
    project_name: str = "OpenPartSelector"
    version: str = "0.1.0"
    debug: bool = False
    
    # API Keys
    api_keys: APIKeys = field(default_factory=APIKeys)
    
    # LLM 配置
    default_llm: str = "openai"
    model_name: str = "gpt-4o"
    temperature: float = 0.1
    
    # 搜索配置
    max_results: int = 10
    timeout_seconds: int = 30
    
    # 知识库配置
    vector_store_path: str = "./data/vector_store"
    embedding_model: str = "text-embedding-3-small"
    
    # 缓存配置
    cache_enabled: bool = True
    cache_ttl_hours: int = 24
    
    @classmethod
    def load(cls, config_path: Optional[str] = None) -> "Config":
        """从 YAML 文件加载配置"""
        if config_path is None:
            config_path = os.environ.get(
                "OPS_CONFIG_PATH", 
                str(Path(__file__).parent.parent / "config.yaml")
            )
        
        if not os.path.exists(config_path):
            return cls()
        
        with open(config_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        if data is None:
            return cls()
        
        config = cls()
        
        if 'api_keys' in data:
            for key, value in data['api_keys'].items():
                if hasattr(config.api_keys, key):
                    setattr(config.api_keys, key, value)
        
        # 覆盖环境变量
        for attr in ['openai', 'anthropic', 'google', 'deepseek']:
            env_key = f"OPS_{attr.upper()}_API_KEY"
            env_value = os.environ.get(env_key, "")
            if env_value:
                setattr(config.api_keys, attr, env_value)
        
        return config
    
    def save(self, config_path: str):
        """保存配置到 YAML 文件"""
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump({
                'api_keys': {
                    'openai': self.api_keys.openai,
                    'anthropic': self.api_keys.anthropic,
                    'google': self.api_keys.google,
                    'deepseek': self.api_keys.deepseek,
                }
            }, f, allow_unicode=True)
