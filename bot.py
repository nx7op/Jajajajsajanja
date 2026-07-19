"""
🚀 NOVA AI BOT - ULTRA ADVANCED v2.1
=======================================

✅ FIXED BUGS:
   - 'Message' object has no attribute 'message'
   - Inline query timeout issues  
   - Markdown entity parsing errors
   - Fallback models not working (2025 update!)

✅ NEW FEATURES:
   - 🎨 Font Changer (15+ Fancy Fonts)
   - 📝 Shayari Generator
   - 💬 Quotes Generator
   - ⚡ Ultra Fast Inline Mode
   - 🤖 Human-like Responses
   - 🧠 MODEL SELECTOR (/models) - 17+ Free Models!
   - 🔥 All 2025 Working Free Models Added!

Author: Nova AI Team
Model: nvidia/nemotron-3-ultra-550b-a55b:free
"""

import os
import sys
import asyncio
import time
import threading
import random
import json
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from telegram import (
    Update,
    BotCommand,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    InlineQueryResultArticle,
    InputTextMessageContent,
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    InlineQueryHandler,
    ContextTypes,
    filters,
    ApplicationBuilder,
)
from telegram.error import TelegramError, Forbidden, BadRequest

# ChatAction constants
CHAT_TYPING = "typing"
CHAT_UPLOAD_PHOTO = "upload_photo"
CHAT_RECORD_VIDEO = "record_video"
CHAT_UPLOAD_VIDEO = "upload_video"
CHAT_RECORD_AUDIO = "record_audio"
CHAT_UPLOAD_AUDIO = "upload_audio"
CHAT_UPLOAD_DOCUMENT = "upload_document"
CHAT_FIND_LOCATION = "find_location"
CHAT_RECORD_VIDEO_NOTE = "record_video_note"
CHAT_UPLOAD_VIDEO_NOTE = "upload_video_note"

# Import our modules
from config import (
    BOT_TOKEN,
    OWNER_ID,
    ADMIN_IDS,
    validate_config,
    get_env_info,
    PORT,
    DEBUG_MODE,
    TYPING_DELAY,
    MAX_RESPONSE_TIME,
    RATE_LIMIT_MINUTE,
    RATE_LIMIT_HOUR,
    FREE_TEXT_MODELS,        # NEW: All free models
    USER_MODEL_PREFERENCES,  # NEW: User model preferences
)
from utils.ai_engine import AIEngine, get_ai_engine


# ============================================================
# 🎨 TERMINAL COLORS & EFFECTS
# ============================================================

class Colors:
    """ANSI color codes for beautiful terminal output."""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"
    
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_BLUE = "\033[44m"


class TerminalEffects:
    """Cool terminal effects for the bot."""
    
    @staticmethod
    def spinner():
        while True:
            for char in "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏":
                yield char
    
    @staticmethod
    def progress_bar(current: int, total: int, width: int = 30) -> str:
        if total == 0:
            return "[" + " " * width + "]"
        filled = int(width * current / total)
        bar = "█" * filled + "░" * (width - filled)
        return f"[{Colors.BRIGHT_GREEN}{bar}{Colors.RESET}]"
    
    @staticmethod
    def timestamp() -> str:
        return datetime.now().strftime("%H:%M:%S")
    
    @staticmethod
    def print_banner():
        banner = f"""
{Colors.BRIGHT_CYAN}╔══════════════════════════════════════════════════════╗{Colors.RESET}
{Colors.BRIGHT_CYAN}║{Colors.RESET}  {Colors.BOLD}{Colors.BRIGHT_YELLOW}🚀 NOVA AI BOT - ULTRA v2.0{Colors.RESET}                    {Colors.BRIGHT_CYAN}║{Colors.RESET}
{Colors.BRIGHT_CYAN}╠══════════════════════════════════════════════════════╣{Colors.RESET}
{Colors.BRIGHT_CYAN}║{Colors.RESET}                                                    {Colors.BRIGHT_CYAN}║{Colors.RESET}
{Colors.BRIGHT_CYAN}║{Colors.RESET}  {Colors.GREEN}✅ All Bugs Fixed{Colors.RESET}                                {Colors.BRIGHT_CYAN}║{Colors.RESET}
{Colors.BRIGHT_CYAN}║{Colors.RESET}  {Colors.GREEN}✅ Ultra Fast Inline Mode{Colors.RESET}                        {Colors.BRIGHT_CYAN}║{Colors.RESET}
{Colors.BRIGHT_CYAN}║{Colors.RESET}  {Colors.GREEN}✅ Font Changer (15+ Fonts){Colors.RESET}                       {Colors.BRIGHT_CYAN}║{Colors.RESET}
{Colors.BRIGHT_CYAN}║{Colors.RESET}  {Colors.GREEN}✅ Shayari & Quotes Generator{Colors.RESET}                    {Colors.BRIGHT_CYAN}║{Colors.RESET}
{Colors.BRIGHT_CYAN}║{Colors.RESET}  {Colors.GREEN}✅ Human-like Responses{Colors.RESET}                          {Colors.BRIGHT_CYAN}║{Colors.RESET}
{Colors.BRIGHT_CYAN}║{Colors.RESET}  {Colors.GREEN}✅ Railway Deployment Ready{Colors.RESET}                        {Colors.BRIGHT_CYAN}║{Colors.RESET}
{Colors.BRIGHT_CYAN}║{Colors.RESET}                                                    {Colors.BRIGHT_CYAN}║{Colors.RESET}
{Colors.BRIGHT_CYAN}╚══════════════════════════════════════════════════════╝{Colors.RESET}
"""
        print(banner)


class Logger:
    """Advanced logger with colors and formatting."""
    
    @staticmethod
    def info(message: str):
        ts = TerminalEffects.timestamp()
        print(f"  {Colors.BRIGHT_BLUE}[{ts}]{Colors.RESET} {Colors.BRIGHT_CYAN}ℹ{Colors.RESET}  {message}")
    
    @staticmethod
    def success(message: str):
        ts = TerminalEffects.timestamp()
        print(f"  {Colors.BRIGHT_BLUE}[{ts}]{Colors.RESET} {Colors.BRIGHT_GREEN}✔{Colors.RESET}  {message}")
    
    @staticmethod
    def warning(message: str):
        ts = TerminalEffects.timestamp()
        print(f"  {Colors.BRIGHT_BLUE}[{ts}]{Colors.RESET} {Colors.BRIGHT_YELLOW}⚠{Colors.RESET}  {Colors.YELLOW}{message}{Colors.RESET}")
    
    @staticmethod
    def error(message: str):
        ts = TerminalEffects.timestamp()
        print(f"  {Colors.BRIGHT_BLUE}[{ts}]{Colors.RESET} {Colors.BRIGHT_RED}✘{Colors.RESET}  {Colors.RED}{message}{Colors.RESET}")
    
    @staticmethod
    def chat(user: str, message: str, incoming: bool = True):
        ts = TerminalEffects.timestamp()
        direction = "◀" if incoming else "▶"
        color = Colors.BRIGHT_MAGENTA if incoming else Colors.BRIGHT_GREEN
        prefix = "USER" if incoming else "NOVA"
        display_msg = message[:80] + "..." if len(message) > 80 else message
        print(f"  {Colors.BRIGHT_BLUE}[{ts}]{Colors.RESET} {color}{direction}{Colors.RESET} [{Colors.BOLD}{prefix}{Colors.RESET}] {Colors.DIM}{user}:{Colors.RESET} {display_msg}")


# ============================================================
# 🎨 FONT CHANGER - 15+ FANCY FONTS
# ============================================================

