# SAISA - Super AI Self-Autonomous Agent

> 🤖 Powerful local AI agent that works 100% offline on your machine!

## 🚀 Quick Start

```bash
# Clone the repo
git clone https://github.com/Souraka229/local-agent-windows
cd local-agent-windows

# Install dependencies
pip install -r requirements.txt

# Configure (optional)
cp .env.example .env

# Run with Ollama (recommended)
ollama run llama3.2
python main.py

# OR use Groq API
python main.py
```

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🧠 Local AI | Powered by Ollama (Gemma/Llama) - no cloud, zero latency |
| 🎯 Autonomous | Run tasks automatically with `/autopilot` |
| 🌐 Web Search | DuckDuckGo integration for live search |
| 📦 Docker | Container management support |
| 🔧 Git Built-in | Full Git command integration |
| 💾 Learning Memory | SQLite that learns from mistakes |
| 🔒 Safe Sandbox | Docker isolation for secure execution |
| 🛠️ Extensible | Plugin system with skills |

## 📁 Architecture

```
local-agent-windows/
├── brain/              # AI Brain (Ollama - Planning)
├── agents/             # Orchestrator (7 specialized agents)
├── tools/             # Tool Layer + Browser (Playwright)
├── memory/             # Learning System
├── sandbox/            # Docker Sandbox
├── api/                # CLI Interface
└── main.py             # Entry Point
```

## ⚙️ Configuration

Create `.env` file:

```env
# Backend: ollama or groq
AGENT_BACKEND=ollama

# Ollama settings
OLLAMA_MODEL=llama3.2

# Enable features
ALLOW_GIT=1
ALLOW_DOCKER=1
ALLOW_SYSTEM_MONITOR=1
AUTONOMOUS_MODE=1
LEARNING_MODE=1

# Custom name
AGENT_NAME=SAISA
```

## 📖 Commands

```bash
# Interactive mode
python -m api.cli --interactive

# Autonomous mode
python main.py
/autopilot 60 create a Python project

# Check stats
python -m api.cli --stats
```

## 🧠 How AI Learns

1. **Memory** - Saves every conversation
2. **Error Analysis** - Learns from failures
3. **Skills** - Remembers successful tasks
4. **Score** - Tracks progress

## 🤝 Contributing

Contributions welcome! Open an issue or PR.

## 📜 License

MIT License - see LICENSE file.

---

**⭐ Star if useful!**

Made with ❤️ by @Souraka229
