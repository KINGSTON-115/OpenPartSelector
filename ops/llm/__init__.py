"""
LLM 集成模块 - 支持多模型调用
"""
from typing import Dict, List, Optional, Any
from abc import ABC, abstractmethod
from dataclasses import dataclass
import logging

from .config import Config

logger = logging.getLogger(__name__)


@dataclass
class LLMResponse:
    """LLM 响应"""
    content: str
    model: str
    tokens_used: int = 0
    cost: float = 0.0
    latency_ms: float = 0.0


class BaseLLMProvider(ABC):
    """LLM 提供商基类"""
    
    def __init__(self, config: Config, api_key: str):
        self.config = config
        self.api_key = api_key
    
    @abstractmethod
    async def generate(
        self, 
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 2000,
        temperature: float = 0.1
    ) -> LLMResponse:
        """生成文本"""
        pass
    
    @abstractmethod
    async def generate_json(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.1
    ) -> Dict:
        """生成 JSON 响应"""
        pass


class OpenAIProvider(BaseLLMProvider):
    """OpenAI GPT Provider"""
    
    def __init__(self, config: Config):
        super().__init__(config, config.api_keys.openai)
        self.client = None
    
    async def _get_client(self):
        """获取异步客户端"""
        if self.client is None:
            try:
                from openai import AsyncOpenAI
                self.client = AsyncOpenAI(api_key=self.api_key)
            except ImportError:
                logger.error("OpenAI package not installed")
                raise
        return self.client
    
    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 2000,
        temperature: float = 0.1
    ) -> LLMResponse:
        """调用 GPT 生成"""
        import time
        
        client = await self._get_client()
        start_time = time.time()
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        try:
            response = await client.chat.completions.create(
                model=self.config.model_name or "gpt-4o",
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
            )
            
            latency = (time.time() - start_time) * 1000
            
            return LLMResponse(
                content=response.choices[0].message.content,
                model=response.model,
                tokens_used=response.usage.total_tokens,
                cost=self._calculate_cost(response.usage.total_tokens),
                latency_ms=latency
            )
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise
    
    async def generate_json(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.1
    ) -> Dict:
        """调用 GPT 生成 JSON"""
        import json
        
        # 添加 JSON 格式要求
        json_prompt = f"{prompt}\n\n请仅返回 JSON 格式，不要其他内容。"
        
        response = await self.generate(
            prompt=json_prompt,
            system_prompt=system_prompt,
            temperature=temperature
        )
        
        try:
            # 清理可能的 markdown 代码块
            content = response.content.strip()
            if content.startswith("```json"):
                content = content[7:]
            if content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
            
            return json.loads(content.strip())
        except json.JSONDecodeError as e:
            logger.error(f"JSON parse error: {e}")
            return {"error": "Failed to parse JSON", "raw": response.content}
    
    def _calculate_cost(self, tokens: int) -> float:
        """计算成本 (GPT-4o 定价)"""
        per_million = 5.0  # $5 / 1M tokens
        return tokens / 1_000_000 * per_million


class AnthropicProvider(BaseLLMProvider):
    """Anthropic Claude Provider"""
    
    def __init__(self, config: Config):
        super().__init__(config, config.api_keys.anthropic)
    
    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 2000,
        temperature: float = 0.1
    ) -> LLMResponse:
        """调用 Claude 生成"""
        import time
        from anthropic import Anthropic
        
        client = Anthropic(api_key=self.api_key)
        start_time = time.time()
        
        messages = []
        if system_prompt:
            messages.append({"role": "user", "content": f"{system_prompt}\n\n{prompt}"})
        else:
            messages.append({"role": "user", "content": prompt})
        
        try:
            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=max_tokens,
                temperature=temperature,
                messages=messages
            )
            
            latency = (time.time() - start_time) * 1000
            
            return LLMResponse(
                content=response.content[0].text,
                model=response.model,
                tokens_used=response.usage.input_tokens + response.usage.output_tokens,
                cost=self._calculate_cost(response.usage),
                latency_ms=latency
            )
        except Exception as e:
            logger.error(f"Anthropic API error: {e}")
            raise
    
    async def generate_json(self, prompt: str, system_prompt: Optional[str] = None, temperature: float = 0.1) -> Dict:
        """Claude JSON 生成"""
        import json
        json_prompt = f"{prompt}\n\n请仅返回有效的 JSON 格式。"
        response = await self.generate(prompt=json_prompt, system_prompt=system_prompt, temperature=temperature)
        try:
            return json.loads(response.content)
        except json.JSONDecodeError:
            return {"error": "JSON parse failed", "raw": response.content}
    
    def _calculate_cost(self, usage) -> float:
        """计算成本 (Claude 3.5 Sonnet)"""
        input_cost = 3.0  # $3 / 1M input
        output_cost = 15.0  # $15 / 1M output
        return usage.input_tokens / 1_000_000 * input_cost + usage.output_tokens / 1_000_000 * output_cost