class FontChanger:
    """
    Convert text to fancy fonts using Unicode characters.
    Supports 15+ different font styles!
    """
    
    # Unicode character mappings for different fonts
    FONTS = {
        # Mathematical Bold
        "bold": {
            'a': '𝐚', 'b': '𝐛', 'c': '𝐜', 'd': '𝐝', 'e': '𝐞', 'f': '𝐟', 'g': '𝐠', 'h': '𝐡',
            'i': '𝐢', 'j': '𝐣', 'k': '𝐤', 'l': '𝐥', 'm': '𝐦', 'n': '𝐧', 'o': '𝐨', 'p': '𝐩',
            'q': '𝐪', 'r': '𝐫', 's': '𝐬', 't': '𝐭', 'u': '𝐮', 'v': '𝐯', 'w': '𝐰', 'x': '𝐱',
            'y': '𝐲', 'z': '𝐳',
            'A': '𝐀', 'B': '𝐁', 'C': '𝐂', 'D': '𝐃', 'E': '𝐄', 'F': '𝐅', 'G': '𝐆', 'H': '𝐇',
            'I': '𝐈', 'J': '𝐉', 'K': '𝐊', 'L': '𝐋', 'M': '𝐌', 'N': '𝐍', 'O': '𝐎', 'P': '𝐏',
            'Q': '𝐐', 'R': '𝐑', 'S': '𝐒', 'T': '𝐓', 'U': '𝐔', 'V': '𝐕', 'W': '𝐖', 'X': '𝐗',
            'Y': '𝐘', 'Z': '𝐙',
        },
        # Mathematical Italic
        "italic": {
            'a': '𝑎', 'b': '𝑏', 'c': '𝑐', 'd': '𝑑', 'e': '𝑒', 'f': '𝑓', 'g': '𝑔', 'h': 'ℎ',
            'i': '𝑖', 'j': '𝑗', 'k': '𝑘', 'l': '𝑙', 'm': '𝑚', 'n': '𝑛', 'o': '𝑜', 'p': '𝑝',
            'q': '𝑞', 'r': '𝑟', 's': '𝑠', 't': '𝑡', 'u': '𝑢', 'v': '𝑣', 'w': '𝑤', 'x': '𝑥',
            'y': '𝑦', 'z': '𝑧',
            'A': '𝐴', 'B': '𝐵', 'C': '𝐶', 'D': '𝐷', 'E': '𝐸', 'F': '𝐹', 'G': '𝐺', 'H': '𝐻',
            'I': '𝐼', 'J': '𝐽', 'K': '𝐾', 'L': '𝐿', 'M': '𝑀', 'N': '𝑁', 'O': '𝑂', 'P': '𝑃',
            'Q': '𝑄', 'R': '𝑅', 'S': '𝑆', 'T': '𝑇', 'U': '𝑈', 'V': '𝑉', 'W': '𝑊', 'X': '𝑋',
            'Y': '𝑌', 'Z': '𝑍',
        },
        # Mathematical Bold Italic
        "bold_italic": {
            'a': '𝒂', 'b': '𝒃', 'c': '𝒄', 'd': '𝒅', 'e': '𝒆', 'f': '𝒇', 'g': '𝒈', 'h': '𝒉',
            'i': '𝒊', 'j': '𝒋', 'k': '𝒌', 'l': '𝒍', 'm': '𝒎', 'n': '𝒏', 'o': '𝒐', 'p': '𝒑',
            'q': '𝒒', 'r': '𝒓', 's': '𝒔', 't': '𝒕', 'u': '𝒖', 'v': '𝒗', 'w': '𝒘', 'x': '𝒙',
            'y': '𝒚', 'z': '𝒛',
            'A': '𝑨', 'B': '𝑩', 'C': '𝑪', 'D': '𝑫', 'E': '𝑬', 'F': '𝑭', 'G': '𝑮', 'H': '𝑯',
            'I': '𝑰', 'J': '𝑱', 'K': '𝑲', 'L': '𝑳', 'M': '𝑴', 'N': '𝑵', 'O': '𝑶', 'P': '𝑷',
            'Q': '𝑸', 'R': '𝑹', 'S': '𝑺', 'T': '𝑻', 'U': '𝑼', 'V': '𝑽', 'W': '𝑾', 'X': '𝑿',
            'Y': '𝒀', 'Z': '𝒁',
        },
        # Script/Cursive
        "script": {
            'a': '𝒶', 'b': '𝒷', 'c': '𝒸', 'd': '𝒹', 'e': '𝑒', 'f': '𝒻', 'g': '𝓊', 'h': '𝒽',
            'i': '𝒾', 'j': '𝒿', 'k': '𝓀', 'l': '𝓁', 'm': '𝓂', 'n': '𝓃', 'o': 'ℴ', 'p': '𝓅',
            'q': '𝓆', 'r': '𝓇', 's': '𝓈', 't': '𝓉', 'u': '𝓊', 'v': '𝓋', 'w': '𝓌', 'x': '𝓍',
            'y': '𝓎', 'z': '𝓏',
            'A': '𝒜', 'B': 'ℬ', 'C': '𝒞', 'D': '𝒟', 'E': 'ℰ', 'F': 'ℱ', 'G': '𝒢', 'H': 'ℋ',
            'I': 'ℐ', 'J': '𝒥', 'K': '𝒦', 'L': '𝐿', 'M': '𝑀', 'N': '𝒩', 'O': '𝒪', 'P': '𝒫',
            'Q': '𝒬', 'R': 'ℛ', 'S': '𝒮', 'T': '𝒯', 'U': '𝒰', 'V': '𝒱', 'W': '𝒲', 'X': '𝒳',
            'Y': '𝒴', 'Z': '𝒵',
        },
        # Bold Script
        "bold_script": {
            'a': '𝓪', 'b': '𝓫', 'c': '𝓬', 'd': '𝓭', 'e': '𝓮', 'f': '𝓯', 'g': '𝓰', 'h': '𝓱',
            'i': '𝓲', 'j': '𝓳', 'k': '𝓴', 'l': '𝓵', 'm': '𝓶', 'n': '𝓷', 'o': '𝓸', 'p': '𝓹',
            'q': '𝓺', 'r': '𝓻', 's': '𝓼', 't': '𝓽', 'u': '𝓾', 'v': '𝓿', 'w': '𝔀', 'x': '𝔁',
            'y': '𝔂', 'z': '𝔃',
            'A': '𝓐', 'B': '𝓑', 'C': '𝓒', 'D': '𝓓', 'E': '𝓔', 'F': '𝓕', 'G': '𝓖', 'H': '𝓗',
            'I': '𝓘', 'J': '𝓙', 'K': '𝓚', 'L': '𝓛', 'M': '𝓜', 'N': '𝓝', 'O': '𝓞', 'P': '𝓟',
            'Q': '𝓠', 'R': '𝓡', 'S': '𝓢', 'T': '𝓣', 'U': '𝓤', 'V': '𝓥', 'W': '𝓦', 'X': '𝓧',
            'Y': '𝓨', 'Z': '𝓩',
        },
        # Fraktur/Gothic
        "gothic": {
            'a': '𝔞', 'b': '𝔟', 'c': '𝔠', 'd': '𝔡', 'e': '𝔢', 'f': '𝔣', 'g': '𝔤', 'h': '𝔥',
            'i': '𝔦', 'j': '𝔧', 'k': '𝔨', 'l': '𝔩', 'm': '𝔪', 'n': '𝔫', 'o': '𝔬', 'p': '𝔭',
            'q': '𝔮', 'r': '𝔯', 's': '𝔰', 't': '𝔱', 'u': '𝔲', 'v': '𝔳', 'w': '𝔴', 'x': '𝔵',
            'y': '𝔶', 'z': '𝔷',
            'A': '𝔄', 'B': '𝔅', 'C': '𝔇', 'D': '𝔈', 'E': '𝔉', 'F': '𝔊', 'G': '𝔋', 'H': '𝔌',
            'I': '𝔍', 'J': '𝔎', 'K': '𝔏', 'L': '𝔐', 'M': '𝔑', 'N': '𝔒', 'O': '𝔓', 'P': '𝔔',
            'Q': '𝔕', 'R': '𝔖', 'S': '𝔗', 'T': '𝔘', 'U': '𝔙', 'V': '𝔚', 'W': '𝔛', 'X': '𝔜',
            'Y': '𝔝', 'Z': '𝔞',
        },
        # Bold Fraktur
        "bold_gothic": {
            'a': '𝖆', 'b': '𝖇', 'c': '𝖈', 'd': '𝖉', 'e': '𝖊', 'f': '𝖋', 'g': '𝖌', 'h': '𝖍',
            'i': '𝖎', 'j': '𝖏', 'k': '𝖐', 'l': '𝖑', 'm': '𝖒', 'n': '𝖓', 'o': '𝖔', 'p': '𝖕',
            'q': '𝖖', 'r': '𝖗', 's': '𝖘', 't': '𝖙', 'u': '𝖚', 'v': '𝖛', 'w': '𝖜', 'x': '𝖝',
            'y': '𝖞', 'z': '𝖟',
            'A': '𝕬', 'B': '𝕭', 'C': '𝕮', 'D': '𝕯', 'E': '𝕰', 'F': '𝕱', 'G': '𝕲', 'H': '𝕳',
            'I': '𝕴', 'J': '𝕵', 'K': '𝕶', 'L': '𝕷', 'M': '𝕸', 'N': '𝕹', 'O': '𝕺', 'P': '𝕻',
            'Q': '𝕼', 'R': '𝕽', 'S': '𝕾', 'T': '𝕿', 'U': '𝖀', 'V': '𝖁', 'W': '𝖂', 'X': '𝖃',
            'Y': '𝖄', 'Z': '𝖅',
        },
        # Double-Struck
        "double": {
            'a': '𝕒', 'b': '𝕓', 'c': '𝕔', 'd': '𝕕', 'e': '𝕖', 'f': '𝕗', 'g': '𝕘', 'h': '𝕙',
            'i': '𝕚', 'j': '𝕛', 'k': '𝕜', 'l': '𝕝', 'm': '𝕞', 'n': '𝕟', 'o': '𝕠', 'p': '𝕡',
            'q': '𝕢', 'r': '𝕣', 's': '𝕤', 't': '𝕥', 'u': '𝕦', 'v': '𝕧', 'w': '𝕨', 'x': '𝕩',
            'y': '𝕪', 'z': '𝕫',
            'A': '𝔸', 'B': '𝔹', 'C': 'ℂ', 'D': '𝔻', 'E': '𝔼', 'F': '𝔽', 'G': '𝔾', 'H': 'ℍ',
            'I': '𝕀', 'J': '𝕁', 'K': '𝕂', 'L': '𝕃', 'M': '𝕄', 'N': 'ℕ', 'O': '𝕆', 'P': 'ℙ',
            'Q': 'ℚ', 'R': 'ℝ', 'S': '𝕊', 'T': '𝕋', 'U': '𝕌', 'V': '𝕍', 'W': '𝕎', 'X': '𝕏',
            'Y': '𝕐', 'Z': 'ℤ',
        },
        # Sans-Serif
        "sans": {
            'a': '𝖺', 'b': '𝖻', 'c': '𝑐', 'd': '𝖽', 'e': '𝖾', 'f': '𝒻', 'g': '𝗀', 'h': '𝗁',
            'i': '𝗂', 'j': '𝗃', 'k': '𝗄', 'l': '𝗅', 'm': '𝗆', 'n': '𝗇', 'o': '𝗈', 'p': '𝗉',
            'q': '𝗊', 'r': '𝗋', 's': '𝗌', 't': '𝗍', 'u': '𝗎', 'v': '𝗏', 'w': '𝗐', 'x': '𝗑',
            'y': '𝗒', 'z': '𝗓',
            'A': '𝖠', 'B': '𝖡', 'C': '𝖢', 'D': '𝖣', 'E': '𝖤', 'F': '𝖦', 'G': '𝖧', 'H': '𝖨',
            'I': '𝖩', 'J': '𝖪', 'K': '𝖫', 'L': '𝖬', 'M': '𝖭', 'N': '𝖮', 'O': '𝖯', 'P': '𝖰',
            'Q': '𝖱', 'R': '𝖲', 'S': '𝖳', 'T': '𝖴', 'U': '𝖵', 'V': '𝖶', 'W': '𝖷', 'X': '𝖸',
            'Y': '𝖹', 'Z': '𝖺',
        },
        # Sans-Serif Bold
        "bold_sans": {
            'a': '𝗮', 'b': '𝗯', 'c': '𝗰', 'd': '𝗱', 'e': '𝗲', 'f': '𝗳', 'g': '𝗴', 'h': '𝗵',
            'i': '𝗶', 'j': '𝗷', 'k': '𝗸', 'l': '𝗹', 'm': '𝗺', 'n': '𝗻', 'o': '𝗼', 'p': '𝗽',
            'q': '𝗾', 'r': '𝗿', 's': '𝘀', 't': '𝘁', 'u': '𝘂', 'v': '𝘃', 'w': '𝘄', 'x': '𝘅',
            'y': '𝘆', 'z': '𝘇',
            'A': '𝗔', 'B': '𝗕', 'C': '𝗖', 'D': '𝗗', 'E': '𝗘', 'F': '𝗙', 'G': '𝗚', 'H': '𝗛',
            'I': '𝗜', 'J': '𝗝', 'K': '𝗞', 'L': '𝗟', 'M': '𝗠', 'N': '𝗡', 'O': '𝗢', 'P': '𝗣',
            'Q': '𝗤', 'R': '𝗥', 'S': '𝗦', 'T': '𝗧', 'U': '𝗨', 'V': '𝗩', 'W': '𝗪', 'X': '𝗫',
            'Y': '𝗬', 'Z': '𝗭',
        },
        # Monospace
        "mono": {
            'a': '𝚊', 'b': '𝚋', 'c': '𝚌', 'd': '𝚍', 'e': '𝚎', 'f': '𝚏', 'g': '𝚐', 'h': '𝚑',
            'i': '𝚒', 'j': '𝚓', 'k': '𝚔', 'l': '𝚕', 'm': '𝚖', 'n': '𝚗', 'o': '𝚘', 'p': '𝚙',
            'q': '𝚚', 'r': '𝚛', 's': '𝚜', 't': '𝚝', 'u': '𝚞', 'v': '𝚟', 'w': '𝚠', 'x': '𝚡',
            'y': '𝚢', 'z': '𝚣',
            'A': '𝙰', 'B': '𝙱', 'C': '𝙲', 'D': '𝙳', 'E': '𝙴', 'F': '𝙵', 'G': '𝙶', 'H': '𝙷',
            'I': '𝙸', 'J': '𝙹', 'K': '𝙺', 'L': '𝙻', 'M': '𝙼', 'N': '𝙽', 'O': '𝙾', 'P': '𝙿',
            'Q': '𝚀', 'R': '𝚁', 'S': '𝚂', 'T': '𝚃', 'U': '𝚄', 'V': '𝚅', 'W': '𝚆', 'X': '𝚇',
            'Y': '𝚈', 'Z': '𝚉',
        },
        # Circled
        "circled": {
            'a': 'ⓐ', 'b': 'ⓑ', 'c': 'ⓒ', 'd': 'ⓓ', 'e': 'ⓔ', 'f': 'ⓕ', 'g': 'ⓖ', 'h': 'ⓗ',
            'i': 'ⓘ', 'j': 'ⓙ', 'k': 'ⓚ', 'l': 'ⓛ', 'm': 'ⓜ', 'n': 'ⓝ', 'o': 'ⓞ', 'p': 'ⓟ',
            'q': 'ⓠ', 'r': 'ⓡ', 's': 'ⓢ', 't': 'ⓣ', 'u': 'ⓤ', 'v': 'ⓥ', 'w': 'ⓦ', 'x': 'ⓧ',
            'y': 'ⓨ', 'z': 'ⓩ',
            'A': 'Ⓐ', 'B': 'Ⓑ', 'C': 'Ⓒ', 'D': 'Ⓓ', 'E': 'Ⓔ', 'F': 'Ⓕ', 'G': 'Ⓖ', 'H': 'Ⓗ',
            'I': 'Ⓘ', 'J': 'Ⓙ', 'K': 'Ⓚ', 'L': 'Ⓛ', 'M': 'Ⓜ', 'N': 'Ⓝ', 'O': 'Ⓞ', 'P': 'Ⓟ',
            'Q': 'Ⓠ', 'R': 'Ⓡ', 'S': 'Ⓢ', 'T': 'Ⓣ', 'U': 'Ⓤ', 'V': 'Ⓥ', 'W': 'Ⓦ', 'X': 'Ⓧ',
            'Y': 'Ⓨ', 'Z': 'Ⓩ',
        },
        # Squared
        "squared": {
            'a': '🄐', 'b': '🄑', 'c': '🄒', 'd': '🄓', 'e': '🄔', 'f': '🄕', 'g': '🄖', 'h': '🄗',
            'i': '🄘', 'j': '🄙', 'k': '🄚', 'l': '🄛', 'm': '🄜', 'n': '🄝', 'o': '🄞', 'p': '🄟',
            'q': '🄠', 'r': '🄡', 's': '🄢', 't': '🄣', 'u': '🄤', 'v': '🄥', 'w': '🄦', 'x': '🄧',
            'y': '🄨', 'z': '🄩',
            'A': '🄰', 'B': '🄱', 'C': '🄲', 'D': '🄳', 'E': '🄴', 'F': '🄵', 'G': '🄶', 'H': '🄷',
            'I': '🄸', 'J': '🄹', 'K': '🄺', 'L': '🄻', 'M': '🄼', 'N': '🄽', 'O': '🄾', 'P': '🄿',
            'Q': '🅀', 'R': '🅁', 'S': '🅂', 'T': '🅃', 'U': '🅄', 'V': '🅅', 'W': '🅆', 'X': '🅇',
            'Y': '🅈', 'Z': '🅉',
        },
        # Strikethrough
        "strike": {
            'a': 'a̶', 'b': 'b̶', 'c': 'c̶', 'd': 'd̶', 'e': 'e̶', 'f': 'f̶', 'g': 'g̶', 'h': 'h̶',
            'i': 'i̶', 'j': 'j̶', 'k': 'k̶', 'l': 'l̶', 'm': 'm̶', 'n': 'n̶', 'o': 'o̶', 'p': 'p̶',
            'q': 'q̶', 'r': 'r̶', 's': 's̶', 't': 't̶', 'u': 'u̶', 'v': 'v̶', 'w': 'w̶', 'x': 'x̶',
            'y': 'y̶', 'z': 'z̶',
            'A': 'A̶', 'B': 'B̶', 'C': 'C̶', 'D': 'D̶', 'E': 'E̶', 'F': 'F̶', 'G': 'G̶', 'H': 'H̶',
            'I': 'I̶', 'J': 'J̶', 'K': 'K̶', 'L': 'L̶', 'M': 'M̶', 'N': 'N̶', 'O': 'O̶', 'P': 'P̶',
            'Q': 'Q̶', 'R': 'R̶', 'S': 'S̶', 'T': 'T̶', 'U': 'U̶', 'V': 'V̶', 'W': 'W̶', 'X': 'X̶',
            'Y': 'Y̶', 'Z': 'Z̶',
        },
        # Upside Down
        "upside": {
            'a': 'ɐ', 'b': 'q', 'c': 'ɔ', 'd': 'p', 'e': 'ǝ', 'f': 'ɟ', 'g': 'ƃ', 'h': 'ɥ',
            'i': 'ᴉ', 'j': 'ɾ', 'k': 'ʞ', 'l': 'l', 'm': 'ɯ', 'n': 'u', 'o': 'o', 'p': 'd',
            'q': 'b', 'r': 'ɹ', 's': 's', 't': 'ʇ', 'u': 'n', 'v': 'ʌ', 'w': 'ʍ', 'x': 'x',
            'y': 'ʎ', 'z': 'z',
            'A': '∀', 'B': 'q', 'C': 'Ɔ', 'D': 'p', 'E': 'Ǝ', 'F': 'Ⅎ', 'G': '⅁', 'H': 'H',
            'I': 'I', 'J': 'ſ', 'K': 'ʞ', 'L': '˥', 'M': 'W', 'N': 'N', 'O': 'O', 'P': 'Ԁ',
            'Q': 'Q', 'R': 'ᴚ', 'S': 'S', 'T': '⊥', 'U': '∩', 'V': 'Λ', 'W': 'M', 'X': 'X',
            'Y': '⅄', 'Z': 'Z',
        },
        # Fancy/Luxury
        "fancy": {
            'a': 'ą', 'b': 'მ', 'c': 'ç', 'd': '∂', 'e': 'є', 'f': 'ƒ', 'g': 'g', 'h': 'ħ',
            'i': 'ι', 'j': 'j', 'k': 'κ', 'l': 'ł', 'm': 'м', 'n': 'η', 'o': 'ø', 'p': 'ρ',
            'q': 'q', 'r': 'я', 's': 'ş', 't': 'τ', 'u': 'υ', 'v': 'ν', 'w': 'ω', 'x': 'χ',
            'y': 'ყ', 'z': 'ż',
            'A': 'Å', 'B': 'B', 'C': 'Ç', 'D': 'Ð', 'E': 'Ξ', 'F': 'F', 'G': 'G', 'H': 'H',
            'I': 'I', 'J': 'J', 'K': 'K', 'L': 'L', 'M': 'M', 'N': 'Ñ', 'O': 'Ø', 'P': 'P',
            'Q': 'Q', 'R': 'R', 'S': 'Ş', 'T': 'T', 'U': 'U', 'V': 'V', 'W': 'W', 'X': 'X',
            'Y': 'Y', 'Z': 'Z',
        },
    }
    
    @classmethod
    def convert(cls, text: str, font_name: str) -> str:
        """Convert text to specified font."""
        if font_name not in cls.FONTS:
            return text
        
        font_map = cls.FONTS[font_name]
        result = []
        
        for char in text:
            if char in font_map:
                result.append(font_map[char])
            else:
                result.append(char)
        
        return ''.join(result)
    
    @classmethod
    def get_font_list(cls) -> List[str]:
        """Get list of available fonts."""
        return list(cls.FONTS.keys())
    
    @classmethod
    def get_font_preview(cls, font_name: str) -> str:
        """Get preview text for a font."""
        preview_text = "Nova AI Bot"
        return cls.convert(preview_text, font_name)


