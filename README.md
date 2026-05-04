# 🧠 SAISA - Super AI Self-Autonomous Agent

> The most powerful 100% local AI agent that runs completely offline on your machine!

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/Souraka229/local-agent-windows?style=social)](https://github.com/Souraka229/local-agent-windows)

---

## ⚡ Why SAISA?

- 🔒 **100% Offline** - Your data never leaves your machine
- 🚀 **Fast** - Local AI with zero API latency
- 🤖 **Autonomous** - Can run tasks while you sleep
- 💰 **Free** - No API costs, uses Ollama
- 🔧 **Extensible** - Plugin system for custom skills

---

## 🚀 Quick Start (Windows)

### Option 1: PowerShell (Recommended)

```powershell
# Clone the repository
git clone https://github.com/Souraka229/local-agent-windows
cd local-agent-windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
$env:AGENT_BACKEND = "ollama"
$env:OLLAMA_MODEL = "llama3.2"

# Start Ollama (in a new terminal)
ollama serve
ollama run llama3.2

# Run the agent
python main.py
```

### Option 2: CMD

```cmd
git clone https://github.com/Souraka229/local-agent-windows
cd local-agent-windows
pip install -r requirements.txt
set AGENT_BACKEND=ollama
set OLLAMA_MODEL=llama3.2
ollama serve
python main.py
```

### Option 3: Groq API (Cloud - No Ollama needed)

```powershell
# Create .env file first
$env:AGENT_BACKEND = "groq"
$env:GROQ_API_KEY = "gsk_your_key_here"
python main.py
```

---

## 📋 Requirements

| Package | Description |
|---------|-------------|
| Python 3.10+ | Runtime |
| python-dotenv | Environment loading |
| httpx | HTTP client |
| duckduckgo_search | Web search |
| playwright | Browser automation |
| pytest | Testing |

**Install all:**
```bash
pip install -r requirements.txt
```

### Ollama Installation (Windows)

Download from: https://ollama.com

Or PowerShell:
```powershell
irm https://ollama.com/install.ps1 | iex
```

---

## ⚙️ Configuration

### Using .env file (Recommended)

Create a `.env` file in the project root:

```env
# =============================================================================
# AI BACKEND CONFIGURATION
# =============================================================================

# Choose: "ollama" (local, free) or "groq" (cloud, fast)
AGENT_BACKEND=ollama

# =============================================================================
# OLLAMA CONFIG (local AI)
# =============================================================================
OLLAMA_MODEL=llama3.2
OLLAMA_BASE_URL=http://localhost:11434

# =============================================================================
# GROQ CONFIG (cloud AI) - Only if AGENT_BACKEND=groq
# =============================================================================
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=mixtral-8x7b-32768

# =============================================================================
# FEATURE FLAGS (1 = enabled, 0 = disabled)
# =============================================================================
ALLOW_GIT=1
ALLOW_DOCKER=0
ALLOW_POWERSHELL=1
ALLOW_OPEN_BROWSER=1
ALLOW_FETCH_URL=1
ALLOW_SMTP_SEND=0
ALLOW_SYSTEM_MONITOR=1

# =============================================================================
# AUTONOMOUS MODE
# =============================================================================
AUTONOMOUS_MODE=1
AGENT_MAX_TOOL_ROUNDS=25

# =============================================================================
# MEMORY & LEARNING
# =============================================================================
LEARNING_MODE=1

# =============================================================================
# PERSONALIZATION
# =============================================================================
AGENT_NAME=SAISA
AGENT_OWNER_NAME=YourName
```

### Windows Environment Variables

**PowerShell:**
```powershell
$env:AGENT_BACKEND = "groq"
$env:GROQ_API_KEY = "gsk_..."
python main.py
```

**CMD:**
```cmd
set AGENT_BACKEND=groq
set GROQ_API_KEY=gsk_...
python main.py
```

---

## 📖 Usage

### Interactive Chat

```bash
python main.py
```

Then type your task. Type `quit` to exit.

### CLI Interface

```bash
# Interactive mode
python -m api.cli --interactive

# One-liner
python -m api.cli "create a hello world program"

# Statistics
python -m api.cli --stats
```

### Web Interface

```bash
python web.py
# Then open http://localhost:7860
```

---

## 🏗️ Architecture

```
local-agent-windows/
├── brain/                  # AI Brain (Cerebrum)
│   └── cerebrum.py         # Task analysis & planning
├── agents/                 # Orchestrator
│   └── orchestrator.py    # Sub-agents coordination
├── tools/                 # Tool Layer
│   ├── tool_layer.py      # Tool management
│   └── specialists/      # Browser automation
├── memory/                # Learning system
│   └── semantic/        # SQLite memory
├── local_agent/           # Core agent
│   ├── config.py        # Configuration
│   ├── tools.py        # ToolContext
│   ├── groq_agent.py   # Groq backend
│   ├── ollama_agent.py # Ollama backend
│   └── prompts.py     # System prompts
├── api/                  # CLI interface
│   └── cli.py          # Terminal UI
├── sandbox/             # Docker sandbox
├── workspace/           # Working files
├── main.py             # Entry point
├── simple.py           # Simple mode
└── web.py              # Web UI
```

---

## 🤖 Sub-Agents

| Agent | Tools | Description |
|-------|-------|-------------|
| `code` | write_file, run_powershell | Generate & execute code |
| `browser` | web_search, fetch_url, open_browser | Internet search |
| `terminal` | run_powershell | Shell commands |
| `git` | run_git | Git operations |
| `docker` | docker_ps, docker_exec | Container management |
| `test` | run_powershell | Run tests (pytest, jest) |
| `crud` | write_file, read_file, delete_file | File operations |
| `fix` | read_file, append_memory_note | Error fixing |

---

## 🔧 Available Tools

| Tool | Description | Requires |
|------|-------------|----------|
| `list_dir(path)` | List directory contents | - |
| `read_file(path)` | Read file content | - |
| `write_file(path, content)` | Write file | - |
| `delete_file(path)` | Delete file | DeleteGuard |
| `run_powershell(cmd)` | Execute command | ALLOW_POWERSHELL=1 |
| `web_search(query)` | DuckDuckGo search | - |
| `fetch_url(url)` | Download URL content | ALLOW_FETCH_URL=1 |
| `open_browser_url(url)` | Open browser | ALLOW_OPEN_BROWSER=1 |
| `run_git(cmd)` | Git command | ALLOW_GIT=1 |
| `docker_ps()` | List containers | ALLOW_DOCKER=1 |
| `docker_exec(container, cmd)` | Run in container | ALLOW_DOCKER=1 |
| `send_smtp_email(to, subject, body)` | Send email | ALLOW_SMTP_SEND=1 |
| `append_memory_note(note, tag)` | Save to memory | - |
| `read_memory_notes(tag)` | Read memory | - |
| `system_info()` | System information | ALLOW_SYSTEM_MONITOR=1 |

---

## 🧠 How It Works

```
User Input → Cerebrum (AI Brain)
              ↓
         Analyzes task
              ↓
         Creates execution plan
              ↓
Orchestrator → Sub-agents
              ↓
         Execute steps via ToolContext
              ↓
         Results → Memory (learning)
```

1. **Cerebrum** analyzes your task using AI
2. **Orchestrator** breaks task into steps
3. **Sub-agents** execute each step using real tools
4. **Memory** learns from success/failure

---

## ⚠️ Security

- **Workspace isolation** - Can't access files outside `workspace/`
- **DeleteGuard** - Requires 5 "YES" confirmations to delete
- **Command blocking** - Dangerous commands blocked
- **Sandbox** - Optional Docker isolation

---

## 🛠️ Troubleshooting

### "command not found"

**PowerShell:**
```powershell
$env:Path += ";$env:LOCALAPPDATA\Ollama"
```

**CMD:**
```cmd
set PATH=%PATH%;%LOCALAPPDATA%\Ollama
```

### Ollama not running

```powershell
ollama serve
```

### Connection refused

```powershell
# Check Ollama is running
ollama list

# If no models, pull one
ollama pull llama3.2
```

### Groq API error

Check your API key in `.env`:
```env
GROQ_API_KEY=gsk_... (not gsk_zq...)
```

---

## 📝 Examples

### Create a Python project

```bash
python main.py
# Then type:
create a Python web scraper for news articles
```

### Search the web

```bash
python main.py
# Then type:
search python asyncio best practices
```

### Run Docker commands

```bash
# Enable in .env first
ALLOW_DOCKER=1

python main.py
docker ps
```

---

## 🙏 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing`)
3. Commit changes
4. Push to branch
5. Open Pull Request

---

## 📜 License

MIT License - free to use, modify, and distribute.

---

<div align="center">

**⭐ Star this repo if it helps you!**

Made with ❤️ by [@Souraka229](https://github.com/Souraka229)

</div>
