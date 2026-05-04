# 🧠 SAISA - Super AI Self-Autonomous Agent

> The most powerful 100% local AI agent that runs completely offline on your machine!

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/Souraka229/local-agent-windows?style=social)](https://github.com/Souraka229/local-agent-windows)

## ⚡ Why SAISA?

- 🔒 **100% Offline** - Your data never leaves your machine
- 🚀 **Fast** - Local AI with zero API latency
- 🤖 **Autonomous** - Can run tasks while you sleep
- 💰 **Free** - No API costs, uses Ollama
- 🔧 **Extensible** - Plugin system for custom skills

## 🚀 Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/Souraka229/local-agent-windows
cd local-agent-windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure (optional)
cp .env.example .env

# 4. Start Ollama (for local AI)
ollama run llama3.2

# 5. Run the agent!
python main.py
```

**Or use Groq API (cloud):**
```bash
AGENT_BACKEND=groq GROQ_API_KEY=your_key python main.py
```

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🧠 **Local AI** | Powered by Ollama (Llama 3.2, Gemma) |
| 🎯 **Autonomous Mode** | Run tasks automatically with `/autopilot` |
| 🌐 **Web Search** | DuckDuckGo integration |
| 📦 **Docker** | Container management |
| 🔧 **Git Built-in** | Full Git command support |
| 💾 **Learning Memory** | SQLite that learns from mistakes |
| 🔒 **Sandbox** | Docker isolation for security |
| 🛠️ **Skills** | Extensible plugin system |

## 📁 Project Structure

```
local-agent-windows/
├── brain/              # AI Brain (planning & reasoning)
├── agents/             # Task orchestrator
├── tools/              # Tool layer + browser automation
├── memory/             # Learning system
├── sandbox/            # Docker execution sandbox
├── api/                # CLI interface
├── workspace/          # Your working files
└── main.py             # Entry point
```

## ⚙️ Configuration

Create a `.env` file:

```env
# AI Backend: ollama or groq
AGENT_BACKEND=ollama

# Ollama model
OLLAMA_MODEL=llama3.2

# Enable features
ALLOW_GIT=1
ALLOW_DOCKER=1
ALLOW_SYSTEM_MONITOR=1
AUTONOMOUS_MODE=1
LEARNING_MODE=1

# Customize
AGENT_NAME=SAISA
AGENT_OWNER_NAME=YourName
```

## 📖 Usage

```bash
# Interactive chat mode
python -m api.cli --interactive

# Autonomous mode (run for 60 minutes)
python main.py
/autopilot 60 create a Python project

# Check agent stats
python -m api.cli --stats

# Export conversation
python -m api.cli --export
```

## 🧠 How It Learns

SAISA gets smarter over time:

1. **📝 Memory** - Saves every conversation
2. **🔍 Error Analysis** - Learns from failures  
3. **✅ Skills** - Remembers successful patterns
4. **📊 Score** - Tracks progress and improvement

## 🤝 Contributing

We welcome contributions! 

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/amazing`)
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📜 License

MIT License - free to use, modify, and distribute.

---

<div align="center">

**⭐ Star this repo if it helps you!**

Made with ❤️ by [@Souraka229](https://github.com/Souraka229)

</div>