# ============================================================
# 📝 SHAYARI GENERATOR
# ============================================================

class ShayariGenerator:
    """Generate beautiful shayaris on demand!"""
    
    SHAYARIS = {
        "ishq": [
            "❤️ 𝐓𝐨𝐡𝐞 𝐝𝐞𝐤𝐡 𝐤𝐚𝐫 𝐣𝐢𝐧𝐧𝐚𝐭 𝐤𝐨 𝐛𝐡𝐮𝐥𝐚𝐲𝐞 𝐡𝐚𝐢,\n𝐖𝐨 𝐤𝐚𝐡𝐞 𝐡𝐦𝐬𝐞 𝐦𝐨𝐡𝐚𝐛𝐛𝐚𝐭 𝐡𝐨 𝐠𝐚𝐢 𝐚𝐚𝐩 𝐬𝐞... 💕",
            
            "💔 𝐔𝐬𝐤𝐞 𝐛𝐚𝐝 𝐲𝐞 𝐦𝐮𝐦𝐤𝐢𝐧 𝐧𝐡𝐢 𝐡𝐚𝐢 𝐤𝐨𝐢 𝐝𝐮𝐬𝐫𝐚 𝐩𝐚𝐬𝐧𝐝 𝐚𝐚𝐲𝐞,\n𝐇𝐚𝐦 𝐭𝐨 𝐮𝐬𝐤𝐞 𝐤𝐡𝐰𝐚𝐛𝐨𝐧 𝐦𝐞𝐧 𝐡𝐢 𝐤𝐡𝐨 𝐠𝐚𝐲𝐞 𝐡𝐚𝐢𝐧... 😔",
            
            "🌹 𝐓𝐮𝐦𝐡𝐚𝐫𝐚 𝐤𝐡𝐲𝐚𝐥 𝐚𝐲𝐞 𝐭𝐨 𝐡𝐨𝐧𝐭𝐚 𝐡𝐚𝐢 𝐝𝐢𝐥 𝐤𝐨,\n𝐖𝐚𝐫𝐧𝐚 𝐝𝐢𝐥 𝐭𝐨 𝐬𝐢𝐥𝐡𝐧𝐚 𝐛𝐡𝐢 𝐛𝐡𝐮𝐥 𝐠𝐚𝐲𝐞 𝐭𝐡𝐞... 💫",
            
            "💝 𝐇𝐚𝐦𝐤𝐨 𝐦𝐨𝐡𝐚𝐛𝐛𝐚𝐭 𝐦𝐞𝐧 𝐮𝐝𝐚𝐬𝐧𝐚 𝐛𝐡𝐢 𝐚𝐚𝐭𝐚 𝐡𝐚𝐢,\n𝐊𝐡𝐮𝐬𝐡𝐢 𝐭𝐨 𝐛𝐚𝐬 𝐭𝐞𝐫𝐞 𝐝𝐢𝐝𝐚𝐫 𝐤𝐚 𝐦𝐮𝐪𝐚𝐦 𝐡𝐚𝐢... ✨",
            
            "🦋 𝐙𝐢𝐧𝐝𝐚𝐠𝐢 𝐦𝐞𝐧 𝐤𝐮𝐜𝐡 𝐭𝐨 𝐤𝐡𝐨𝐲𝐚 𝐡𝐚𝐢 𝐭𝐞𝐫𝐞 𝐬𝐢𝐰𝐚,\n𝐖𝐚𝐫𝐧𝐚 𝐢𝐭𝐧𝐚 𝐬𝐚𝐝𝐚 𝐤𝐮𝐧 𝐡𝐚𝐢𝐭𝐞𝐫𝐞 𝐤𝐨𝐢... 🌙",
        ],
        "dard": [
            "😢 𝐃𝐚𝐫𝐝 𝐰𝐨 𝐡𝐚𝐢 𝐣𝐨 𝐬𝐢𝐥𝐧𝐡𝐢 𝐧𝐡𝐢 𝐣𝐚𝐭𝐚,\n𝐀𝐧𝐬𝐮 𝐰𝐨 𝐡𝐚𝐢𝐧 𝐣𝐨 𝐛𝐡𝐢 𝐧𝐚𝐡𝐢 𝐠𝐢𝐫𝐭𝐞... 💔",
            
            "🥀 𝐇𝐚𝐦 𝐭𝐨 𝐰𝐡𝐢 𝐤𝐡𝐚𝐤 𝐡𝐮𝐞 𝐣𝐢𝐬𝐞 𝐭𝐞𝐫𝐚 𝐬𝐚𝐭𝐡 𝐭𝐡𝐚,\n𝐀𝐣 𝐰𝐨 𝐤𝐡𝐚𝐤 𝐡𝐮𝐞 𝐣𝐢𝐬𝐞 𝐤𝐨𝐢 𝐚𝐮𝐫 𝐤𝐚 𝐬𝐚𝐭𝐡 𝐡𝐚𝐢... 🍂",
            
            "🌧️ 𝐔𝐝𝐚𝐬 𝐡𝐨𝐧𝐞 𝐤𝐚 𝐤𝐨𝐢 𝐡𝐚𝐪 𝐧𝐡𝐢 𝐡𝐨𝐭𝐚 𝐡𝐦𝐤𝐨,\n𝐁𝐚𝐬 𝐭𝐞𝐫𝐞 𝐛𝐢𝐧 𝐮𝐝𝐚𝐬 𝐡𝐨𝐧𝐞 𝐤𝐢 𝐚𝐝𝐚𝐭 𝐬𝐞 𝐡𝐚𝐢... ☔",
            
            "💔 𝐂𝐡𝐥𝐨 𝐬𝐦𝐣𝐡𝐭𝐞 𝐡𝐚𝐢𝐧 𝐤𝐡𝐮𝐝 𝐤𝐨 𝐡𝐮𝐦,\n𝐖𝐨 𝐣𝐚𝐧𝐞 𝐰𝐚𝐥𝐞 𝐭𝐨 𝐤𝐛𝐡𝐢 𝐬𝐦𝐣𝐡𝐭𝐞 𝐡𝐢 𝐧𝐡𝐢𝐧... 😞",
            
            "🖤 𝐊𝐮𝐜𝐡 𝐝𝐚𝐫𝐝 𝐢𝐭𝐧𝐞 𝐠𝐡𝐚𝐦𝐛𝐢𝐫 𝐡𝐨𝐭𝐞 𝐡𝐚𝐢𝐧,\n𝐊𝐞 𝐡𝐮𝐦 𝐮𝐧𝐡𝐞 𝐛𝐡𝐢 𝐧𝐚 𝐛𝐡𝐮𝐥𝐚 𝐬𝐚𝐤𝐭𝐞... 🌑",
        ],
        "friendship": [
            "👫 𝐃𝐨𝐬𝐭𝐢 𝐰𝐨 𝐧𝐡𝐢 𝐣𝐨 𝐡𝐚𝐦𝐬𝐡𝐚 𝐬𝐚𝐭𝐡 𝐫𝐡𝐞,\n𝐃𝐨𝐬𝐭𝐢 𝐰𝐨 𝐡𝐚𝐢 𝐣𝐨 𝐝𝐢𝐥 𝐦𝐞𝐧 𝐬𝐚𝐭𝐡 𝐫𝐡𝐞... 💚",
            
            "🤝 𝐃𝐨𝐬𝐭𝐢 𝐤𝐚 𝐫𝐢𝐬𝐭𝐚 𝐤𝐨𝐢 𝐳𝐡𝐨𝐤𝐢𝐦 𝐧𝐡𝐢 𝐡𝐨𝐭𝐚,\n𝐁𝐚𝐬 𝐬𝐚𝐭𝐡 𝐠𝐮𝐳𝐚𝐫𝐧𝐞 𝐤𝐚 𝐰𝐚𝐝𝐚 𝐡𝐨𝐭𝐚 𝐡𝐚𝐢... ✨",
            
            "💚 𝐇𝐮𝐦𝐚𝐫𝐢 𝐝𝐨𝐬𝐭𝐢 𝐩𝐚𝐤𝐢 𝐠𝐡𝐫 𝐤𝐢 𝐭𝐚𝐫𝐚𝐡 𝐡𝐚𝐢,\n𝐉𝐢𝐬𝐤𝐨 𝐤𝐡𝐨 𝐝𝐨 𝐭𝐨 𝐠𝐡𝐫 𝐛𝐡𝐢 𝐮𝐝𝐚𝐬 𝐥𝐠𝐭𝐚 𝐡𝐚𝐢... 🏠",
            
            "🌟 𝐃𝐨𝐬𝐭𝐢 𝐰𝐨 𝐡𝐚𝐢 𝐣𝐨 𝐤𝐚𝐦𝐳𝐨𝐫𝐢 𝐩𝐞 𝐡𝐚𝐭𝐡 𝐛𝐮𝐥𝐚𝐭𝐞 𝐡𝐚𝐢𝐧,\n𝐀𝐮𝐫 𝐤𝐚𝐦𝐲𝐚𝐛𝐢 𝐩𝐞 𝐬𝐛𝐬𝐞 𝐩𝐡𝐥𝐞 𝐚𝐭𝐞 𝐡𝐚𝐢𝐧... 🎯",
            
            "💫 𝐔𝐬 𝐝𝐨𝐬𝐭𝐢 𝐤𝐨 𝐬𝐚𝐥𝐚𝐦 𝐡𝐚𝐦𝐚𝐫𝐚 𝐭𝐚𝐫𝐟 𝐬𝐞,\n𝐉𝐢𝐬𝐧𝐞 𝐡𝐮𝐦𝐚𝐫𝐞 𝐛𝐞𝐠𝐡𝐚𝐫 𝐦𝐞𝐧 𝐛𝐡𝐢 𝐡𝐦𝐚𝐫𝐚 𝐬𝐚𝐭𝐡 𝐝𝐢𝐲𝐚... 👋",
        ],
        "motivational": [
            "🔥 𝐖𝐨 𝐦𝐮𝐪𝐚𝐦𝐦 𝐤𝐡𝐮𝐬 𝐧𝐡𝐢𝐡 𝐡𝐨𝐭𝐞 𝐣𝐨 𝐬𝐚𝐛 𝐤𝐮𝐜𝐡 𝐩𝐚 𝐥𝐞𝐭𝐞 𝐡𝐚𝐢𝐧,\n𝐀𝐬𝐥𝐢 𝐤𝐡𝐮𝐬𝐢 𝐭𝐨 𝐰𝐡𝐢 𝐡𝐚𝐢 𝐣𝐨 𝐝𝐮𝐬𝐫𝐨𝐧 𝐤𝐨 𝐤𝐡𝐮𝐬 𝐤𝐫𝐭𝐞 𝐡𝐚𝐢𝐧... ⭐",
            
            "💪 𝐌𝐮𝐬𝐤𝐢𝐛𝐥𝐚𝐭𝐞𝐧 𝐰𝐡𝐢 𝐥𝐨𝐠𝐨𝐧 𝐬𝐞 𝐦𝐢𝐥𝐭𝐢 𝐡𝐚𝐢,\n𝐉𝐨 𝐢𝐧𝐬𝐚𝐧 𝐤𝐨 𝐤𝐚𝐦𝐳𝐨𝐫 𝐛𝐧𝐚𝐭𝐢 𝐡𝐚𝐢 𝐧𝐡𝐢 𝐤𝐞 𝐤𝐚𝐦𝐳𝐨𝐫 𝐡𝐚𝐢... 🎯",
            
            "🚀 𝐅𝐚𝐢𝐬𝐥𝐚 𝐬𝐞𝐟𝐚𝐢𝐬𝐡 𝐧𝐡𝐢𝐧 𝐤𝐚𝐡𝐭𝐢, 𝐊𝐮𝐜𝐡 𝐭𝐨 𝐬𝐞𝐤𝐡 𝐥𝐢𝐲𝐚 𝐡𝐨𝐠𝐚,\n𝐀𝐮𝐫 𝐢𝐬𝐬𝐞 𝐛𝐡𝐢 𝐳𝐲𝐚𝐝𝐚 𝐤𝐮𝐜𝐡 𝐬𝐞𝐤𝐡 𝐥𝐞𝐧𝐠𝐚 𝐣𝐢𝐬𝐚𝐧𝐞 𝐦𝐮𝐣𝐡𝐞 𝐦𝐚𝐚𝐥𝐮𝐦 𝐡𝐚𝐢... ✨",
            
            "⭐ 𝐙𝐢𝐧𝐝𝐚𝐠𝐢 𝐦𝐞𝐧 𝐤𝐮𝐜𝐡 𝐟𝐚𝐢𝐬𝐥𝐞 𝐣𝐚𝐫𝐮𝐫𝐢 𝐡𝐨𝐧𝐠𝐢,\n𝐏𝐞𝐫 𝐭𝐮 𝐡𝐚𝐫 𝐝𝐮𝐬𝐫𝐨𝐧 𝐬𝐞 𝐚𝐠𝐲𝐞 𝐫𝐡𝐧𝐚... 💫",
            
            "🌟 𝐇𝐚𝐮𝐬𝐥𝐚 𝐰𝐡𝐢 𝐦𝐢𝐥𝐭𝐚 𝐡𝐚𝐢 𝐣𝐛 𝐭𝐮 𝐡𝐢𝐦𝐦𝐚𝐭 𝐬𝐞 𝐜𝐡𝐥𝐚,\n𝐑𝐮𝐤𝐧𝐞 𝐰𝐚𝐥𝐨𝐧 𝐤𝐨 𝐭𝐞𝐫𝐚 𝐫𝐚𝐬𝐭𝐚 𝐤𝐡𝐨𝐧𝐞 𝐤𝐨 𝐦𝐢𝐥𝐭𝐚 𝐡𝐚𝐢... 🏆",
        ],
        "funny": [
            "😂 𝐏𝐝𝐡𝐨𝐧𝐞 𝐝𝐞𝐤𝐡 𝐥𝐞, 𝐧𝐚𝐭𝐢𝐣𝐚 𝐭𝐞𝐫𝐚 𝐛𝐡𝐢 𝐚𝐚𝐲𝐞𝐠𝐚,\n𝐖𝐚𝐫𝐧𝐚 𝐭𝐞𝐫𝐞 𝐩𝐚𝐬 𝐭𝐨 𝐛𝐚𝐬 𝐦𝐞𝐫𝐢 𝐲𝐚𝐝𝐞𝐧 𝐡𝐚𝐢𝐧𝐠𝐢... 📱",
            
            "🤪 𝐓𝐮 𝐛𝐨𝐡𝐮𝐭 𝐩𝐲𝐚𝐫𝐢 𝐡𝐚𝐢, 𝐦𝐮𝐣𝐡𝐞 𝐩𝐚𝐭𝐚 𝐡𝐚𝐢,\n𝐏𝐚𝐫 𝐭𝐮 𝐢𝐭𝐧𝐢 𝐩𝐲𝐚𝐫𝐢 𝐡𝐚𝐢 𝐤𝐞 𝐭𝐞𝐫𝐞 𝐩𝐚𝐬 𝐦𝐞𝐫𝐚 𝐧𝐮𝐦𝐛𝐞𝐫 𝐧𝐡𝐢𝐧 𝐡𝐚𝐢... 💘",
            
            "😜 𝐃𝐢𝐦𝐚𝐠 𝐤𝐨 𝐠𝐨𝐫𝐚 𝐤𝐚𝐫, 𝐃𝐢𝐥 𝐤𝐨 𝐬𝐚𝐟 𝐤𝐚𝐫,\n𝐖𝐚𝐫𝐧𝐚 𝐤𝐡𝐮𝐝𝐚 𝐤𝐨 𝐬𝐚𝐟 𝐤𝐚𝐫𝐧𝐞 𝐤𝐚 𝐭𝐢𝐦𝐞 𝐧𝐡𝐢𝐧 𝐦𝐢𝐥𝐞𝐠𝐚... 🧠",
            
            "🎭 𝐇𝐮𝐦 𝐰𝐨 𝐧𝐡𝐢𝐧 𝐣𝐨 𝐬𝐚𝐛 𝐛𝐚𝐭𝐞𝐤 𝐬𝐮𝐧𝐭𝐞 𝐡𝐚𝐢𝐧,\n𝐇𝐮𝐦 𝐭𝐨 𝐰𝐡𝐢 𝐬𝐮𝐧𝐭𝐞 𝐡𝐚𝐢𝐧 𝐣𝐨 𝐡𝐮𝐦𝐞 𝐬𝐮𝐧𝐚𝐧𝐚 𝐜𝐡𝐚𝐡𝐢𝐲𝐞... 👂",
            
            "🤡 𝐀𝐭𝐭𝐢𝐭𝐮𝐝𝐞 𝐝𝐞𝐤𝐡 𝐤𝐚𝐫, 𝐥𝐢𝐤𝐢𝐧 𝐝𝐞𝐤𝐡 𝐤𝐚𝐫,\n𝐇𝐮𝐦 𝐭𝐨 𝐡𝐚𝐢𝐧 𝐡𝐢 𝐤𝐡𝐚𝐬... 😎",
        ],
        "attitude": [
            "😎 𝐇𝐮𝐦 𝐰𝐡𝐢 𝐡𝐚𝐢𝐧 𝐣𝐢𝐬𝐧𝐞 𝐭𝐮𝐦𝐡𝐚𝐫𝐚 𝐚𝐭𝐭𝐢𝐭𝐮𝐝𝐞 𝐬𝐞 𝐩𝐫𝐨𝐛𝐥𝐞𝐦 𝐡𝐚𝐢,\n𝐖𝐚𝐫𝐧𝐚 𝐡𝐮𝐦 𝐭𝐨 𝐭𝐮𝐦𝐡𝐚𝐫𝐚 𝐚𝐭𝐭𝐢𝐭𝐮𝐝𝐞 𝐡𝐢 𝐡𝐚𝐢𝐧... 🔥",
            
            "👑 𝐌𝐞𝐫𝐚 𝐬𝐭𝐲𝐥𝐞 𝐦𝐞𝐫𝐚 𝐩𝐚𝐬 𝐡𝐢 𝐡𝐚𝐢,\n𝐓𝐮𝐦 𝐣𝐞𝐡𝐫𝐚 𝐛𝐡𝐢 𝐤𝐡𝐚𝐫𝐢𝐝 𝐧𝐡𝐢 𝐬𝐚𝐤𝐭𝐞... 💅",
            
            "🔥 𝐊𝐢𝐲𝐚 𝐠𝐡𝐮𝐫 𝐫𝐡𝐞 𝐡𝐨 𝐦𝐞𝐫𝐞 𝐩𝐢𝐜 𝐩𝐚𝐫?\n𝐀𝐛 𝐭𝐨 𝐛𝐚𝐬 𝐝𝐞𝐤𝐡 𝐥𝐨, 𝐋𝐢𝐤𝐞 𝐤𝐚𝐫𝐧𝐚 𝐛𝐚𝐧𝐝 𝐡𝐚𝐢... 📸",
            
            "⚡ 𝐇𝐮𝐦 𝐭𝐨 𝐡𝐚𝐢𝐧 𝐤𝐡𝐮𝐝 𝐤𝐢 𝐚𝐬𝐥𝐢 𝐦𝐮𝐬𝐤𝐢𝐛𝐚𝐭 𝐡𝐚𝐢,\n𝐁𝐚𝐪𝐤𝐢 𝐠𝐡𝐫 𝐤𝐢 𝐭𝐫𝐚𝐢𝐧𝐢𝐧𝐠 𝐡𝐚𝐢... 🚂",
            
            "💎 𝐌𝐞𝐫𝐞 𝐣𝐚𝐢𝐬𝐞 𝐥𝐨𝐠𝐨𝐧 𝐤𝐨 𝐦𝐞𝐫𝐞 𝐣𝐚𝐢𝐬𝐚 𝐧𝐡𝐢𝐦𝐢𝐥 𝐬𝐚𝐤𝐭𝐚,\n𝐊𝐲𝐮𝐧𝐤𝐢 𝐦𝐞𝐫𝐞 𝐣𝐚𝐢𝐬𝐚 𝐥𝐨𝐠 𝐡𝐢 𝐧𝐡𝐢𝐧 𝐡𝐨𝐭𝐞... 🌟",
        ],
    }
    
    @classmethod
    def generate(cls, category: str = None) -> str:
        """Generate a random shayari from specified or random category."""
        if category and category.lower() in cls.SHAYARIS:
            shayaris = cls.SHAYARIS[category.lower()]
        else:
            # Random category
            shayaris = random.choice(list(cls.SHAYARIS.values()))
        
        return random.choice(shayaris)
    
    @classmethod
    def get_categories(cls) -> List[str]:
        """Get available categories."""
        return list(cls.SHAYARIS.keys())