class DeepSeekProvider(BaseLLMProvider):
    """DeepSeek Provider (性价比高)"""
    
    def __init__(self, config: Config):
        super().__init__(config, config.api_keys.deepseek)
    
    async def generate(self, prompt: str, system_prompt: Optional[str] = None, max_tokens: int = 2000, temperature: float = 0.1) -> LLMResponse:
        """调用 DeepSeek 生成"""
        import time, httpx
        
        client = httpx.AsyncClient(timeout=120.0)
        start_time = time.time()
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        try:
            response = await client.post(
                "https://api.deepseek.com/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "model": "deepseek-chat",
                    "messages": messages,
                    "max_tokens": max_tokens,
                    "temperature": temperature
                }
            )
            response.raise_for_status()
            data = response.json()
            
            latency = (time.time() - start_time) * 1000
            
            return LLMResponse(
                content=data["choices"][0]["message"]["content"],
                model="deepseek-chat",
                tokens_used=data["usage"]["total_tokens"],
                cost=self._calculate_cost(data["usage"]["total_tokens"]),
                latency_ms=latency
            )
        except Exception as e:
            logger.error(f"DeepSeek API error: {e}")
            raise
        finally:
            await client.aclose()
    
    async def generate_json(self, prompt: str, system_prompt: Optional[str] = None, temperature: float = 0.1) -> Dict:
        """DeepSeek JSON 生成"""
        import json
        response = await self.generate(prompt + "\n\n请仅返回 JSON。", system_prompt, temperature)
        try:
            return json.loads(response.content)
        except json.JSONDecodeError:
            return {"error": "JSON parse failed", "raw": response.content}
    
    def _calculate_cost(self, tokens: int) -> float:
        """DeepSeek 定价 ($0.14 / 1M tokens)"""
        return tokens / 1_000_000 * 0.14


class LLMManager:
    """LLM 管理器"""
    
    def __init__(self, config: Config):
        self.config = config
        self.providers: Dict[str, BaseLLMProvider] = {}
        self._init_providers()
    
    def _init_providers(self):
        """初始化 providers"""
        if self.config.api_keys.openai:
            self.providers["openai"] = OpenAIProvider(self.config)
        
        if self.config.api_keys.anthropic:
            self.providers["anthropic"] = AnthropicProvider(self.config)
        
        if self.config.api_keys.deepseek:
            self.providers["deepseek"] = DeepSeekProvider(self.config)
    
    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        model: Optional[str] = None,
        **kwargs
    ) -> LLMResponse:
        """生成文本 (自动选择模型)"""
        provider_name = model or self.config.default_llm
        
        if provider_name not in self.providers:
            # 尝试使用第一个可用的 provider
            if self.providers:
                provider_name = list(self.providers.keys())[0]
            else:
                raise ValueError("No LLM provider configured")
        
        provider = self.providers[provider_name]
        return await provider.generate(prompt, system_prompt, **kwargs)
    
    async def generate_json(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        model: Optional[str] = None,
        **kwargs
    ) -> Dict:
        """生成 JSON"""
        provider_name = model or self.config.default_llm
        
        if provider_name not in self.providers:
            if self.providers:
                provider_name = list(self.providers.keys())[0]
            else:
                raise ValueError("No LLM provider configured")
        
        provider = self.providers[provider_name]
        return await provider.generate_json(prompt, system_prompt, **kwargs)
    
    def get_available_models(self) -> List[str]:
        """获取可用模型列表"""
        return list(self.providers.keys())
