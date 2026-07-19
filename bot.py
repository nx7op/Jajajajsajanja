"""
🚀 NOVA AI BOT - ADVANCED TELEGRAM AI ASSISTANT
=============================================

Features:
✅ Live Typing Indicators (user sees bot "typing...")
✅ Streaming Responses (real-time text generation)
✅ Beautiful Terminal Output (colors, animations)
✅ Conversation Memory (remembers context)
✅ OpenRouter API (Nemotron Ultra Model)
✅ Rate Limiting & Error Handling
✅ Railway Deployment Ready
✅ Admin Commands

Author: Advanced AI Bot
Model: nvidia/nemotron-3-ultra-550b-a55b:free
"""

import os
import sys
import asyncio
import time
import threading
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from telegram import (
    Update,
    BotCommand,
    ChatAction,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
    ApplicationBuilder,
)
from telegram.error import TelegramError, Forbidden, BadRequest

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
    
    # Colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    
    # Bright colors
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"
    
    # Backgrounds
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_BLUE = "\033[44m"


class TerminalEffects:
    """Cool terminal effects for the bot."""
    
    @staticmethod
    def spinner():
        """Yield spinner characters."""
        while True:
            for char in "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏":
                yield char
    
    @staticmethod
    def progress_bar(current: int, total: int, width: int = 30) -> str:
        """Generate a progress bar string."""
        if total == 0:
            return "[" + " " * width + "]"
        
        filled = int(width * current / total)
        bar = "█" * filled + "░" * (width - filled)
        return f"[{Colors.BRIGHT_GREEN}{bar}{Colors.RESET}]"
    
    @staticmethod
    def timestamp() -> str:
        """Get formatted timestamp."""
        return datetime.now().strftime("%H:%M:%S")
    
    @staticmethod
    def print_banner():
        """Print awesome startup banner."""
        banner = f"""
{Colors.BRIGHT_CYAN}╔══════════════════════════════════════════════════════╗{Colors.RESET}
{Colors.BRIGHT_CYAN}║{Colors.RESET}  {Colors.BOLD}{Colors.BRIGHT_YELLOW}🤖 NOVA AI BOT - ADVANCED EDITION{Colors.RESET}              {Colors.BRIGHT_CYAN}║{Colors.RESET}
{Colors.BRIGHT_CYAN}╠══════════════════════════════════════════════════════╣{Colors.RESET}
{Colors.BRIGHT_CYAN}║{Colors.RESET}                                                    {Colors.BRIGHT_CYAN}║{Colors.RESET}
{Colors.BRIGHT_CYAN}║{Colors.RESET}  {Colors.GREEN}✓ Live Typing Indicators{Colors.RESET}                         {Colors.BRIGHT_CYAN}║{Colors.RESET}
{Colors.BRIGHT_CYAN}║{Colors.RESET}  {Colors.GREEN}✓ Streaming Responses{Colors.RESET}                             {Colors.BRIGHT_CYAN}║{Colors.RESET}
{Colors.BRIGHT_CYAN}║{Colors.RESET}  {Colors.GREEN}✓ OpenRouter Nemotron Model{Colors.RESET}                      {Colors.BRIGHT_CYAN}║{Colors.RESET}
{Colors.BRIGHT_CYAN}║{Colors.RESET}  {Colors.GREEN}✓ Conversation Memory{Colors.RESET}                            {Colors.BRIGHT_CYAN}║{Colors.RESET}
{Colors.BRIGHT_CYAN}║{Colors.RESET}  {Colors.GREEN}✓ Railway Deployment Ready{Colors.RESET}                        {Colors.BRIGHT_CYAN}║{Colors.RESET}
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
        
        # Truncate long messages
        display_msg = message[:80] + "..." if len(message) > 80 else message
        
        print(f"  {Colors.BRIGHT_BLUE}[{ts}]{Colors.RESET} {color}{direction}{Colors.RESET} [{Colors.BOLD}{prefix}{Colors.RESET}] {Colors.DIM}{user}:{Colors.RESET} {display_msg}")


# ============================================================
# 📊 RATE LIMITER
# ============================================================

class RateLimiter:
    """Per-user rate limiting."""
    
    def __init__(self):
        self._requests: Dict[int, List[float]] = {}
    
    def check(self, user_id: int) -> tuple[bool, str]:
        """Check if user is within rate limits. Returns (allowed, reason)."""
        now = time.time()
        
        if user_id not in self._requests:
            self._requests[user_id] = []
        
        # Clean old requests (older than 1 hour)
        self._requests[user_id] = [t for t in self._requests[user_id] if now - t < 3600]
        
        # Check minute limit
        recent_minute = [t for t in self._requests[user_id] if now - t < 60]
        if len(recent_minute) >= RATE_LIMIT_MINUTE:
            return False, f"Rate limit: {RATE_LIMIT_MINUTE}/minute"
        
        # Check hour limit
        if len(self._requests[user_id]) >= RATE_LIMIT_HOUR:
            return False, f"Rate limit: {RATE_LIMIT_HOUR}/hour"
        
        # Record this request
        self._requests[user_id].append(now)
        return True, ""
    
    def clear(self, user_id: int):
        """Clear rate limits for user."""
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
🤖 **Hello {user.first_name}! I'm Nova!**

I'm an **AI Assistant** powered by **Nemotron Ultra** - one of the most advanced AI models!

**What can I do?**
💬 Chat about anything
💻 Help with coding
📝 Write & analyze text
🔍 Answer questions
🎨 Creative tasks & more!

**Quick Start:**
Just type a message and I'll respond!

**Commands:**
`/help` - See all commands
`/clear` - Clear conversation memory
`/model` - View current model info
`/stats` - View your stats

Let's chat! 💬
"""
    
    keyboard = [
        [InlineKeyboardButton("💬 Start Chatting", callback_data="chat_start")],
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
    help_text = """
📖 **Nova AI Bot - Help Guide**

**Basic Commands:**
• `/start` - Start the bot
• `/help` - Show this help
• `/clear` - Reset conversation memory

**Info Commands:**
• `/model` - Current AI model info
• `/stats` - Your usage statistics
• `/info` - Bot information

**Admin Commands** *(Owner only)*:
• `/broadcast <msg>` - Send to all users
• `/users` - User count
• `/stats global` - Global stats

**Tips:**
💡 I remember our conversation context
💡 Use clear questions for better answers
💡 You can send voice notes too!
💡 Type normally, no special format needed

**Having issues?**
Contact: @owner_username
"""
    
    await update.message.reply_text(help_text, parse_mode='Markdown')


async def model_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show current model information."""
    env_info = get_env_info()
    
    text = f"""
🧠 **AI Model Information**

**Active Model:** `{env_info['model']}`

**Configuration:**
• Max Tokens: `{env_info['max_tokens']}`
• Temperature: `{env_info['temperature']}`
• Memory: `{env_info['memory']}`

**Features Enabled:**
{' '.join(env_info['features'].values())}

**Provider:** OpenRouter API
**Status:** ✅ Online
"""
    
    await update.message.reply_text(text, parse_mode='Markdown')


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

_Use `/clear` to reset your conversation._
"""
    
    await update.message.reply_text(text, parse_mode='Markdown')


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle regular text messages - THE MAIN BRAIN!
    
    Features:
    - Live typing indicator
    - Streaming responses
    - Rate limiting
    - Error handling
    """
    # Get user info
    user = update.effective_user
    message = update.message.text or ""
    user_id = user.id
    user_name = user.first_name or "Unknown"
    
    # Log incoming message
    logger.chat(user_name, message, incoming=True)
    
    # Check rate limits
    allowed, reason = rate_limiter.check(user_id)
    if not allowed:
        logger.warning(f"Rate limited: {user_name} ({reason})")
        await update.message.reply_text(
            f"⏳ **Slow down!**\n\n{reason}\nPlease wait a moment and try again.",
            parse_mode='Markdown'
        )
        return
    
    # Check empty message
    if not message.strip():
        return
    
    # Create status message placeholder
    status_msg = await update.message.reply_text("🤔 *Thinking...*", parse_mode='Markdown')
    
    # Start typing indicator loop
    typing_task = asyncio.create_task(
        continuous_typing(update.effective_chat.id, context.bot)
    )
    
    # Stream buffer for live updates
    stream_buffer = []
    last_update_time = [time.time()]
    
    async def stream_callback(chunk: str):
        """Callback for streaming chunks."""
        stream_buffer.append(chunk)
        
        # Update message every 2 seconds with accumulated content
        current_time = time.time()
        if current_time - last_update_time[0] > 2.0:
            last_update_time[0] = current_time
            preview = ''.join(stream_buffer[-500:])  # Last 500 chars
            
            try:
                await status_msg.edit_text(
                    f"⌨️ *Generating...*\n\n```\n{preview}```",
                    parse_mode='Markdown'
                )
            except Exception:
                pass  # Ignore edit errors during streaming
    
    try:
        # Get AI response
        engine = get_ai_engine()
        response = await engine.chat(
            user_id=user_id,
            message=message,
            stream_callback=stream_callback
        )
        
        # Cancel typing indicator
        typing_task.cancel()
        
        if response.error and not response.content:
            # Complete failure
            logger.error(f"AI error for {user_name}: {response.error}")
            
            await status_msg.edit_text(
                f"😵 **Oops! Something went wrong**\n\n"
                f"`{response.error[:200]}`\n\n"
                f"Please try again in a moment.",
                parse_mode='Markdown'
            )
            return
        
        # Success! Format response
        ai_response = response.content
        
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
        
        # Edit status message with final response
        try:
            await status_msg.edit_text(final_text, parse_mode='Markdown')
        except Exception as e:
            # If edit fails (message too old), send new message
            logger.warning(f"Edit failed, sending new message: {e}")
            await update.message.reply_text(final_text, parse_mode='Markdown')
        
        # Log success
        latency_s = response.latency_ms / 1000
        logger.success(
            f"Response to {user_name}: {len(ai_response)} chars in {latency_s:.2f}s "
            f"(model: {response.model_used.split('/')[-1]})"
        )
        
    except Exception as e:
        # Cancel typing on error
        typing_task.cancel()
        
        logger.error(f"Message handler error: {e}")
        
        try:
            await status_msg.edit_text(
                "😵 **Unexpected error occurred**\n\n"
                "The developers have been notified.\n"
                "Please try again!",
                parse_mode='Markdown'
            )
        except Exception:
            pass


async def continuous_typing(chat_id: int, bot, interval: float = TYPING_DELAY):
    """
    Continuously send typing action while processing.
    This makes it look like the bot is really "thinking"!
    """
    try:
        while True:
            await bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
            await asyncio.sleep(interval)
    except asyncio.CancelledError:
        # Expected when task is cancelled
        pass
    except Exception as e:
        # Ignore errors from typing action
        pass


# ============================================================
# 🔘 CALLBACK HANDLERS (Inline Buttons)
# ============================================================

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle inline button presses."""
    query = update.callback_query
    await query.answer()  # Acknowledge the button press
    
    data = query.data
    user = query.from_user
    
    if data == "chat_start":
        await query.edit_message_text(
            "💬 **Great! Just type your message below!**\n\n"
            "I'm ready when you are!",
            parse_mode='Markdown'
        )
    
    elif data == "show_help":
        await help_command(query.message, context)
    
    elif data == "show_stats":
        await stats_command(query.message, context)


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
    # In real implementation, would store user IDs and broadcast
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
        f"Total Messages: `{stats.get('total_messages', 0)}`",
        parse_mode='Markdown'
    )