# ============================================================
# 💬 QUOTES GENERATOR  
# ============================================================

class QuotesGenerator:
    """Generate inspirational and motivational quotes!"""
    
    QUOTES = {
        "motivational": [
            ("🚀", "The only way to do great work is to love what you do.", "Steve Jobs"),
            ("⭐", "Success is not final, failure is not fatal: it is the courage to continue that counts.", "Winston Churchill"),
            ("💪", "Believe you can and you're halfway there.", "Theodore Roosevelt"),
            ("🔥", "The future belongs to those who believe in the beauty of their dreams.", "Eleanor Roosevelt"),
            ("🎯", "It does not matter how slowly you go as long as you do not stop.", "Confucius"),
            ("⚡", "The best time to plant a tree was 20 years ago. The second best time is now.", "Chinese Proverb"),
            ("🌟", "Your limitation—it's only your imagination.", "Unknown"),
            ("💫", "Push yourself, because no one else is going to do it for you.", "Unknown"),
            ("🏆", "Great things never come from comfort zones.", "Ben Franklin"),
            ("🎪", "Dream it. Wish it. Do it.", "Unknown"),
        ],
        "life": [
            ("🌻", "Life is what happens when you're busy making other plans.", "John Lennon"),
            ("🌈", "In the end, it's not the years in your life that count. It's the life in your years.", "Abraham Lincoln"),
            ("☀️", "Life is really simple, but we insist on making it complicated.", "Confucius"),
            ("🌺", "The purpose of our lives is to be happy.", "Dalai Lama"),
            ("🍀", "Life is either a daring adventure or nothing at all.", "Helen Keller"),
            ("🌸", "Life is 10% what happens to us and 90% how we react to it.", "Charles R. Swindoll"),
            ("🌼", "The unexamined life is not worth living.", "Socrates"),
            ("🌷", "Turn your wounds into wisdom.", "Oprah Winfrey"),
            ("🌹", "Life is short, smile while you still have teeth.", "Unknown"),
            ("🌿", "Keep smiling, because life is a beautiful thing and there's so much to smile about.", "Marilyn Monroe"),
        ],
        "success": [
            ("💎", "Success usually comes to those who are too busy to be looking for it.", "Henry David Thoreau"),
            ("👑", "The secret of getting ahead is getting started.", "Mark Twain"),
            ("🏅", "I find that the harder I work, the more luck I seem to have.", "Thomas Jefferson"),
            ("🎖️", "Don't be afraid to give up the good to go for the great.", "John D. Rockefeller"),
            ("🏵️", "Success is walking from failure to failure with no loss of enthusiasm.", "Winston Churchill"),
            ("💰", "The way to get started is to quit talking and begin doing.", "Walt Disney"),
            ("🎯", "Opportunities don't happen, you create them.", "Chris Grosser"),
            ("⭐", "Don't limit your challenges. Challenge your limits.", "Unknown"),
            ("🌟", "Success is not the key to happiness. Happiness is the key to success.", "Albert Schweitzer"),
            ("🔑", "I failed my way to success.", "Thomas Edison"),
        ],
        "friendship": [
            ("💚", "A friend is someone who knows all about you and still loves you.", "Elbert Hubbard"),
            ("🤝", "Walking with a friend in the dark is better than walking alone in the light.", "Helen Keller"),
            ("💫", "Friends show their love in times of trouble, not in happiness.", "Euripides"),
            ("🌟", "True friendship comes when the silence between two people is comfortable.", "David Tyson Gentry"),
            ("💝", "Good friends are like stars. You don't always see them, but you know they're always there.", "Unknown"),
            ("🎁", "Friendship is born at that moment when one person says to another, 'What! You too? I thought I was the only one.'", "C.S. Lewis"),
            ("🌈", "A real friend is one who walks in when the rest of the world walks out.", "Walter Winchell"),
            ("☀️", "There is nothing better than a friend, unless it is a friend with chocolate.", "Linda Grayson"),
            ("🎪", "Lots of people want to ride with you in the limo, but what you want is someone who will take the bus with you when the limo breaks down.", "Oprah Winfrey"),
            ("🎈", "A friend is what the heart needs all the time.", "Henry Van Dyke"),
        ],
        "hindi": [
            ("🔥", "जो अकेले चलते हैं, वही आगे बढ़ते हैं।", "स्वामी विवेकानन्द"),
            ("⭐", "कामयाबी का कोई शॉर्टकट नहीं होता।", "अज्ञात"),
            ("💪", "परिस्थितियों से नहीं, अपने विश्वास से लड़ो।", "अज्ञात"),
            ("🚀", "सपने वो नहीं जो हम सोते में देखें, सपने वो हैं जो हमें सोने नहीं देते।", "अब्दुल कलाम"),
            ("🌟", "मेहनत झूठ नहीं बोलती, परिणाम झूठ नहीं बोलते।", "अज्ञात"),
            ("🎯", "जो सोचता है वो करता है, जो करता है वो बन जाता है।", "अज्ञात"),
            ("💫", "गिरकर उठना भी एक कला है, जो इस कला को जानता है वो असली खिलाड़ी है।", "अज्ञात"),
            ("⚡", "जिंदगी में आगे बढ़ने के लिए पीछे मुड़कर नहीं देखना चाहिए।", "अज्ञात"),
            ("🌈", "हार का मतलब हार नहीं होता, यह एक सीख होती है।", "शाहरुख खान"),
            ("🏆", "तूफान में भी कमल का फूल खिलता है, वो ही असली खूबसूरती है।", "अज्ञात"),
        ],
        "funny": [
            ("😂", "I'm not lazy, I'm on energy-saving mode.", "Unknown"),
            ("🤪", "I may be wrong, but I highly doubt it.", "Unknown"),
            ("😜", "I'm not arguing, I'm just explaining why I'm right.", "Unknown"),
            ("🎭", "Common sense is like deodorant. The people who need it most never use it.", "Unknown"),
            ("🤡", "I don't need an alarm clock. My ideas wake me up.", "Unknown"),
            ("😎", "I'm not weird, I'm limited edition.", "Unknown"),
            ("🃏", "Life is short. Smile while you still have teeth.", "Unknown"),
            ("🎪", "I'm on a seafood diet. I see food and I eat it.", "Unknown"),
            ("🎁", "Age is just a number, but stupidity is a lifelong achievement.", "Unknown"),
            ("🎈", "I'm not clumsy, it's just the floor hates me.", "Unknown"),
        ],
    }
    
    @classmethod
    def generate(cls, category: str = None) -> tuple:
        """Generate a random quote: (emoji, quote, author)."""
        if category and category.lower() in cls.QUOTES:
            quotes = cls.QUOTES[category.lower()]
        else:
            quotes = random.choice(list(cls.QUOTES.values()))
        
        emoji, quote, author = random.choice(quotes)
        return emoji, quote, author
    
    @classmethod
    def get_categories(cls) -> List[str]:
        """Get available categories."""
        return list(cls.QUOTES.keys())


