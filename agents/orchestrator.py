"""
AGENT ORCHESTRATOR
================
Coordinates specialized sub-agents, each wired to real ToolContext tools.

Agents:
  - code     → write_file + run_powershell (generate and execute code)
  - browser  → web_search + fetch_url + open_browser_url  
  - terminal → run_powershell (direct shell commands)
  - git      → run_git (git operations)
  - docker   → docker_ps + docker_exec
  - test     → run_powershell (pytest, unittest, node test...)
  - fix      → run_powershell + write_file (read error, fix, re-run)
  - crud     → write_file / read_file / delete_file / list_dir
"""

from __future__ import annotations

import json
from typing import Any


class AgentOrchestrator:
    """Orchestrates specialized sub-agents, each calling ToolContext methods."""

    def __init__(self, cerebrum, tool_context):
        self.cerebrum = cerebrum
        self.tool_context = tool_context
        self.agents: dict[str, "BaseAgent"] = {}
        self._register_agents()

    def _register_agents(self):
        tc = self.tool_context
        self.agents = {
            "code": CodeAgent(tc),
            "browser": BrowserAgent(tc),
            "terminal": TerminalAgent(tc),
            "git": GitAgent(tc),
            "docker": DockerAgent(tc),
            "test": TestAgent(tc),
            "fix": FixAgent(tc),
            "crud": CrudAgent(tc),
            # aliases
            "powershell": TerminalAgent(tc),
            "web": BrowserAgent(tc),
            "file": CrudAgent(tc),
        }

    def execute_step(self, step: dict[str, Any]) -> str:
        action = step.get("action", "")
        detail = step.get("detail", "")
        tool = step.get("tool", "terminal").lower()

        agent = self.agents.get(tool, self.agents["terminal"])
        try:
            return agent.execute(action, detail)
        except Exception as exc:
            return f"ERROR in agent {tool}: {exc}"

    def create_plan(self, task: str) -> list[dict[str, Any]]:
        """Create execution plan via Cerebrum."""
        result = self.cerebrum.analyze_task(task)
        
        if "error" in result:
            print(f"Plan error: {result.get('error')}")
            return []
        
        steps = result.get("steps", result.get("plan", []))
        if isinstance(steps, list):
            return steps
        
        return [{"action": task, "detail": str(steps), "tool": "terminal"}]

    def execute_task(self, task: str) -> str:
        """Break down task via Cerebrum then execute each step."""
        plan = self.create_plan(task)

        if "error" in plan:
            return f"Planning failed: {plan['error']}"

        steps = plan if isinstance(plan, list) else []
        if not steps:
            return "No steps generated for this task."

        print(f"\nPlan: {task}")
        print(f"Steps: {len(steps)}")

        results = []
        for step in steps:
            order = step.get("order", len(results) + 1)
            action = step.get("action", "?")
            detail = step.get("detail", "")

            print(f"Step {order}: {action}")

            result = self.execute_step(step)
            results.append({"step": order, "action": action, "result": result})

            ok = self._is_success(result)
            print(f"  {'OK' if ok else 'FAIL'}: {str(result)[:100]}")

            if not ok and step.get("critical", False):
                print(f"\nCritical step failed. Stopping.")
                break

        return self._format_results(results)

    def _is_success(self, result: str) -> bool:
        if not result:
            return False
        try:
            data = json.loads(result)
            if "error" in data and data["error"]:
                return False
            if data.get("exit_code", 0) != 0:
                return False
        except (json.JSONDecodeError, TypeError):
            pass
        fail_words = ["error", "failed", "failure", "exception", "traceback", "not found", "denied"]
        return not any(w in result.lower() for w in fail_words)

    def _format_results(self, results: list[dict]) -> str:
        lines = ["# Execution Results\n"]
        ok_count = 0
        for r in results:
            ok = self._is_success(str(r.get("result", "")))
            if ok:
                ok_count += 1
            lines.append(f"{'OK' if ok else 'FAIL'} Step {r['step']}: {r['action']}")
        lines.append(f"\n{ok_count}/{len(results)} steps completed.")
        return "\n".join(lines)


# =============================================================================
# BASE AGENT
# =============================================================================

class BaseAgent:
    def __init__(self, tool_context):
        self.tc = tool_context

    def execute(self, action: str, detail: str) -> str:
        raise NotImplementedError


# =============================================================================
# CODE AGENT - generate + execute code
# =============================================================================

class CodeAgent(BaseAgent):
    """write_file() to create source, run_powershell() to execute."""

    LANG_MAP = {
        "python": ("script.py", "python script.py"),
        "py": ("script.py", "python script.py"),
        "node": ("script.js", "node script.js"),
        "js": ("script.js", "node script.js"),
        "bash": ("script.sh", "bash script.sh"),
    }

    def execute(self, action: str, detail: str) -> str:
        a = action.lower()

        # Write + execute
        if any(k in a for k in ("create", "write", "generate", "make")):
            filename, run_cmd = "code.txt", None
            for lang, (fname, cmd) in self.LANG_MAP.items():
                if lang in a:
                    filename, run_cmd = fname, cmd
                    break

            write_res = self.tc.write_file(filename, detail)

            if run_cmd:
                exec_res = self.tc.run_powershell(run_cmd)
                return f"File: {write_res}\nExec: {exec_res}"
            return f"File: {write_res}"

        # Direct execution
        if any(k in a for k in ("run", "exec", "execute", "start", "launch")):
            return self.tc.run_powershell(detail)

        return self.tc.run_powershell(detail)


