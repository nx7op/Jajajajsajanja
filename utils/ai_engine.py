"""
🧠 ADVANCED AI ENGINE - OpenRouter Integration
Nemotron Ultra Model + Streaming + Fallback
"""

import os
import json
import asyncio
import aiohttp
import time
from typing import Optional, AsyncGenerator, Dict, List, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta

from config import (
    OPENROUTER_API_KEY,
    OPENROUTER_MODEL,
    OPENROUTER_BASE_URL,
    SYSTEM_PROMPT,
    MAX_TOKENS,
    TEMPERATURE,
    TOP_P,
    FALLBACK_MODELS,
    REQUEST_TIMEOUT,
)


@dataclass
class Message:
    """Chat message structure."""
    role: str  # "user", "assistant", "system"
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> dict:
        return {"role": self.role, "content": self.content}


@dataclass 
class AIResponse:
    """AI Response with metadata."""
    content: str
    model_used: str
    tokens_used: int = 0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    latency_ms: int = 0
    is_fallback: bool = False
    error: Optional[str] = None


class ConversationMemory:
    """Per-user conversation memory with TTL."""
    
    def __init__(self, max_messages: int = 20, ttl_hours: int = 24):
        self.max_messages = max_messages
        self.ttl = timedelta(hours=ttl_hours)
        self.conversations: Dict[int, List[Message]] = {}
        self._last_access: Dict[int, datetime] = {}
    
    def add_message(self, user_id: int, role: str, content: str):
        """Add message to conversation history."""
        if user_id not in self.conversations:
            self.conversations[user_id] = []
        
        # Check TTL - clear if expired
        self._check_ttl(user_id)
        
        # Add new message
        msg = Message(role=role, content=content)
        self.conversations[user_id].append(msg)
        
        # Trim to max size
        if len(self.conversations[user_id]) > self.max_messages:
            self.conversations[user_id] = self.conversations[user_id][-self.max_messages:]
        
        self._last_access[user_id] = datetime.now()
    
    def get_history(self, user_id: int) -> List[dict]:
        """Get conversation history for API."""
        self._check_ttl(user_id)
        
        if user_id not in self.conversations:
            return []
        
        return [msg.to_dict() for msg in self.conversations[user_id]]
    
    def clear(self, user_id: int):
        """Clear conversation for user."""
        if user_id in self.conversations:
            del self.conversations[user_id]
        if user_id in self._last_access:
            del self._last_access[user_id]
    
    def _check_ttl(self, user_id: int):
        """Check and clear expired conversations."""
        if user_id in self._last_access:
            if datetime.now() - self._last_access[user_id] > self.ttl:
                self.clear(user_id)
    
    def get_stats(self) -> dict:
        """Get memory statistics."""
        total_msgs = sum(len(msgs) for msgs in self.conversations.values())
        return {
            "active_users": len(self.conversations),
            "total_messages": total_msgs,
            "avg_per_user": total_msgs // len(self.conversations) if self.conversations else 0
        }


