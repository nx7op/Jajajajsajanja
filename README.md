# 🤖 Nova AI Bot - Advanced Telegram AI Assistant

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.11+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

**Ultra-advanced Telegram AI Bot powered by OpenRouter & NVIDIA Nemotron Ultra Model!**

## ✨ Features

### 🎯 Core Features
- **🧠 Advanced AI**: Powered by `nvidia/nemotron-3-ultra-550b-a55b:free` via OpenRouter
- **⌨️ Live Typing**: Real-time typing indicators while processing
- **📡 Streaming Responses**: Watch responses generate in real-time
- **🧠 Conversation Memory**: Remembers context across messages
- **🎨 Beautiful Terminal**: Colorful output with animations

### ⚙️ Advanced Features
- **🔄 Auto Fallback**: Multiple model fallback if primary fails
- **⏱️ Rate Limiting**: Per-user rate limiting
- **📊 Statistics**: Usage stats & analytics
- **🛡️ Error Handling**: Robust error recovery
- **🚀 Railway Ready**: One-click deployment

## 📋 Commands

| Command | Description |
|---------|-------------|
| `/start` | Start the bot & see welcome |
| `/help` | View help guide |
| `/model` | See current AI model info |
| `/clear` | Clear conversation memory |
| `/stats` | View your statistics |

### Admin Commands
| Command | Description |
|---------|-------------|
| `/broadcast <msg>` | Broadcast to all users (owner) |
| `/users` | Active user count (admin) |

## 🔧 Setup

### 1. Get OpenRouter API Key (FREE!)
1. Go to [OpenRouter.ai](https://openrouter.ai/)
2. Sign up / Login
3. Go to API Keys → Create key
4. Copy your API key

### 2. Create Telegram Bot
1. Message [@BotFather](https://t.me/BotFather) on Telegram
2. Send `/newbot`
3. Follow instructions to create bot
4. Copy the bot token

### 3. Deploy to Railway

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template-url=...)

#### Or Manual Deploy:

```bash
# Fork/Clone this repo
git clone https://github.com/nx7op/Jajajajsajanja.git
cd Jajajajsajanja

# Add to Railway Environment Variables:
BOT_TOKEN=your_telegram_bot_token
OPENROUTER_API_KEY=your_openrouter_api_key

# Push to GitHub - Railway auto-deploys!
git push origin main
```

### Required Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `BOT_TOKEN` | Telegram bot token from @BotFather | `123456:ABC...` |
| `OPENROUTER_API_KEY` | Your OpenRouter API key | `sk-or-v1-...` |

### Optional Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `AI_MODEL` | `nvidia/nemotron-3-ultra-550b-a55b:free` | AI model to use |
| `MAX_TOKENS` | `2048` | Max response tokens |
| `TEMPERATURE` | `0.7` | Response creativity (0-2) |
| `MAX_HISTORY` | `20` | Messages to remember per user |
| `OWNER_ID` | - | Owner's Telegram ID for admin commands |
| `PORT` | `8080` | Health check port |

## 🚀 Local Development

```bash
# Clone repo
git clone https://github.com/nx7op/Jajajajsajanja.git
cd Jajajajsajanja

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export BOT_TOKEN="your_bot_token"
export OPENROUTER_API_KEY="your_api_key"

# Run the bot!
python bot.py
```

## 📁 Project Structure

```
nova-ai-bot/
├── bot.py              # Main bot file with all handlers
├── config.py           # Configuration management
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker config for Railway
├── .gitignore         # Git ignore rules
└── utils/
    ├── __init__.py    # Package init
    └── ai_engine.py   # AI engine with OpenRouter
```

## 🎨 Terminal Preview

When you run the bot, you'll see:

```
╔══════════════════════════════════════════════════════╗
║  🤖 NOVA AI BOT - ADVANCED EDITION                  ║
╠══════════════════════════════════════════════════════╣
║                                                    ║
║  ✓ Live Typing Indicators                          ║
║  ✓ Streaming Responses                             ║
║  ✓ OpenRouter Nemotron Model                       ║
║  ✓ Conversation Memory                             ║
║  ✓ Railway Deployment Ready                        ║
║                                                    ║
╚══════════════════════════════════════════════════════╝

  [14:32:05] ℹ  Initializing Nova AI Bot...
  [14:32:06] ✔  Bot initialized successfully!
  [14:32:06] ℹ  Model: nemotron-3-ultra-550b-a55b:free
  
  ══════════════════════════════════════════════════
    🚀 Bot is LIVE and ready!
    Waiting for messages...
  ══════════════════════════════════════════════════

  [14:33:01] ◀ [USER] John: Hello! How are you?
  [14:33:02] ▶ [NOVA] Hello John! I'm doing great, thanks...
  ✔  Response to John: 156 chars in 1.23s
```

## 🤖 Supported AI Models (Free!)

The bot uses these free models from OpenRouter:

1. **Primary**: `nvidia/nemotron-3-ultra-550b-a55b:free`
2. **Fallback 1**: `meta-llama/llama-3.3-70b-instruct:free`
3. **Fallback 2**: `mistralai/mistral-7b-instruct:free`
4. **Fallback 3**: `google/gemma-2-9b-it:free`

## 📄 License

MIT License - Feel free to use, modify, and distribute!

## 👨‍💻 Author

Created with ❤️ by Advanced AI Development Team

---

**⭐ Star this repo if you find it useful!**

**🐛 Found a bug? [Report Issue](https://github.com/nx7op/Jajajajsajanja/issues)**
