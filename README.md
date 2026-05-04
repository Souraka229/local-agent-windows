<div align="center">

# 🧠 SAISA v2

### Super AI Self-Autonomous Coding Agent

> Open-source, local-first, multi-provider terminal coding agent.
> Like Claude Code and Cursor — but yours.

<p>
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge" alt="License">
  <img src="https://img.shields.io/badge/Open_Source-100%25-orange?style=for-the-badge&logo=opensourceinitiative" alt="Open Source">
  <img src="https://img.shields.io/badge/Local_First-Ollama-ff6b35?style=for-the-badge" alt="Local First">
</p>

**Created by [Souraka HAMIDA](https://souraka.restafy.shop) — [@Souraka229](https://github.com/Souraka229)**

---

[Installation](#-installation) · [Quick Start](#-quick-start) · [Features](#-features) · [Configuration](#-configuration) · [Ollama Guide](./docs/OLLAMA.md)

</div>

---

## ❓ What is SAISA?

SAISA is a **terminal-based autonomous coding agent** that reads, writes, edits, searches, and runs code directly on your machine. It can handle **entire projects** — from scaffolding to deployment.

```
┌─────────────────────────────────────────────────────────┐
│   You  ───────►  SAISA  ───────►  Your Code          │
│                    │                                  │
│              ┌─────┼─────┐                          │
│              │     │     │                          │
│           Read   Edit   Run     Search   Git   Build     │
│           Files  Code   Shell   Code     Ops   Deploy      │
│                                                         │
│   Powered by: Ollama | Groq | OpenAI | Anthropic        │
└─────────────────────────────────────────────────────────┘
```

---

## ✨ Why SAISA?

| Feature | Description |
|---------|-------------|
| 🔒 **100% Local** | Your code never leaves your machine |
| 🚀 **Autonomous** | Can handle full projects while you sleep |
| 💰 **Free** | Uses Ollama — no API costs |
| 🤖 **Multi-Provider** | Ollama, Groq, OpenAI, Anthropic |
| 🛠️ **8 Specialized Agents** | Code, Browser, Git, Docker, Terminal, Test, Fix, CRUD |
| 💾 **Memory** | Remembers your project context |
| 🔌 **Extensible** | Plugin system for custom skills |

---

## 📦 Installation

### Windows (PowerShell)

```powershell
# Clone
git clone https://github.com/Souraka229/local-agent-windows
cd local-agent-windows

# Install dependencies
pip install -r requirements.txt

# Configure
$env:AGENT_BACKEND = "ollama"
$env:OLLAMA_MODEL = "llama3.2"

# Start Ollama (new terminal)
ollama serve

# Run
python main.py
```

### Linux/macOS

```bash
git clone https://github.com/Souraka229/local-agent-windows
cd local-agent-windows
pip install -r requirements.txt
export AGENT_BACKEND=ollama
export OLLAMA_MODEL=llama3.2
python main.py
```

### Groq API (Cloud - No Ollama needed)

```powershell
$env:AGENT_BACKEND = "groq"
$env:GROQ_API_KEY = "gsk_your_key_here"
python main.py
```

---

## 🚀 Quick Start

1. **Create `.env`:**
```env
AGENT_BACKEND=ollama
OLLAMA_MODEL=llama3.2
```

2. **Run:**
```powershell
python main.py
```

3. **Give a task:**
```
> Create a Python hello world app in /workspace/project
```

---

## ⚙️ Configuration

### `.env` Options

| Variable | Description | Default |
|----------|-------------|---------|
| `AGENT_BACKEND` | Provider: `ollama`, `groq`, `openai`, `anthropic` | `ollama` |
| `OLLAMA_MODEL` | Ollama model name | `llama3.2` |
| `GROQ_API_KEY` | Groq API key | - |
| `OPENAI_API_KEY` | OpenAI API key | - |
| `ANTHROPIC_API_KEY` | Anthropic API key | - |
| `OLLAMA_BASE_URL` | Ollama server URL | `http://localhost:11434` |
| `OLLAMA_TEMPERATURE` | Creativity (0-1) | `0.7` |

---

## 🤖 Agents

| Agent | Tools | Description |
|-------|-------|------------|
| `code` | write_file, run_powershell | Generate & execute code |
| `browser` | web_search, fetch_url, open_browser | Web research |
| `terminal` | run_powershell | Direct shell commands |
| `git` | run_git | Git operations |
| `docker` | docker_ps, docker_exec | Docker management |
| `test` | run_powershell (pytest) | Run tests |
| `fix` | run_powershell, write_file | Debug & fix |
| `crud` | write_file, read_file, delete_file | File operations |

---

## 📁 Project Structure

```
local-agent-windows/
├── main.py                 # Entry point
├── api/                   # CLI interface
├── agents/               # Sub-agents
│   └── orchestrator.py    # Agent coordinator
├── brain/               # AI Brain
│   └── cerebrum.py     # Task analyzer
├── local_agent/          # Core agent
│   ├── groq_agent.py   # Groq provider
│   ├── ollama_agent.py # Ollama provider
│   └── tools.py       # Tool definitions
├── saisa/              # SAISA v2 features
│   ├── autopilot.py   # Autonomous mode
│   ├── providers/   # Multi-provider
│   └── memory.py   # Context memory
├── docs/               # Documentation
│   └── OLLAMA.md   # Ollama guide
└── workspace/          # Working directory
```

---

## 🛠️ Troubleshooting

### "command not found: ollama"
```powershell
$env:PATH += ";$env:LOCALAPPDATA\Ollama"
```

### "Connection refused"
```powershell
ollama serve
```

### "model not found"
```powershell
ollama pull llama3.2
```

---

## 📖 Complete Guide

See [docs/OLLAMA.md](./docs/OLLAMA.md) for the full Ollama guide.

---

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch
3. Make your changes
4. Submit a PR

---

## 📜 License

MIT License — See [LICENSE](./LICENSE)

---

<div align="center">

**Built with ❤️ by [Souraka HAMIDA](https://souraka.restafy.shop)**

[GitHub](https://github.com/Souraka229) · [Issues](https://github.com/Souraka229/local-agent-windows/issues)

</div>
