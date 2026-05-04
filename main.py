"""
SAISA - Super AI Self-Autonomous Agent
Command-line interface for local AI agent.

Usage: python main.py
"""

from __future__ import annotations

import atexit
import json
import sys
import time
from datetime import datetime
from pathlib import Path

from local_agent.config import (
    AGENT_BACKEND,
    AGENT_OWNER_NAME,
    AGENT_PERFORMANCE_MODE,
    ALLOW_FETCH_URL,
    ALLOW_OPEN_BROWSER,
    ALLOW_POWERSHELL,
    ALLOW_SMTP_SEND,
    GROQ_MODEL,
    OLLAMA_CRITIC_MODEL,
    OLLAMA_MODEL,
    SELF_EVAL_ENABLED,
    WORKSPACE_ROOT,
)
from local_agent.groq_agent import GroqAgent
from local_agent.ollama_agent import OllamaAgent
import httpx

# Constants
OLLAMA_URL = "http://127.0.0.1:11434"
DEFAULT_AUTOPILOT_MINUTES = 60
DEFAULT_AUTOPILOT_TURNS = 120


class AgentError(Exception):
    """Base exception for agent errors."""
    pass


def check_tools_support(model: str) -> bool:
    """Test if the model supports tools.
    
    Args:
        model: Name of the Ollama model to test.
        
    Returns:
        True if tools are supported, False otherwise.
    """
    try:
        client = httpx.Client(timeout=30.0)
        response = client.post(
            f"{OLLAMA_URL}/api/chat",
            json={
                "model": model,
                "messages": [{"role": "user", "content": "ok"}],
                "stream": False
            }
        )
        client.close()
        
        if response.status_code == 200:
            print(f"✓ Model {model} OK")
            return True
        else:
            print(f"⚠ Error {response.status_code}, using simple mode")
            return False
    except Exception as e:
        print(f"⚠ Simple mode: {e}")
        return False


def _read_multiline() -> str:
    """Read multiple lines until /fin is entered.
    
    Returns:
        The concatenated input lines.
    """
    print("(Multiline - paste text, then /fin on a new line)", flush=True)
    lines: list[str] = []
    
    while True:
        try:
            raw = input()
        except (EOFError, KeyboardInterrupt):
            raise
        
        if raw.strip() == "/fin":
            break
        lines.append(raw)
    
    return "\n".join(lines).strip()


def _print_help() -> None:
    """Display available REPL commands."""
    print("\n📖 Available Commands:")
    print("  /help              Show this help")
    print("  /new               Clear conversation history")
    print("  /memory [tag]       Show memory journal (filterable)")
    print("  /status           Show backend/model/options")
    print("  /history          Show conversation history")
    print("  /model <name>     Change model for session")
    print("  /search <query>   Web search")
    print("  /news <query>   News search")
    print("  /note <tag> <text>  Add tagged note")
    print("  /export          Export session")
    print("  /autopilot [min]  Autonomous mode (default 60 min)")
    print("  /paste           Multiline input")
    print("  /quit            Exit agent")
    print()


def _pretty_json(text: str) -> str:
    """Try to parse and format JSON.
    
    Args:
        text: String to parse as JSON.
        
    Returns:
        Formatted JSON or original string.
    """
    try:
        return json.dumps(json.loads(text), ensure_ascii=False, indent=2)
    except Exception:
        return text


def _parse_memory(text: str) -> str:
    """Parse memory content from JSON.
    
    Args:
        text: JSON string to parse.
        
    Returns:
        Extracted content or formatted JSON.
    """
    try:
        data = json.loads(text)
    except Exception:
        return text
    
    content = data.get("content")
    if isinstance(content, str):
        return content
    return json.dumps(data, ensure_ascii=False, indent=2)


def _parse_int(value: str | None, default: int) -> int:
    """Try to parse integer from string.
    
    Args:
        value: String to parse.
        default: Default value if parsing fails.
        
    Returns:
        Parsed integer or default.
    """
    try:
        return int(value) if value else default
    except (TypeError, ValueError):
        return default


def _export_session(agent: GroqAgent | OllamaAgent, title: str = "session") -> Path:
    """Export current history to workspace/memory.
    
    Args:
        agent: The agent instance.
        title: Title for the export.
        
    Returns:
        Path to exported file.
    """
    history: list[dict] = getattr(agent, "_history", [])
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    path = Path(WORKSPACE_ROOT) / "memory" / f"{title}-{timestamp}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    
    lines = [f"# Export: {title}\n"]
    for msg in history:
        role = msg.get("role", "?")
        content = str(msg.get("content", "")).strip()
        lines.append(f"\n## {role}\n{content}\n")
    
    path.write_text("\n".join(lines), encoding="utf-8", newline="")
    return path


