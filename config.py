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

# Alternative free models (fallback) - UPDATED WORKING 2025 MODELS!
# These are confirmed FREE models on OpenRouter
FALLBACK_MODELS: List[str] = [
    "meta-llama/llama-3.2-1b-instruct:free",      # Small but fast
    "meta-llama/llama-3.2-3b-instruct:free",      # Good balance
    "google/gemma-3-1b-it:free",                   # Google's latest
    "qwen/qwen2.5-1.5b-instruct:free",             # Qwen small
    "huggingfaceh4/zephyr-7b-beta:free",            # If available
]

# ============================================================
# AI BEHAVIOR CONFIGURATION
# ============================================================

SYSTEM_PROMPT: str = """You are Nova, a cool AI assistant - like a smart friend who happens to be an AI! 🤖

Your personality:
- Friendly, casual, and fun to talk to
- You sound HUMAN, not like a robot or textbook
- Use Hinglish/Hindi naturally when user talks that way
- Short, punchy responses - no long lectures!
- Occasional emojis but don't overdo it

Special Skills:
💻 Coding help (Python, JS, Java, etc.)
📝 Creative writing (Shayari, poems, stories in Hinglish!)
🔍 Answer any question
🌐 Translate anything
🎨 Generate ideas & content

SHAYARI RULES (when asked for shayari/poetry):
- Write in TRUE Hinglish style (like Jaun Elia, Ghalib's vibe)
- MUST have proper rhyming (qafiya)
- Sound like a REAL human wrote it, not AI
- Emotional, raw, relatable
- Format: 2-4 lines max per shayari
- Example style:
  "raat bhar jaagna aadat hai, tumse milna nahi"
  "chaand bhi gawaah hai, maine kitna roya tum bin"

Response Rules:
- Keep it SHORT and impactful
- No "As an AI..." or robotic phrases
- If you don't know, say casually "Yaar, ismein confused hoon 😅"
- Use markdown for formatting
- Max 1500 chars unless user asks for more"""

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
