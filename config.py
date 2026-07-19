"""
🤖 ADVANCED TELEGRAM AI BOT - Configuration
OpenRouter API + Nemotron Ultra Model
"""

import os
from pathlib import Path
from typing import Optional, List

# ============================================================
# TELEGRAM CONFIGURATION
# ============================================================

BOT_TOKEN: str = os.environ.get("BOT_TOKEN", "")

# ============================================================
# OPENROUTER AI CONFIGURATION  
# ============================================================

OPENROUTER_API_KEY: str = os.environ.get("OPENROUTER_API_KEY", "")
OPENROUTER_MODEL: str = os.environ.get("AI_MODEL", "nvidia/nemotron-3-ultra-550b-a55b:free")
OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"

# Alternative free models (fallback)
FALLBACK_MODELS: List[str] = [
    "meta-llama/llama-3.3-70b-instruct:free",
    "mistralai/mistral-7b-instruct:free",
    "google/gemma-2-9b-it:free",
]

# ============================================================
# AI BEHAVIOR CONFIGURATION
# ============================================================

SYSTEM_PROMPT: str = """You are Nova, an advanced AI assistant created to help users with anything they need.

Your personality traits:
- Friendly, helpful, and engaging
- Respond concisely but thoroughly
- Use emojis occasionally to make conversations lively
- You can help with: coding, writing, analysis, math, creative tasks, explanations
- Be honest when you don't know something

Response guidelines:
- Format code blocks properly with language tags
- Use markdown for formatting (bold, lists, etc.)
- Keep responses under 2000 characters when possible
- If asked in Hindi/Hinglish, respond similarly
- Be respectful and avoid harmful content"""

MAX_TOKENS: int = int(os.environ.get("MAX_TOKENS", "2048"))
TEMPERATURE: float = float(os.environ.get("TEMPERATURE", "0.7"))
TOP_P: float = float(os.environ.get("TOP_P", "0.9"))

# ============================================================
# CONVERSATION MEMORY
# ============================================================

MAX_HISTORY_PER_USER: int = int(os.environ.get("MAX_HISTORY", "20"))  # Messages to remember
MEMORY_TTL_HOURS: int = 24  # Hours before clearing memory

# ============================================================
# RATE LIMITING & PERFORMANCE
# ============================================================

TYPING_DELAY: float = 3.0  # Seconds between typing updates
MAX_RESPONSE_TIME: int = 60  # Max seconds to wait for AI response
REQUEST_TIMEOUT: int = 90  # HTTP request timeout

# Rate limiting (requests per minute per user)
RATE_LIMIT_MINUTE: int = 10
RATE_LIMIT_HOUR: int = 50

# ============================================================
# BOT FEATURES
# ============================================================

ENABLE_VOICE: bool = True  # Voice message support
ENABLE_IMAGE: bool = False  # Image generation (needs DALL-E key)
ENABLE_CODE_EXECUTION: bool = False  # Sandbox code execution
STREAM_RESPONSES: bool = True  # Stream responses for live preview

# Admin users (can use admin commands)
ADMIN_IDS: List[int] = [
    int(x) for x in os.environ.get("ADMIN_IDS", "").split(",") if x.isdigit()
]

OWNER_ID: Optional[int] = int(os.environ.get("OWNER_ID", "0")) or None

# ============================================================
# RAILWAY / DEPLOYMENT CONFIGURATION
# ============================================================

PORT: int = int(os.environ.get("PORT", "8080"))
DEBUG_MODE: bool = os.environ.get("DEBUG", "false").lower() == "true"
LOG_LEVEL: str = os.environ.get("LOG_LEVEL", "INFO")

# File paths
DATA_DIR: Path = Path("./data")
SESSION_FILE: Path = DATA_DIR / "bot_session.json"

# ============================================================
# VALIDATION
# ============================================================

def validate_config() -> tuple[bool, list[str]]:
    """Validate all required configuration."""
    errors = []
    warnings = []
    
    if not BOT_TOKEN:
        errors.append("❌ BOT_TOKEN is required")
    
    if not OPENROUTER_API_KEY:
        errors.append("❌ OPENROUTER_API_KEY is required")
    
    if OWNER_ID and OWNER_ID == 0:
        warnings.append("⚠️ OWNER_ID not set (admin commands disabled)")
    
    return len(errors) == 0, errors + warnings


def get_env_info() -> dict:
    """Get environment info for display."""
    return {
        "model": OPENROUTER_MODEL.split("/")[-1] if "/" in OPENROUTER_MODEL else OPENROUTER_MODEL,
        "max_tokens": MAX_TOKENS,
        "temperature": TEMPERATURE,
        "memory": f"{MAX_HISTORY_PER_USER} msgs/user",
        "features": {
            "typing": "✅ Live Typing",
            "stream": "✅ Streaming" if STREAM_RESPONSES else "❌",
            "voice": "✅" if ENABLE_VOICE else "❌",
            "memory": "✅ Context Memory",
        }
    }


# Create data directory on import
DATA_DIR.mkdir(parents=True, exist_ok=True)

print("\n" + "="*60)
print("🤖 NOVA AI BOT - Configuration Loaded")
print("="*60)
print(f"   Model: {OPENROUTER_MODEL}")
print(f"   Max Tokens: {MAX_TOKENS}")
print(f"   Temperature: {TEMPERATURE}")
print(f"   Memory: {MAX_HISTORY_PER_USER} messages/user")
print("="*60 + "\n")