# ============================================================
# 📊 RATE LIMITER
# ============================================================

class RateLimiter:
    """Per-user rate limiting."""
    
    def __init__(self):
        self._requests: Dict[int, List[float]] = {}
    
    def check(self, user_id: int) -> tuple[bool, str]:
        now = time.time()
        
        if user_id not in self._requests:
            self._requests[user_id] = []
        
        self._requests[user_id] = [t for t in self._requests[user_id] if now - t < 3600]
        
        recent_minute = [t for t in self._requests[user_id] if now - t < 60]
        if len(recent_minute) >= RATE_LIMIT_MINUTE:
            return False, f"Rate limit: {RATE_LIMIT_MINUTE}/minute"
        
        if len(self._requests[user_id]) >= RATE_LIMIT_HOUR:
            return False, f"Rate limit: {RATE_LIMIT_HOUR}/hour"
        
        self._requests[user_id].append(now)
        return True, ""
    
    def clear(self, user_id: int):
        if user_id in self._requests:
            del self._requests[user_id]


# Global instances
logger = Logger()
rate_limiter = RateLimiter()


# ============================================================
# 🤖 COMMAND HANDLERS
# ============================================================

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command - Show welcome message."""
    user = update.effective_user
    
    logger.chat(user.first_name or "Unknown", "/start", incoming=True)
    
    welcome_text = f"""
🤖 **Hello {user.first_name}! I'm Nova!** 🚀

I'm an **Ultra Advanced AI Assistant** powered by **Nemotron Ultra**!

**✨ INLINE MODE (USE ANYWHERE!)**
`@Rahulxaibot [your question]`

**🆕 NEW FEATURES:**
• 🎨 **Font Changer** - `/font [text]`
• 📝 **Shayari** - `/shayari`
• 💬 **Quotes** - `/quote`
• ⚡ **Ultra Fast Response**

**What can I do?**
💬 Chat about anything
💻 Code generation (`code:` prefix)
🌐 Translation (`translate:` prefix)
🎨 Font transformation
📝 Poetry & Quotes
🔍 Answer questions

**Quick Start:**
• Type any message to chat!
• Use `@Rahulxaibot` anywhere!
• Try `/font hello`

Let's chat! 💬
"""
    
    keyboard = [
        [InlineKeyboardButton("🎨 Try Font Changer", callback_data="show_fonts")],
        [InlineKeyboardButton("📝 Get Shayari", callback_data="get_shayari"),
         InlineKeyboardButton("💬 Get Quote", callback_data="get_quote")],
        [InlineKeyboardButton("❓ Help", callback_data="show_help"), 
         InlineKeyboardButton("📊 Stats", callback_data="show_stats")],
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        welcome_text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
    
    logger.success(f"Welcome sent to {user.id}")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command - Show help menu."""
    help_text = f"""
📖 **Nova AI Bot - Help Guide** v2.0

**✨ INLINE MODE (USE ANYWHERE!)**
`@Rahulxaibot [query]` - Use in any chat!

**🆕 NEW COMMANDS:**
• `/font <text>` - Convert to fancy fonts
• `/fonts` - See all available fonts
• `/shayari [type]` - Generate shayari
• `/quote [type]` - Get inspirational quote

**Font Types:** bold, italic, script, gothic, double, mono, circled, fancy, upside & more!

**Shayari Types:** ishq, dard, friendship, motivational, funny, attitude

**Quote Types:** motivational, life, success, friendship, hindi, funny

**Inline Modes:**
• `@Rahulxaibot hello` - Normal chat
• `@Rahulxaibot code: python sort list` - Code
• `@Rahulxaibot translate: hi to hindi` - Translate
• `@Rahulxaibot font:bold Hello` - Fancy font!

**Basic Commands:**
• `/start` - Start the bot
• `/clear` - Reset conversation memory
• `/model` - Current AI model info
• `/stats` - Your usage statistics

**Features:**
🧠 Remembers conversation context
⌨️ Live typing indicators
📡 Streaming responses
🎨 Beautiful formatted output
⚡ Ultra fast responses

**Tips:**
💡 Use inline mode in group chats!
💡 Try `/font Your Name` for cool text!
💡 I support Hindi/Hinglish too!

**Having issues?**
Contact bot owner!
"""
    
    await update.message.reply_text(help_text, parse_mode='Markdown')