# =============================================================================
# BROWSER AGENT - internet
# =============================================================================

class BrowserAgent(BaseAgent):
    """web_search(), fetch_url(), open_browser_url()."""

    def execute(self, action: str, detail: str) -> str:
        a = action.lower()

        if any(k in a for k in ("search", "find", "look")):
            return self.tc.web_search(detail)

        if any(k in a for k in ("fetch", "scrape", "download", "read_url")):
            return self.tc.fetch_url(detail)

        if any(k in a for k in ("open", "navigate", "goto")):
            return self.tc.open_browser_url(detail)

        # Auto-detect
        if detail.startswith("http"):
            return self.tc.fetch_url(detail)
        return self.tc.web_search(detail)


# =============================================================================
# TERMINAL AGENT - shell
# =============================================================================

class TerminalAgent(BaseAgent):
    """run_powershell() with raw command."""

    def execute(self, action: str, detail: str) -> str:
        cmd = detail if detail else action
        return self.tc.run_powershell(cmd)


# =============================================================================
# GIT AGENT
# =============================================================================

class GitAgent(BaseAgent):
    """run_git() for all git operations."""

    def execute(self, action: str, detail: str) -> str:
        a = action.lower()

        if detail.startswith("git "):
            return self.tc.run_git(detail[4:].strip())

        if "init" in a:
            return self.tc.run_git("init")
        if "status" in a:
            return self.tc.run_git("status")
        if "log" in a:
            return self.tc.run_git("log --oneline -10")
        if "add" in a:
            return self.tc.run_git(f"add {detail}" if detail else "add -A")
        if "commit" in a:
            msg = detail or "auto-commit by SAISA"
            return self.tc.run_git(f'commit -m "{msg}"')
        if "push" in a:
            return self.tc.run_git(f"push {detail}".strip())
        if "pull" in a:
            return self.tc.run_git(f"pull {detail}".strip())
        if "clone" in a:
            return self.tc.run_git(f"clone {detail}")
        if "branch" in a:
            return self.tc.run_git(f"branch {detail}".strip())
        if "checkout" in a:
            return self.tc.run_git(f"checkout {detail}")

        return self.tc.run_git(detail.strip() or action)


# =============================================================================
# DOCKER AGENT
# =============================================================================

class DockerAgent(BaseAgent):
    """docker_ps(), docker_exec(), run_powershell for rest."""

    def execute(self, action: str, detail: str) -> str:
        a = action.lower()

        if any(k in a for k in ("ps", "list", "containers")):
            return self.tc.docker_ps(all_containers=True)

        if any(k in a for k in ("exec", "run_in")):
            parts = detail.split("|", 1)
            if len(parts) == 2:
                return self.tc.docker_exec(parts[0].strip(), parts[1].strip())

        cmd = f"docker {detail}".strip() if detail else f"docker {action}"
        return self.tc.run_powershell(cmd)


# =============================================================================
# TEST AGENT
# =============================================================================

class TestAgent(BaseAgent):
    """pytest, jest, mocha via run_powershell."""

    def execute(self, action: str, detail: str) -> str:
        a = action.lower()

        if "pytest" in a or "python" in a:
            cmd = detail or "pytest -v"
        elif "jest" in a or "node" in a:
            cmd = detail or "npx jest"
        elif "mocha" in a:
            cmd = detail or "npx mocha"
        else:
            cmd = detail or action

        return self.tc.run_powershell(cmd)


# =============================================================================
# FIX AGENT
# =============================================================================

class FixAgent(BaseAgent):
    """Read buggy file, log error for learning."""

    def execute(self, action: str, detail: str) -> str:
        parts = detail.split("|", 1)
        filepath = parts[0].strip()
        error_desc = parts[1].strip() if len(parts) > 1 else "unspecified error"

        file_content = self.tc.read_file(filepath)
        try:
            source_code = json.loads(file_content).get("content", "")
        except (json.JSONDecodeError, TypeError):
            source_code = file_content

        if not source_code:
            return f"Cannot read: {filepath}"

        self.tc.append_memory_note(
            f"ERROR in {filepath}: {error_desc}\nCode:\n{source_code[:400]}",
            tag="error"
        )

        return f"Fix requested: {filepath}\nLogged for learning."


# =============================================================================
# CRUD AGENT - file operations
# =============================================================================

class CrudAgent(BaseAgent):
    """write_file, read_file, delete_file, list_dir."""

    def execute(self, action: str, detail: str) -> str:
        a = action.lower()

        # CREATE / UPDATE
        if any(k in a for k in ("create", "write", "update", "save")):
            parts = detail.split("|", 1)
            if len(parts) == 2:
                path, content = parts[0].strip(), parts[1]
            else:
                lines = detail.split("\n", 1)
                path = lines[0].strip()
                content = lines[1] if len(lines) > 1 else ""
            return self.tc.write_file(path, content)

        # READ
        if any(k in a for k in ("read", "get", "open", "show", "cat")):
            return self.tc.read_file(detail.strip())

        # LIST
        if any(k in a for k in ("list", "ls", "dir")):
            return self.tc.list_dir(detail.strip() or ".")

        # DELETE
        if any(k in a for k in ("delete", "remove", "rm")):
            return self.tc.delete_file(detail.strip())

        return self.tc.list_dir(detail.strip() or ".")
