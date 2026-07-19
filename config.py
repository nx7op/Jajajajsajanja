"""
🤖 NOVA AI BOT v2.3 - Configuration
====================================

✅ MODEL:
   - openrouter/auto-beta (MULTIMODAL!)
   - Text + Image Generation in ONE model!

✅ FEATURES:
   - Font Changer, Shayari, Quotes
   - 🆕 IMAGE GENERATION (/image, /generate)
   - 🎨 AI Art Creator
   - Code Agent Mode (/agent)
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
OPENROUTER_MODEL: str = "openrouter/auto-beta"  # MULTIMODAL MODEL!
OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"

# ============================================================
# 🧠 THE ONLY MODEL - MULTIMODAL AUTO-BETA!
# ============================================================

# PRIMARY MODEL - Does EVERYTHING!
PRIMARY_MODEL: str = "openrouter/auto-beta"

# Model info for display
MODEL_INFO: dict = {
    "id": "openrouter/auto-beta",
    "name": "🚀 Auto Beta (Multimodal)",
    "provider": "OpenRouter",
    "desc": "🎨 TEXT + IMAGE GENERATION - All in one!",
    "capabilities": ["text", "image", "code", "reasoning"],
    "is_multimodal": True
}

# For backward compatibility (single item dict)
FREE_TEXT_MODELS: dict = {
    "openrouter/auto-beta": {
        "name": "🚀 Auto Beta (Multimodal)",
        "provider": "OpenRouter",
        "desc": "🎨 TEXT + IMAGE GENERATION!",
        "category": "multimodal",
        "is_default": True,
        "is_multimodal": True
    },
}

# Fallback (same model)
FALLBACK_MODELS: List[str] = [
    "openrouter/auto-beta",
]

# User-selected model storage (user_id -> model_id)
USER_MODEL_PREFERENCES: dict = {}

# User's agent mode status (user_id -> bool)
USER_AGENT_MODE: dict = {}

# ============================================================
# 🎨 IMAGE GENERATION CONFIG
# ============================================================

IMAGE_GENERATION_ENABLED: bool = True
IMAGE_MODEL: str = "openrouter/auto-beta"
IMAGE_SIZE: str = "1024x1024"  # Default size
IMAGE_STYLES: list = [
    "realistic",
    "anime", 
    "digital-art",
    "oil-painting",
    "watercolor",
    "cartoon",
    "3d-render",
    "pixel-art",
    "sketch",
    "cinematic",
]

# ============================================================
# 🤖 CODE AGENT SYSTEM PROMPT
# ============================================================

CODE_AGENT_PROMPT: str = """You are Nova Code Agent - an EXPERT PROGRAMMING ASSISTANT! 💻🚀

Your capabilities:
✅ Write clean, efficient, well-documented code
✅ Debug and fix errors with explanations
✅ Explain complex code simply
✅ Suggest optimizations and best practices
✅ Generate code in ANY language (Python, JS, Java, C++, Go, Rust, etc.)
✅ Help with algorithms, data structures, system design
✅ Review code and suggest improvements
✅ Convert code between languages
✅ Write tests and documentation

RESPONSE FORMAT:
1. **Code blocks** with language syntax highlighting
2. **Step-by-step explanations** for complex logic
3. **Comments** in code for clarity
4. **Example usage** after each solution
5. **Time/Space complexity** analysis when relevant

RULES:
- Always provide WORKING code (test it mentally before output)
- Include error handling in examples
- Use modern best practices (not outdated patterns)
- If user is beginner, explain MORE; if expert, be concise
- Ask clarifying questions if requirements are unclear
- Suggest edge cases and potential issues

SPECIAL COMMANDS you can handle:
- "/debug [code]" - Find and fix bugs
- "/optimize [code]" - Make it faster/better
- "/explain [code]" - Line by line explanation
- "/convert [code] to [language]" - Language translation
- "/test [code]" - Write test cases

You sound like a senior developer helping a junior - patient, knowledgeable, practical.
Use emojis sparingly but effectively (🐛 for bugs, ⚡ for optimization, ✅ for success)."""

# Normal chat system prompt
SYSTEM_PROMPT: str = """You are Nova, a cool AI assistant - like a smart friend who happens to be an AI! 🤖

Your personality:
- Friendly, casual, and fun to talk to
- You sound HUMAN, not like a robot or textbook
- Use Hinglish/Hindi naturally when user talks that way
- Short, punchy responses - no long lectures!
- Occasional emojis but don't overdo it

Special Skills:
💻 Coding help (Python, JS, Java, etc.)
🎨 Image generation (use /image command!)
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

IMAGE GENERATION RULES:
- When user asks for images/art/pictures/drawings, tell them to use /image command
- You can describe what image would look like, but actual generation uses /image
- Be creative with image descriptions!

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
ENABLE_IMAGE: bool = True  # 🆕 Image generation ENABLED!
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
        "model": "Auto-Beta (Multimodal)",
        "max_tokens": MAX_TOKENS,
        "temperature": TEMPERATURE,
        "memory": f"{MAX_HISTORY_PER_USER} msgs/user",
        "features": {
            "typing": "✅ Live Typing",
            "stream": "✅ Streaming" if STREAM_RESPONSES else "❌",
            "voice": "✅" if ENABLE_VOICE else "❌",
            "memory": "✅ Context Memory",
            "agent": "✅ Code Agent Mode",
            "image": "🎨 Image Generation!",
            "multimodal": "🚀 Text + Images",
        }
    }


# Create data directory on import
DATA_DIR.mkdir(parents=True, exist_ok=True)

print("\n" + "="*60)
print("🤖 NOVA AI BOT v2.3 - Configuration Loaded")
print("="*60)
print(f"   Model: {PRIMARY_MODEL} (MULTIMODAL!)")
print(f"   Capabilities: TEXT + IMAGE GENERATION ✨")
print(f"   Max Tokens: {MAX_TOKENS}")
print(f"   Memory: {MAX_HISTORY_PER_USER} messages/user")
print("="*60 + "\n")