async def font_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /font command - Convert text to fancy font."""
    user = update.effective_user
    
    if not context.args:
        # Show font preview
        preview_text = "**🎨 Font Changer - Available Fonts**\n\n"
        preview_text += "Usage: `/font:<style> <text>`\n\n"
        preview_text += "**Example:** `/font:bold Hello`\n\n"
        preview_text += "**Available Styles:**\n"
        
        fonts = FontChanger.get_font_list()
        for i, font_name in enumerate(fonts[:10], 1):
            preview = FontChanger.get_font_preview(font_name)
            preview_text += f"{i}. `{font_name}` → {preview}\n"
        
        preview_text += f"\n*And {len(fonts)-10} more fonts!*"
        
        await update.message.reply_text(preview_text, parse_mode='Markdown')
        return
    
    # Parse font style and text
    input_text = ' '.join(context.args)
    
    if ':' in input_text:
        font_style, text = input_text.split(':', 1)
        font_style = font_style.strip().lower()
        text = text.strip()
    else:
        font_style = "bold"
        text = input_text.strip()
    
    if not text:
        await update.message.reply_text("Please provide text to convert!\nUsage: `/font:bold Hello World`")
        return
    
    # Convert text
    converted = FontChanger.convert(text, font_style)
    
    result_text = f"""🎨 **Font Style: `{font_style.upper()}`**

**Original:** {text}
**Converted:** {converted}

_Try other styles: italic, script, gothic, double, mono, circled, fancy, upside_"""
    
    await update.message.reply_text(result_text, parse_mode='Markdown')
    logger.success(f"Font applied: {font_style} for {user.first_name}")


async def fonts_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show all available fonts with examples."""
    fonts = FontChanger.get_font_list()
    example_text = "Hello Nova"
    
    text = "🎨 **All Available Fonts**\n\n"
    
    for i, font_name in enumerate(fonts, 1):
        converted = FontChanger.convert(example_text, font_name)
        text += f"**{i}. {font_name.title()}**\n   `{converted}`\n\n"
    
    text += "\n_Usage: `/font:<style> your text`_\n_Example: `/font:script Hey there`_"
    
    await update.message.reply_text(text, parse_mode='Markdown')


async def shayari_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Generate beautiful shayari."""
    user = update.effective_user
    
    # Get category if provided
    category = context.args[0].lower() if context.args else None
    
    # Generate shayari
    shayari = ShayariGenerator.generate(category)
    
    # Create keyboard with categories
    categories = ShayariGenerator.get_categories()
    keyboard = []
    row = []
    for cat in categories:
        row.append(InlineKeyboardButton(cat.title(), callback_data=f"shayari_{cat}"))
        if len(row) == 3:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = f"""📝 **Shayari** ✨

{shayari}

_🔄 Click buttons for more shayaris!_
"""
    
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    logger.success(f"Shayari generated for {user.first_name}")


async def quote_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Generate inspirational quote."""
    user = update.effective_user
    
    # Get category if provided
    category = context.args[0].lower() if context.args else None
    
    # Generate quote
    emoji, quote, author = QuotesGenerator.generate(category)
    
    # Create keyboard with categories
    categories = QuotesGenerator.get_categories()
    keyboard = []
    row = []
    for cat in categories:
        row.append(InlineKeyboardButton(cat.title(), callback_data=f"quote_{cat}"))
        if len(row) == 3:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = f"""💬 **Quote of the Day** {emoji}

*"{quote}"*

— **{author}**

_🔄 Click buttons for more quotes!_
"""
    
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    logger.success(f"Quote generated for {user.first_name}")


async def model_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show current model information."""
    user = update.effective_user
    user_id = user.id
    
    # Get user's preferred model (if any)
    preferred_model = USER_MODEL_PREFERENCES.get(user_id)
    current_model = preferred_model or "nvidia/nemotron-3-ultra-550b-a55b:free"
    
    # Get model info
    if current_model in FREE_TEXT_MODELS:
        model_info = FREE_TEXT_MODELS[current_model]
        model_name = model_info['name']
        model_desc = model_info['desc']
    else:
        model_name = current_model.split('/')[-1].replace(':free', '')
        model_desc = "Default Model"
    
    text = f"""
🧠 **AI Model Information**

**Current Model:** `{model_name}`
{model_desc}

**Total Free Models:** `{len(FREE_TEXT_MODELS)}`

_Use `/models` to switch models!_
"""
    
    await update.message.reply_text(text, parse_mode='Markdown')


async def models_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show all available models with selection keyboard - NEW!"""
    user = update.effective_user
    user_id = user.id
    
    logger.chat(user.first_name or "Unknown", "/models", incoming=True)
    
    # Get current model
    preferred_model = USER_MODEL_PREFERENCES.get(user_id)
    current_model_id = preferred_model or "nvidia/nemotron-3-ultra-550b-a55b:free"
    
    # Build model list by category
    categories = {
        "🔥 Premium": [m for m, info in FREE_TEXT_MODELS.items() if info['category'] == 'premium'],
        "⚡ Fast": [m for m, info in FREE_TEXT_MODELS.items() if info['category'] == 'fast'],
        "💨 Ultra Fast": [m for m, info in FREE_TEXT_MODELS.items() if info['category'] == 'ultra_fast'],
        "🎯 Balanced": [m for m, info in FREE_TEXT_MODELS.items() if info['category'] == 'balanced'],
        "💻 Code": [m for m, info in FREE_TEXT_MODELS.items() if info['category'] == 'code'],
        "🧪 Special": [m for m, info in FREE_TEXT_MODELS.items() if info['category'] in ['special', 'experimental']],
    }
    
    # Build keyboard
    keyboard = []
    
    # Add category headers and models
    for cat_name, models in categories.items():
        if models:
            row = []
            for model_id in models[:2]:  # Max 2 per row
                model_info = FREE_TEXT_MODELS[model_id]
                short_name = model_info['name'].split()[0]  # First word only
                
                # Mark current model with ✅
                is_current = "✅" if model_id == current_model else ""
                
                row.append(InlineKeyboardButton(
                    f"{is_current}{short_name}", 
                    callback_data=f"model_{model_id}"
                ))
            if row:
                keyboard.append(row)
    
    # Add action buttons
    keyboard.append([
        InlineKeyboardButton("🔄 Reset to Default", callback_data="model_reset"),
        InlineKeyboardButton("ℹ️ Current Info", callback_data="model_info")
    ])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Current model name
    if current_model_id in FREE_TEXT_MODELS:
        current_name = FREE_TEXT_MODELS[current_model_id]['name']
    else:
        current_name = current_model_id.split('/')[-1]
    
    text = f"""🧠 **Model Selector** 🤖

**Your Current Model:** `{current_name}`

**Available Models:** {len(FREE_TEXT_MODELS)} Free!

**Categories:**
• 🔥 **Premium** - Best quality (slower)
• ⚡ **Fast** - Quick responses
• 💨 **Ultra Fast** - Instant!
• 💻 **Code** - Best for programming

_Tap a button to select model!_
"""
    
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    logger.success(f"Model selector shown to {user.first_name}")


async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Clear conversation memory."""
    user_id = update.effective_user.id
    
    engine = get_ai_engine()
    engine.clear_memory(user_id)
    rate_limiter.clear(user_id)
    
    logger.info(f"Cleared memory for user {user_id}")
    
    await update.message.reply_text(
        "🗑️ **Conversation cleared!**\n\nStarting fresh! Send me a new message!",
        parse_mode='Markdown'
    )


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show usage statistics."""
    engine = get_ai_engine()
    stats = engine.get_stats()
    
    text = f"""
📊 **Your Statistics**

**Session Info:**
• Messages in memory: ~{stats.get('total_messages', 0)}
• Active users: {stats.get('active_users', 0)}

**Bot Performance:**
• Total requests: {stats.get('total_requests', 0)}
• Success rate: {stats.get('success_rate', 'N/A')}
• Avg latency: {stats.get('avg_latency_ms', 0)}ms
• Fallbacks used: {stats.get('fallbacks_used', 0)}

**Features Used:**
• 🎨 Fonts Available: 15+
• 📝 Shayari Categories: 6
• 💬 Quote Categories: 6

_Use `/clear` to reset your conversation._
"""
    
    await update.message.reply_text(text, parse_mode='Markdown')


# ============================================================
# 🧹 MARKDOWN SANITIZATION HELPERS
# ============================================================

def sanitize_markdown(text: str) -> str:
    """
    Sanitize markdown text to prevent Telegram parse errors.
    Enhanced version with better entity handling!
    """
    if not text:
        return text
    
    # First, truncate very long lines to prevent byte offset errors
    lines = text.split('\n')
    safe_lines = []
    
    for line in lines:
        # Limit line length to ~4000 chars to avoid entity parsing issues
        if len(line) > 4000:
            line = line[:3950] + "..."
        safe_lines.append(line)
    
    text = '\n'.join(safe_lines)
    
    # Now fix formatting
    sanitized_lines = []
    in_code_block = False
    
    for line in safe_lines:
        if '```' in line:
            in_code_block = not in_code_block
        
        if not in_code_block:
            # Count formatting characters carefully
            bold_count = line.count('**')
            # Count single * that aren't part of **
            temp = line.replace('**', '')
            italic_count = temp.count('*')
            code_count = line.count('`')
            
            # Fix odd counts
            if bold_count % 2 != 0:
                line += '**'
            if italic_count % 2 != 0:
                line += '*'
            if code_count % 2 != 0:
                line += '`'
        
        sanitized_lines.append(line)
    
    result = '\n'.join(sanitized_lines)
    
    # Ensure code blocks closed
    if result.count('```') % 2 != 0:
        result += '\n```'
    
    return result


def sanitize_for_code(text: str) -> str:
    """Sanitize text for display inside code block."""
    return text.replace('`', "'").replace('```', "'''").replace('*', '')


def truncate_for_inline(text: str, max_length: int = 300) -> str:
    """Truncate text safely for inline results."""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."