class AIEngine:
    """
    Advanced AI Engine with OpenRouter API.
    
    Features:
    - Multiple model fallback
    - Streaming responses
    - Rate limiting aware
    - Error recovery
    """
    
    def __init__(self):
        self.api_key = OPENROUTER_API_KEY
        self.base_url = OPENROUTER_BASE_URL
        self.primary_model = OPENROUTER_MODEL
        self.fallback_models = FALLBACK_MODELS
        
        self.memory = ConversationMemory()
        
        # Stats tracking
        self._request_count = 0
        self._success_count = 0
        self._fallback_count = 0
        self._total_latency = 0
    
    async def chat(
        self,
        user_id: int,
        message: str,
        stream_callback=None,
        system_prompt: str = None
    ) -> AIResponse:
        """
        Process chat message and get AI response.
        
        Args:
            user_id: Telegram user ID
            message: User's message text
            stream_callback: Optional callback for streaming chunks
            system_prompt: Override default system prompt
        """
        start_time = time.time()
        
        # Store user message
        self.memory.add_message(user_id, "user", message)
        
        # Build messages array
        messages = []
        
        # System prompt
        messages.append({
            "role": "system",
            "content": system_prompt or SYSTEM_PROMPT
        })
        
        # Conversation history
        history = self.memory.get_history(user_id)
        messages.extend(history)
        
        # Try primary model first
        response = await self._call_api(
            messages=messages,
            model=self.primary_model,
            stream_callback=stream_callback
        )
        
        # Try fallbacks if needed
        if response.error and self.fallback_models:
            for fallback_model in self.fallback_models:
                print(f"   🔄 Trying fallback: {fallback_model}")
                response = await self._call_api(
                    messages=messages,
                    model=fallback_model,
                    stream_callback=stream_callback
                )
                
                if not response.error:
                    response.is_fallback = True
                    break
        
        # Calculate stats
        latency = int((time.time() - start_time) * 1000)
        response.latency_ms = latency
        
        # Store assistant response if successful
        if not response.error and response.content:
            self.memory.add_message(user_id, "assistant", response.content)
        
        # Update global stats
        self._request_count += 1
        self._total_latency += latency
        if not response.error:
            self._success_count += 1
        if response.is_fallback:
            self._fallback_count += 1
        
        return response
    
    async def _call_api(
        self,
        messages: List[dict],
        model: str,
        stream_callback=None
    ) -> AIResponse:
        """Make API call to OpenRouter."""
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://t.me/nova_ai_bot",
            "X-Title": "Nova AI Bot"
        }
        
        payload = {
            "model": model,
            "messages": messages,
            "max_tokens": MAX_TOKENS,
            "temperature": TEMPERATURE,
            "top_p": TOP_P,
            "stream": stream_callback is not None
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=REQUEST_TIMEOUT)
                ) as resp:
                    
                    if resp.status != 200:
                        error_text = await resp.text()
                        print(f"   ❌ API Error ({resp.status}): {error_text[:200]}")
                        return AIResponse(
                            content="",
                            model_used=model,
                            error=f"API Error {resp.status}: {error_text[:100]}"
                        )
                    
                    if stream_callback:
                        return await self._handle_stream(resp, model, stream_callback)
                    else:
                        return await self._handle_normal(resp, model)
                        
        except asyncio.TimeoutError:
            return AIResponse(content="", model_used=model, error="Request timeout")
        except Exception as e:
            return AIResponse(content="", model_used=model, error=str(e))
    
    async def _handle_stream(self, response, model: str, callback) -> AIResponse:
        """Handle streaming response."""
        full_content = ""
        prompt_tokens = 0
        completion_tokens = 0
        
        try:
            async for line in response.content:
                line = line.decode('utf-8').strip()
                
                if not line.startswith("data: "):
                    continue
                
                data = line[6:]  # Remove "data: "
                
                if data == "[DONE]":
                    break
                
                try:
                    chunk = json.loads(data)
                    
                    # Extract content delta
                    delta = chunk.get("choices", [{}])[0].get("delta", {})
                    content = delta.get("content", "")
                    
                    if content:
                        full_content += content
                        
                        # Call streaming callback
                        try:
                            callback(content)
                        except Exception:
                            pass
                    
                    # Token usage (in last chunk usually)
                    usage = chunk.get("usage", {})
                    if usage:
                        prompt_tokens = usage.get("prompt_tokens", 0)
                        completion_tokens = usage.get("completion_tokens", 0)
                        
                except json.JSONDecodeError:
                    continue
            
            return AIResponse(
                content=full_content.strip(),
                model_used=model,
                tokens_used=prompt_tokens + completion_tokens,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens
            )
            
        except Exception as e:
            # Return what we have so far
            if full_content:
                return AIResponse(
                    content=full_content.strip(),
                    model_used=model,
                    error=f"Stream interrupted: {str(e)[:50]}"
                )
            return AIResponse(content="", model_used=model, error=str(e))
    
    async def _handle_normal(self, response, model: str) -> AIResponse:
        """Handle normal (non-streaming) response."""
        try:
            data = await response.json()
            
            choice = data.get("choices", [{}])[0]
            content = choice.get("message", {}).get("content", "")
            
            usage = data.get("usage", {})
            
            return AIResponse(
                content=content.strip(),
                model_used=model,
                tokens_used=usage.get("total_tokens", 0),
                prompt_tokens=usage.get("prompt_tokens", 0),
                completion_tokens=usage.get("completion_tokens", 0)
            )
            
        except Exception as e:
            return AIResponse(content="", model_used=model, error=f"Parse error: {e}")
    
    def clear_memory(self, user_id: int):
        """Clear conversation memory for user."""
        self.memory.clear(user_id)
    
    def get_stats(self) -> dict:
        """Get engine statistics."""
        avg_latency = self._total_latency / self._request_count if self._request_count else 0
        return {
            "total_requests": self._request_count,
            "success_rate": f"{(self._success_count / self._request_count * 100):.1f}%" if self._request_count else "N/A",
            "avg_latency_ms": int(avg_latency),
            "fallbacks_used": self._fallback_count,
            **self.memory.get_stats()
        }


# Global engine instance
_engine: Optional[AIEngine] = None


def get_ai_engine() -> AIEngine:
    """Get or create global AI engine instance."""
    global _engine
    if _engine is None:
        _engine = AIEngine()
    return _engine