def _run_autopilot(agent: GroqAgent | OllamaAgent, objective: str, minutes: int) -> None:
    """Run autonomous mode with time and turn limits.
    
    Args:
        agent: The agent instance.
        objective: The objective to achieve.
        minutes: Maximum runtime in minutes.
    """
    minutes = max(1, min(minutes, 60))
    deadline = time.monotonic() + (minutes * 60)
    started = datetime.now().strftime("%Y%m%d-%H%M%S")
    log_path = Path(WORKSPACE_ROOT) / "memory" / f"autopilot-log-{started}.md"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    log_path.write_text(
        f"# Autopilot Log\n\n- Start: {datetime.now().isoformat(timespec='seconds')}\n- Objective: {objective}\n",
        encoding="utf-8",
        newline="",
    )
    
    turn = 0
    checkpoint_every = 10
    prompt = (
        f"Priority objective: {objective}\n"
        "Work autonomously. If details are missing, propose 2-4 clear choices "
        "and select the most reasonable option to continue without blocking."
    )
    
    print(f"\n🚀 Autopilot started for {minutes} min. Objective: {objective}")
    print(f"📓 Log: {log_path}")
    
    no_progress_count = 0
    
    while time.monotonic() < deadline and turn < DEFAULT_AUTOPILOT_TURNS:
        turn += 1
        print(f"\n--- Turn {turn} ---")
        
        try:
            reply = agent.run_turn(prompt)
        except Exception as e:
            print(f"❌ Error: {e}")
            break
        
        print("🤖 >", reply)
        
        with log_path.open("a", encoding="utf-8", newline="") as f:
            f.write(f"\n\n## Turn {turn}\n{reply}\n")
        
        reply_lower = reply.lower()
        
        # Check for completion signals
        if any(x in reply_lower for x in ["task completed", "mission complete", "objective achieved"]):
            print("✅ Autopilot: Objective declared complete.")
            break
        
        # Check for stuck signals
        if any(x in reply_lower for x in ["no progress", "cannot", "blocked", "stuck"]):
            no_progress_count += 1
        else:
            no_progress_count = 0
        
        if no_progress_count >= 3:
            print("⚠️ Autopilot: Stopping (no progress for 3 turns).")
            break
        
        # Checkpoint every N turns
        if turn % checkpoint_every == 0:
            checkpoint = _export_session(agent, title="checkpoint")
            print(f"💾 Checkpoint: {checkpoint}")
        
        prompt = "Continue working autonomously. Make real progress (code/tests/docs) and don't ask for validation."
    
    # Final export
    final_export = _export_session(agent, title="final")
    
    with log_path.open("a", encoding="utf-8", newline="") as f:
        f.write(
            f"\n\n- End: {datetime.now().isoformat(timespec='seconds')}\n"
            f"- Turns: {turn}\n"
            f"- Export: {final_export}\n"
        )
    
    print(f"\n✅ Autopilot finished. Turns: {turn}")
    print(f"📄 Final export: {final_export}")