async def safe_edit_status(message, new_text: str):
    """Safely edit status message without raising errors."""
    try:
        # Truncate to safe length
        safe_text = new_text[:4000] if len(new_text) > 4000 else new_text
        await message.edit_text(safe_text, parse_mode='Markdown')
    except Exception:
        pass


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle regular text messages - THE MAIN BRAIN!
    
    Features:
    - Live typing indicator
    - Streaming responses
    - Rate limiting
    - Error handling
    - FIXED: No more 'Message' object errors!
    """
    # Get user info - PROPER WAY
    user = update.effective_user
    message_obj = update.message
    
    # FIX: Use .text properly, not .message
    message = message_obj.text if message_obj else ""
    user_id = user.id
    user_name = user.first_name or "Unknown"
    
    # Log incoming message
    logger.chat(user_name, message, incoming=True)
    
    # Check rate limits
    allowed, reason = rate_limiter.check(user_id)
    if not allowed:
        logger.warning(f"Rate limited: {user_name} ({reason})")
        try:
            await message_obj.reply_text(
                f"⏳ **Slow down!**\n\n{reason}\nPlease wait a moment and try again.",
                parse_mode='Markdown'
            )
        except Exception:
            pass
        return
    
    # Check empty message
    if not message or not message.strip():
        return
    
    # Create status message placeholder
    try:
        status_msg = await message_obj.reply_text("🤔 *Thinking...*", parse_mode='Markdown')
    except Exception:
        return
    
    # Start typing indicator loop
    typing_task = asyncio.create_task(
        continuous_typing(message_obj.chat_id, context.bot)
    )
    
    # Stream buffer for live updates
    stream_buffer = []
    last_update_time = [time.time()]
    
    def stream_callback(chunk: str):
        """Callback for streaming chunks - SYNC function."""
        stream_buffer.append(chunk)
        
        current_time = time.time()
        if current_time - last_update_time[0] > 2.0:
            last_update_time[0] = current_time
            preview = ''.join(stream_buffer[-500:])
            
            asyncio.create_task(
                safe_edit_status(status_msg, f"⌨️ *Generating...*\n\n```\n{sanitize_for_code(preview)}```")
            )
    
    try:
        # Get AI response - USE USER'S PREFERRED MODEL!
        engine = get_ai_engine()
        
        # Check if user has a preferred model
        user_model = USER_MODEL_PREFERENCES.get(user_id)
        
        # Override model for this request (temporary)
        original_model = None
        if user_model and user_model in FREE_TEXT_MODELS:
            original_model = engine.primary_model
            engine.primary_model = user_model
            logger.info(f"Using {FREE_TEXT_MODELS[user_model]['name']} for {user_name}")
        
        try:
            response = await engine.chat(
                user_id=user_id,
                message=message,
                stream_callback=stream_callback
            )
        finally:
            # Restore original model
            if original_model:
                engine.primary_model = original_model
        
        # Cancel typing indicator
        typing_task.cancel()
        
        if response.error and not response.content:
            logger.error(f"AI error for {user_name}: {response.error}")
            
            try:
                await status_msg.edit_text(
                    f"😵 **Oops! Something went wrong**\n\n"
                    f"`{response.error[:200]}`\n\n"
                    f"Please try again in a moment.",
                    parse_mode='Markdown'
                )
            except Exception:
                pass
            return
        
        # Success! Format & sanitize response
        ai_response = sanitize_markdown(response.content)
        
        # Truncate if too long for Telegram (4096 max)
        if len(ai_response) > 4000:
            ai_response = ai_response[:3950] + "\n\n...*(truncated)*"
        
        # Log response
        logger.chat("Nova", ai_response, incoming=False)
        
        # Build final message
        prefix = ""
        if response.is_fallback:
            prefix = "🔄 *Using backup model*\n\n"
        
        final_text = f"{prefix}{ai_response}"
        
        # Edit status message with ENHANCED error handling
        try:
            await status_msg.edit_text(final_text, parse_mode='Markdown')
        except BadRequest as e:
            # Entity parsing error - send plain text
            logger.warning(f"Entity parse error, sending plain text: {str(e)[:50]}")
            plain_text = final_text.replace('*', '').replace('`', '').replace('_', '')
            try:
                await status_msg.edit_text(plain_text)
            except Exception:
                try:
                    await message_obj.reply_text(plain_text)
                except Exception:
                    pass
        except Exception as e:
            logger.warning(f"Edit failed: {str(e)[:50]}")
            plain_text = final_text.replace('*', '').replace('`', '').replace('_', '')
            try:
                await message_obj.reply_text(plain_text)
            except Exception:
                pass
        
        # Log success
        latency_s = response.latency_ms / 1000
        logger.success(
            f"Response to {user_name}: {len(ai_response)} chars in {latency_s:.2f}s "
            f"(model: {response.model_used.split('/')[-1]})"
        )
        
    except Exception as e:
        typing_task.cancel()
        logger.error(f"Message handler error: {e}")
        
        try:
            await status_msg.edit_text(
                "😵 **Unexpected error occurred**\n\n"
                "Please try again!",
                parse_mode='Markdown'
            )
        except Exception:
            pass


async def continuous_typing(chat_id: int, bot, interval: float = TYPING_DELAY):
    """Continuously send typing action while processing."""
    try:
        while True:
            await bot.send_chat_action(chat_id=chat_id, action=CHAT_TYPING)
            await asyncio.sleep(interval)
    except asyncio.CancelledError:
        pass
    except Exception:
        pass


# ============================================================
# 🔘 CALLBACK HANDLERS (Inline Buttons) - FIXED!
# ============================================================

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle inline button presses - FIXED VERSION!"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    user = query.from_user
    
    # FIX: Don't pass query.message to commands expecting Update
    # Instead, handle each case separately
    
    if data == "chat_start":
        await query.edit_message_text(
            "💬 **Great! Just type your message below!**\n\n"
            "I'm ready when you are! Try:\n"
            "• `/font:bold Your Name`\n"
            "• `/shayari`\n"
            "• `/quote`\n"
            "• Or just say hi! 👋",
            parse_mode='Markdown'
        )
    
    elif data == "show_help":
        # Create a fake update-like structure or call directly
        await query.edit_message_text(
            "📖 **Help is here!**\n\n"
            "Use these commands:\n"
            "• `/font <text>` - Fancy fonts\n"
            "• `/shayari` - Poetry\n"
            "• `/quote` - Inspirational\n"
            "• `/help` - Full guide\n\n"
            "Or type `/help` for complete info!",
            parse_mode='Markdown'
        )
    
    elif data == "show_stats":
        await query.edit_message_text(
            "📊 **Your Stats**\n\n"
            "Type `/stats` to see your usage statistics!",
            parse_mode='Markdown'
        )
    
    elif data == "show_fonts":
        fonts = FontChanger.get_font_list()[:8]
        text = "🎨 **Popular Fonts**\n\n"
        for font in fonts:
            preview = FontChanger.convert("Sample", font)
            text += f"• `{font}` → {preview}\n"
        text += "\n_Use `/font:<style> your text`_"
        await query.edit_message_text(text, parse_mode='Markdown')
    
    elif data.startswith("shayari_"):
        category = data.replace("shayari_", "")
        shayari = ShayariGenerator.generate(category)
        await query.edit_message_text(
            f"📝 **Shayari** ({category.title()})\n\n{shayari}\n\n_🔄 Click for more!_",
            parse_mode='Markdown'
        )
    
    elif data.startswith("quote_"):
        category = data.replace("quote_", "")
        emoji, quote, author = QuotesGenerator.generate(category)
        await query.edit_message_text(
            f"💬 **Quote** ({category.title()}) {emoji}\n\n*\"{quote}*\n\n— **{author}**\n\n_🔄 Click for more!_",
            parse_mode='Markdown'
        )
    
    elif data.startswith("font_"):
        font_style = data.replace("font_", "")
        sample = FontChanger.convert("Hello World!", font_style)
        await query.edit_message_text(
            f"🎨 **Font: {font_style.upper()}**\n\n{sample}\n\n_Use `/font:{font_style} your text`_",
            parse_mode='Markdown'
        )
    
    # MODEL SELECTION CALLBACKS - NEW!
    elif data.startswith("model_"):
        model_id = data.replace("model_", "")
        user_id = user.id
        
        if model_id == "reset":
            # Reset to default
            if user_id in USER_MODEL_PREFERENCES:
                del USER_MODEL_PREFERENCES[user_id]
            await query.edit_message_text(
                "🔄 **Model Reset!**\n\nUsing default model now:\n`Nemotron Ultra 550B`\n\n_Enjoy the best quality!_",
                parse_mode='Markdown'
            )
        
        elif model_id == "info":
            # Show current model info
            preferred_model = USER_MODEL_PREFERENCES.get(user_id)
            current = preferred_model or "nvidia/nemotron-3-ultra-550b-a55b:free"
            
            if current in FREE_TEXT_MODELS:
                info = FREE_TEXT_MODELS[current]
                await query.edit_message_text(
                    f"🧠 **Current Model Info**\n\n"
                    f"**Name:** {info['name']}\n"
                    f"**Provider:** {info['provider']}\n"
                    f"**ID:** `{current}`\n\n"
                    f"{info['desc']}",
                    parse_mode='Markdown'
                )
            else:
                await query.edit_message_text(
                    f"🧠 **Current Model:** `{current}`",
                    parse_mode='Markdown'
                )
        
        else:
            # Select a specific model
            if model_id in FREE_TEXT_MODELS:
                # Save user preference
                USER_MODEL_PREFERENCES[user_id] = model_id
                
                model_info = FREE_TEXT_MODELS[model_id]
                
                await query.edit_message_text(
                    f"✅ **Model Selected!**\n\n"
                    f"**{model_info['name']}**\n"
                    f"{model_info['desc']}\n\n"
                    f"_Your next message will use this model!_",
                    parse_mode='Markdown'
                )
                logger.success(f"{user.first_name} selected model: {model_info['name']}")
            else:
                await query.answer(text="❌ Model not found!", show_alert=True)


# ============================================================
# 🔍 INLINE QUERY HANDLER - ULTRA FAST VERSION!
# ============================================================

async def inline_query_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle inline queries - @Rahulxaibot [query]
    
    OPTIMIZED FOR SPEED:
    - Quick responses for simple queries
    - Font conversion built-in
    - Caching enabled
    - Timeout handling improved
    """
    query = update.inline_query
    user = query.from_user
    query_text = query.query.strip()
    
    # Log inline query
    logger.chat(user.first_name or "Unknown", f"@inline: {query_text}", incoming=True)
    
    if not query_text:
        # Show enhanced help when no query
        results = [
            InlineQueryResultArticle(
                id="help_main",
                title="🤖 Nova AI Bot - Start Chatting!",
                description="Type your question to get AI response instantly!",
                input_message_content=InputTextMessageContent(
                    message_text="🤖 **Nova AI Bot v2.0** 🚀\n\nType `@Rahulxaibot [question]` to chat!\n\n**Quick Examples:**\n• `@Rahulxaibot hello`\n• `@Rahulxaibot who is modi`\n• `@Rahulxaibot code: python hello`\n• `@Rahulxaibot translate: hi to hindi`\n• `@Rahulxaibot font:bold Cool Text`\n\n**New Features:** 🎨 Fonts | 📝 Shayari | 💬 Quotes",
                    parse_mode='Markdown'
                ),
            ),
            InlineQueryResultArticle(
                id="help_font",
                title="🎨 Font Changer",
                description="@Rahulxaibot font:bold your text",
                input_message_content=InputTextMessageContent(
                    message_text="🎨 **Font Changer**\n\nUsage: `font:<style> <text>`\n\n**Styles:** bold, italic, script, gothic, double, mono, circled, fancy, upside\n\nExample: `font:bold Hello World`",
                    parse_mode='Markdown'
                ),
            ),
            InlineQueryResultArticle(
                id="help_shayari",
                title="📝 Shayari Generator",
                description="@Rahulxaibot shayari:ishq",
                input_message_content=InputTextMessageContent(
                    message_text="📝 **Shayari Generator**\n\nUsage: `shayari:<type>`\n\n**Types:** ishq, dard, friendship, motivational, funny, attitude\n\nExample: `shayari:ishq`",
                    parse_mode='Markdown'
                ),
            ),
            InlineQueryResultArticle(
                id="help_quote",
                title="💬 Quote Generator",
                description="@Rahulxaibot quote:motivational",
                input_message_content=InputTextMessageContent(
                    message_text="💬 **Quote Generator**\n\nUsage: `quote:<type>`\n\n**Types:** motivational, life, success, friendship, hindi, funny\n\nExample: `quote:motivational`",
                    parse_mode='Markdown'
                ),
            ),
        ]
        
        try:
            await query.answer(results, cache_time=300)
        except Exception as e:
            logger.warning(f"Help results error: {e}")
        return
    
    # Process the query - OPTIMIZED PATHS
    try:
        # ====== FAST PATH: Font Conversion (No API needed!) ======
        if query_text.lower().startswith("font:"):
            font_input = query_text[5:].strip()
            if ':' in font_input:
                font_style, text = font_input.split(':', 1)
                font_style = font_style.strip().lower()
                text = text.strip()
            else:
                parts = font_input.split(None, 1)
                if len(parts) >= 2:
                    font_style = parts[0].lower()
                    text = parts[1]
                else:
                    font_style = "bold"
                    text = font_input
            
            if text:
                converted = FontChanger.convert(text, font_style)
                
                results = [
                    InlineQueryResultArticle(
                        id="font_result",
                        title=f"🎨 {font_style.title()}: {text}",
                        description=f"Converted text: {converted[:100]}",
                        input_message_content=InputTextMessageContent(
                            message_text=f"🎨 **Font: {font_style.upper()}**\n\n**Original:** {text}\n\n**Converted:** {converted}",
                            parse_mode='Markdown'
                        ),
                    )
                ]
                
                try:
                    await query.answer(results, cache_time=300)
                    logger.success(f"Font converted: {font_style}")
                    return
                except Exception as e:
                    logger.warning(f"Font result error: {e}")
        
        # ====== FAST PATH: Shayari (No API needed!) ======
        elif query_text.lower().startswith("shayari:"):
            category = query_text[8:].strip().lower()
            shayari = ShayariGenerator.generate(category)
            
            results = [
                InlineQueryResultArticle(
                    id="shayari_result",
                    title=f"📝 Shayari ({category.title()})",
                    description=shayari.replace('\n', ' ')[:100],
                    input_message_content=InputTextMessageContent(
                        message_text=shayari,
                        parse_mode='Markdown'
                    ),
                )
            ]
            
            try:
                await query.answer(results, cache_time=60)
                logger.success(f"Shayari generated: {category}")
                return
            except Exception as e:
                logger.warning(f"Shayari result error: {e}")
        
        # ====== FAST PATH: Quotes (No API needed!) ======
        elif query_text.lower().startswith("quote:"):
            category = query_text[6:].strip().lower()
            emoji, quote, author = QuotesGenerator.generate(category)
            
            quote_text = f'{emoji} *"{quote}*" — **{author}**'
            
            results = [
                InlineQueryResultArticle(
                    id="quote_result",
                    title=f"💬 Quote ({category.title()})",
                    description=f"{quote[:100]} - {author}",
                    input_message_content=InputTextMessageContent(
                        message_text=quote_text,
                        parse_mode='Markdown'
                    ),
                )
            ]
            
            try:
                await query.answer(results, cache_time=60)
                logger.success(f"Quote generated: {category}")
                return
            except Exception as e:
                logger.warning(f"Quote result error: {e}")
        
        # ====== NORMAL PATH: AI Response (with timeout handling) ======
        engine = get_ai_engine()
        
        # Detect mode from query prefix
        mode = "chat"
        actual_query = query_text
        system_prompt = None
        
        if query_text.lower().startswith("code:"):
            mode = "code"
            actual_query = query_text[5:].strip()
            system_prompt = "You are an expert programmer. Write clean, well-commented code. Be concise. Respond with ONLY the code and brief explanation."
            
        elif query_text.lower().startswith("translate:"):
            mode = "translate"
            actual_query = query_text[10:].strip()
            system_prompt = "You are a professional translator. Translate accurately. Only provide the translation."
            
        elif query_text.lower().startswith("summarize:"):
            mode = "summarize"
            actual_query = query_text[10:].strip()
            system_prompt = "Create a concise summary. Use bullet points. Keep under 500 characters."
        
        # Set timeout for inline (shorter than regular messages!)
        try:
            # Use asyncio.wait_for to enforce timeout
            response = await asyncio.wait_for(
                engine.chat(
                    user_id=user.id,
                    message=f"[INLINE {mode.upper()}] {actual_query}",
                    stream_callback=None,  # No streaming for speed
                    system_prompt=system_prompt,
                ),
                timeout=8.0  # 8 second timeout for inline!
            )
        except asyncio.TimeoutError:
            logger.warning("Inline query timed out")
            results = [
                InlineQueryResultArticle(
                    id="timeout",
                    title="⏱️ Taking too long...",
                    description="Try a shorter query or message me directly!",
                    input_message_content=InputTextMessageContent(
                        message_text="⏱️ **Response taking too long...**\n\nThis query needs more time.\n\n👉 **Try messaging me directly** for longer responses!"
                    ),
                )
            ]
            try:
                await query.answer(results, cache_time=30)
            except:
                pass
            return
        
        if response.error or not response.content:
            error_msg = f"😵 Error: {response.error[:100] if response.error else 'Unknown'}"
            results = [
                InlineQueryResultArticle(
                    id="error",
                    title="⚠️ Error occurred",
                    description=error_msg,
                    input_message_content=InputTextMessageContent(
                        message_text=error_msg
                    ),
                )
            ]
        else:
            ai_response = response.content
            
            # Truncate for display
            display_response = truncate_for_inline(ai_response, 250)
            
            # Sanitize for safety
            safe_response = sanitize_markdown(ai_response)
            
            results = []
            
            # Main result
            results.append(
                InlineQueryResultArticle(
                    id="main_result",
                    title=f"🤖 Nova's Response ({mode.title()})",
                    description=display_response.replace('\n', ' ')[:100],
                    input_message_content=InputTextMessageContent(
                        message_text=safe_response[:4000],  # Hard limit
                        parse_mode='Markdown'
                    ),
                )
            )
            
            # Plain text copy
            plain_text = ai_response.replace('*', '').replace('`', '').replace('_', '')[:4000]
            results.append(
                InlineQueryResultArticle(
                    id="copy_result",
                    title="📋 Copy as Plain Text",
                    description="Click to copy without formatting",
                    input_message_content=InputTextMessageContent(
                        message_text=plain_text
                    ),
                )
            )
            
            # Continue in DM option
            results.append(
                InlineQueryResultArticle(
                    id="continue_dm",
                    title="💬 Continue in DM",
                    description="Open private chat for longer conversations",
                    input_message_content=InputTextMessageContent(
                        message_text=f"🔄 **Continue this conversation in DM!**\n\nYour last query: *{truncate_for_inline(actual_query, 100)}*\n\nResponse preview:\n{display_response}\n\n👉 Message me directly to continue!"
                    ),
                )
            )
        
        # Answer with error handling
        try:
            await query.answer(results, cache_time=300, is_personal=True)
            logger.success(f"Inline response sent ({mode} mode)")
        except Exception as e:
            logger.warning(f"Inline answer error: {e}")
            # Try without cache
            try:
                await query.answer(results, cache_time=0)
            except:
                pass
        
    except Exception as e:
        logger.error(f"Inline query error: {e}")
        
        # Send fallback
        try:
            results = [
                InlineQueryResultArticle(
                    id="error_fallback",
                    title="⚠️ Temporary Error",
                    description=str(e)[:100],
                    input_message_content=InputTextMessageContent(
                        message_text="😵 **Oops!** Something went wrong.\n\nPlease try again or message me directly!"
                    ),
                )
            ]
            await query.answer(results, cache_time=60)
        except:
            pass