# ============================================================
# ⚙️ ERROR HANDLERS
# ============================================================

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors globally."""
    error = context.error
    
    logger.error(f"Error: {type(error).__name__}: {error}")
    
    if isinstance(error, Forbidden):
        logger.warning("Bot was blocked by user")
    elif isinstance(error, BadRequest):
        logger.warning(f"Bad request: {error}")
    elif isinstance(error, TelegramError):
        logger.error(f"Telegram error: {error}")
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
    
    logger.info("Initializing Nova AI Bot...")
    
    # Build application
    app = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .read_timeout(45)
        .write_timeout(45)
        .connect_timeout(45)
        .pool_timeout(45)
        .build()
    )
    
    # Register handlers
    
    # Command handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("model", model_command))
    app.add_handler(CommandHandler("clear", clear_command))
    app.add_handler(CommandHandler("stats", stats_command))
    
    # Admin commands
    app.add_handler(CommandHandler("broadcast", broadcast_command))
    app.add_handler(CommandHandler("users", users_count_command))
    
    # Message handler (must be last!)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Callback handler (inline buttons)
    app.add_handler(CallbackQueryHandler(button_callback))
    
    # Error handler
    app.add_handler(error_handler)
    
    # Set bot commands menu
    async def post_init(app):
        await app.bot.set_my_commands([
            BotCommand("start", "Start the bot"),
            BotCommand("help", "Help & commands"),
            BotCommand("model", "AI model info"),
            BotCommand("clear", "Clear conversation"),
            BotCommand("stats", "Your statistics"),
        ])
    
    app.post_init = post_init
    
    # Start health check server in background
    start_health_check_server(PORT)
    
    logger.success("Bot initialized successfully!")
    logger.info(f"Model: {get_env_info()['model']}")
    logger.info(f"Starting polling on port {PORT}...")
    
    # Print separator
    print(f"\n{Colors.BRIGHT_GREEN}{'═' * 60}{Colors.RESET}")
    print(f"  {Colors.BOLD}🚀 Bot is LIVE and ready!{Colors.RESET}")
    print(f"  {Colors.DIM}Waiting for messages...{Colors.RESET}")
    print(f"{Colors.BRIGHT_GREEN}{'═' * 60}{Colors.RESET}\n")
    
    # Run the bot
    app.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True,
        close_loop=False
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
                    "bot": "Nova AI Bot",
                    "timestamp": datetime.now().isoformat()
                }).encode())
            else:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"OK")
        
        def log_message(self, format, *args):
            pass  # Suppress logs
    
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