def main() -> None:
    """Main entry point."""
    # Configure encoding
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
        except (OSError, ValueError):
            pass

    # Validate backend
    backend = AGENT_BACKEND if AGENT_BACKEND in ("groq", "ollama") else "groq"
    
    # Print header
    print("\n" + "=" * 50)
    print("🧠 SAISA - Super AI Self-Autonomous Agent")
    print("=" * 50)
    print(f"  Performance: {'max' if AGENT_PERFORMANCE_MODE else 'standard'}")
    print(f"  Backend   : {backend}")
    print(f"  Inference: {'local (Ollama)' if backend == 'ollama' else 'cloud (Groq)'}")
    print(f"  Workspace: {WORKSPACE_ROOT}")
    print(f"  Memory   : memory/journal.md")
    print(f"  Skills   : skills/, dissertations/")
    
    if backend == "ollama":
        print(f"  Model    : {OLLAMA_MODEL}")
        print(f"  Critic  : {OLLAMA_CRITIC_MODEL or OLLAMA_MODEL}")
        print(f"  Self-eval: {'enabled' if SELF_EVAL_ENABLED else 'disabled'}")
    else:
        print(f"  Model    : {GROQ_MODEL}")
    
    # Feature flags
    print(f"\n📦 Features:")
    print(f"  PowerShell: {'✓' if ALLOW_POWERSHELL else '✗'}")
    print(f"  fetch_url: {'✓' if ALLOW_FETCH_URL else '✗'}")
    print(f"  SMTP    : {'✓' if ALLOW_SMTP_SEND else '✗'}")
    print(f"  Browser : {'✓' if ALLOW_OPEN_BROWSER else '✗'}")
    
    if AGENT_OWNER_NAME:
        print(f"  Owner   : {AGENT_OWNER_NAME}")
    
    print(f"\n📖 Commands: /help, /status, /history, /memory, /search, /news,")
    print(f"           /note, /model, /export, /autopilot, /quit, /new, /paste")
    print()

    # Initialize agent
    try:
        if backend == "ollama":
            agent: GroqAgent | OllamaAgent = OllamaAgent()
        else:
            agent = GroqAgent()
    except RuntimeError as e:
        print(f"❌ Runtime error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Failed to start agent: {e}", file=sys.stderr)
        sys.exit(1)

    atexit.register(agent.close)

    # Main loop
    while True:
        try:
            line = input("You > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n👋 Goodbye!")
            break
        
        if not line:
            continue
        
        line_lower = line.lower()
        
        # Exit commands
        if line_lower in ("/quit", "/exit", "/q"):
            print("👋 Goodbye!")
            break
        
        # Clear history
        if line_lower in ("/new", "/clear"):
            agent.clear_history()
            print("✅ History cleared.")
            continue
        
        # Help
        if line_lower == "/help":
            _print_help()
            continue
        
        # Status
        if line_lower == "/status":
            model = getattr(agent, "_model", "?")
            print(f"Backend: {backend}")
            print(f"Model: {model}")
            print(f"History messages: {len(getattr(agent, '_history', []))}")
            print(f"PowerShell: {'ON' if ALLOW_POWERSHELL else 'OFF'} | fetch_url: {'ON' if ALLOW_FETCH_URL else 'OFF'} | browser: {'ON' if ALLOW_OPEN_BROWSER else 'OFF'} | smtp: {'ON' if ALLOW_SMTP_SEND else 'OFF'}")
            continue
        
        # History
        if line_lower == "/history":
            hist = getattr(agent, "_history", [])
            print(f"Messages in memory: {len(hist)}")
            for msg in hist[-6:]:
                role = msg.get("role", "?")
                content = str(msg.get("content", "")).replace("\n", " ").strip()
                print(f"- {role}: {content[:140]}")
            continue
        
        # Memory
        if line_lower.startswith("/memory"):
            parts = line.split(maxsplit=1)
            tag = parts[1].strip() if len(parts) > 1 else None
            out = agent._ctx.read_memory_notes(tag=tag)
            print(_parse_memory(out))
            continue
        
        # Web search
        if line_lower.startswith("/search "):
            payload = line[len("/search "):].strip()
            if not payload:
                print("Usage: /search <query> [max]")
                continue
            
            query = payload
            max_results = 6
            if " " in payload:
                left, right = payload.rsplit(" ", 1)
                if right.isdigit():
                    query = left.strip()
                    max_results = max(1, min(int(right), 20))
            
            print(_pretty_json(agent._ctx.web_search(query, max_results=max_results)))
            continue
        
        # News search
        if line_lower.startswith("/news "):
            payload = line[len("/news "):].strip()
            if not payload:
                print("Usage: /news <query> [max]")
                continue
            
            query = payload
            max_results = 5
            if " " in payload:
                left, right = payload.rsplit(" ", 1)
                if right.isdigit():
                    command = left.strip()
                    max_results = max(1, min(int(right), 20))
            
            print(_pretty_json(agent._ctx.news_search(query, max_results=max_results)))
            continue
        
        # Add note
        if line_lower.startswith("/note "):
            payload = line[len("/note "):].strip()
            if not payload or " " not in payload:
                print("Usage: /note <tag> <text>")
                continue
            
            tag, note = payload.split(" ", 1)
            print(_pretty_json(agent._ctx.append_memory_note(note, tag=tag)))
            continue
        
        # Change model
        if line_lower.startswith("/model "):
            new_model = line[len("/model "):].strip()
            if not new_model:
                print("Usage: /model <name>")
                continue
            
            setattr(agent, "_model", new_model)
            print(f"✅ Model updated: {new_model}")
            continue
        
        # Export session
        if line_lower == "/export":
            path = _export_session(agent, title="session")
            print(f"✅ Exported: {path}")
            continue
        
        # Autopilot
        if line_lower.startswith("/autopilot"):
            parts = line.split(maxsplit=2)
            minutes = DEFAULT_AUTOPILOT_MINUTES
            objective = ""
            
            if len(parts) == 2:
                if parts[1].isdigit():
                    minutes = _parse_int(parts[1], DEFAULT_AUTOPILOT_MINUTES)
                else:
                    objective = parts[1]
            elif len(parts) >= 3:
                minutes = _parse_int(parts[1], DEFAULT_AUTOPILOT_MINUTES) if parts[1].isdigit() else DEFAULT_AUTOPILOT_MINUTES
                objective = parts[2] if parts[1].isdigit() else " ".join(parts[1:])
            
            if not objective:
                objective = input("Objective > ").strip()
            
            if not objective:
                print("❌ Objective required.")
                continue
            
            _run_autopilot(agent, objective, minutes)
            continue
        
        # Multiline input
        if line_lower in ("/paste", "/long", "/multiline"):
            try:
                line = _read_multiline()
            except (EOFError, KeyboardInterrupt):
                print("\n❌ Multiline cancelled.")
                continue
            
            if not line:
                print("(Empty message ignored)")
                continue
        
        # Regular message - run agent
        try:
            reply = agent.run_turn(line)
        except Exception as e:
            reply = f"❌ Error: {e}"
        
        print()
        print("🤖 >", reply)
        print()


if __name__ == "__main__":
    main()