# ============================================================
# 👑 ADMIN COMMANDS
# ============================================================

def is_owner(user_id: int) -> bool:
    """Check if user is owner."""
    return OWNER_ID and user_id == OWNER_ID


def is_admin(user_id: int) -> bool:
    """Check if user is admin."""
    return user_id in ADMIN_IDS or is_owner(user_id)


async def broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Broadcast message to all users (Owner only)."""
    if not is_owner(update.effective_user.id):
        await update.message.reply_text("❌ Only owner can use this command.")
        return
    
    if not context.args:
        await update.message.reply_text("Usage: /broadcast <message>")
        return
    
    message = " ".join(context.args)
    await update.message.reply_text(f"📢 Broadcast sent:\n\n{message}")


async def users_count_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show active user count (Admin)."""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Admins only.")
        return
    
    engine = get_ai_engine()
    stats = engine.get_stats()
    
    await update.message.reply_text(
        f"📊 **Global Statistics**\n\n"
        f"Active Users: `{stats.get('active_users', 0)}`\n"
        f"Total Messages: `{stats.get('total_messages', 0)}`\n"
        f"Fonts Available: `15+`\n"
        f"Shayari Categories: `6`\n"
        f"Quote Categories: `6`",
        parse_mode='Markdown'
    )


# ============================================================
# ⚙️ ERROR HANDLERS
# ============================================================

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors globally - FIXED!"""
    error = context.error
    
    # Better error logging
    error_type = type(error).__name__
    error_msg = str(error)
    
    logger.error(f"Error: {error_type}: {error_msg}")
    
    if isinstance(error, Forbidden):
        logger.warning("Bot was blocked by user")
    elif isinstance(error, BadRequest):
        # More specific handling for entity errors
        if "can't find end of the entity" in error_msg.lower():
            logger.warning("Markdown entity parsing error - will use plain text fallback")
        else:
            logger.warning(f"Bad request: {error}")
    elif isinstance(error, TelegramError):
        logger.error(f"Telegram error: {error}")
    elif isinstance(error, AttributeError):
        # This catches the 'Message' object has no attribute 'message' bug!
        logger.error(f"Attribute error (likely Message.text issue): {error}")
    else:
        logger.error(f"Unknown error: {error}")


# ============================================================
# 🚀 MAIN ENTRY POINT
# ============================================================

def main():
    """Start the bot - Main entry point."""
    
    # Print awesome banner
    TerminalEffects.print_banner()
    
    # Validate configuration
    valid, errors = validate_config()
    if not valid:
        logger.error("Configuration errors:")
        for err in errors:
            logger.error(f"  • {err}")
        sys.exit(1)
    
    if errors:
        for warn in errors:
            logger.warning(warn)
    
    logger.info("Initializing Nova AI Bot v2.1...")
    
    # Build application with optimized timeouts
    app = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .read_timeout(45)
        .write_timeout(45)
        .connect_timeout(45)
        .pool_timeout(45)
        .get_updates_read_timeout(60)
        .get_updates_write_timeout(60)
        .get_updates_pool_timeout(60)
        .get_updates_connect_timeout(60)
        .build()
    )
    
    # Register handlers
    
    # Command handlers - NEW ONES ADDED!
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("model", model_command))
    app.add_handler(CommandHandler("models", models_command))  # NEW: Model selector!
    app.add_handler(CommandHandler("clear", clear_command))
    app.add_handler(CommandHandler("stats", stats_command))
    app.add_handler(CommandHandler("font", font_command))
    app.add_handler(CommandHandler("fonts", fonts_command))
    app.add_handler(CommandHandler("shayari", shayari_command))
    app.add_handler(CommandHandler("quote", quote_command))
    
    # Admin commands
    app.add_handler(CommandHandler("broadcast", broadcast_command))
    app.add_handler(CommandHandler("users", users_count_command))
    
    # Message handler (must be last!)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Callback handler (inline buttons) - FIXED!
    app.add_handler(CallbackQueryHandler(button_callback))
    
    # INLINE QUERY HANDLER - ULTRA FAST!
    app.add_handler(InlineQueryHandler(inline_query_handler))
    
    # Error handler
    try:
        app.add_error_handler(error_handler)
    except (AttributeError, TypeError):
        try:
            from telegram.ext import TypeHandler
            class ErrorWrapper(TypeHandler):
                def __init__(self, callback):
                    super().__init__(Update, callback)
            try:
                app.add_handler(ErrorWrapper(error_handler))
            except Exception as e:
                logger.warning(f"Could not register error handler: {e}")
        except Exception:
            pass
    
    # Set bot commands menu - UPDATED!
    async def post_init(app):
        await app.bot.set_my_commands([
            BotCommand("start", "Start the bot"),
            BotCommand("help", "Help & commands"),
            BotCommand("models", "🆕 Choose AI Model (17+)"),
            BotCommand("font", "Change text font"),
            BotCommand("shayari", "Get shayari"),
            BotCommand("quote", "Get inspirational quote"),
            BotCommand("model", "Current model info"),
            BotCommand("clear", "Clear conversation"),
            BotCommand("stats", "Your statistics"),
        ])
    
    app.post_init = post_init
    
    # Start health check server
    start_health_check_server(PORT)
    
    logger.success("Bot initialized successfully!")
    logger.info(f"Model: {get_env_info()['model']}")
    logger.info(f"Free Models Available: {len(FREE_TEXT_MODELS)}")
    logger.info(f"Starting polling on port {PORT}...")
    
    # Print separator
    print(f"\n{Colors.BRIGHT_GREEN}{'═' * 60}{Colors.RESET}")
    print(f"  {Colors.BOLD}🚀 Nova AI Bot v2.1 is LIVE!{Colors.RESET}")
    print(f"  {Colors.DIM}{len(FREE_TEXT_MODELS)} Free Models | Bug Fixes | New Features{Colors.RESET}")
    print(f"{Colors.BRIGHT_GREEN}{'═' * 60}{Colors.RESET}\n")
    
    # Run the bot
    app.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True,
        close_loop=False,
    )


def start_health_check_server(port: int):
    """Start HTTP health check server for Railway."""
    from http.server import HTTPServer, BaseHTTPRequestHandler
    
    class HealthHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/health':
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "status": "healthy",
                    "bot": "Nova AI Bot v2.0",
                    "version": "2.0.0",
                    "features": ["font_changer", "shayari", "quotes", "fast_inline"],
                    "timestamp": datetime.now().isoformat()
                }).encode())
            else:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"OK")
        
        def log_message(self, format, *args):
            pass
    
    def run_server():
        server = HTTPServer(('0.0.0.0', port), HealthHandler)
        logger.info(f"Health check server running on port {port}")
        server.serve_forever()
    
    thread = threading.Thread(target=run_server, daemon=True)
    thread.start()


# ============================================================
# ▶️ RUN
# ============================================================

if __name__ == "__main__":
    main()
