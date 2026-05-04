"""
SAISA - Super AI Self-Autonomous Agent
===================================
Main CLI interface for terminal.

Usage:
    python -m api.cli "create a login system"
    python -m api.cli --stats
    python -m api.cli --interactive
"""

from __future__ import annotations

import sys
from pathlib import Path

# Add path for local imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from brain.cerebrum import Cerebrum
from agents.orchestrator import AgentOrchestrator
from tools.tool_layer import ToolLayer
from memory.semantic.memory_system import MemorySystem
from local_agent.config import WORKSPACE_ROOT, OLLAMA_MODEL


class SAISA:
    """
    Super AI Self-Autonomous Agent - The ultimate local AI.
    
    Combines:
    - Cerebrum (brain)
    - Orchestrator (project manager)
    - Tool Layer (tools)
    - Memory (learning)
    """
    
    def __init__(self):
        print("🚀 Initializing SAISA...")
        
        # Initialize components
        self.tool_layer = ToolLayer(WORKSPACE_ROOT)
        self.cerebrum = Cerebrum()
        self.orchestrator = AgentOrchestrator(self.cerebrum, self.tool_layer)
        self.memory = MemorySystem()
        
        print(f"   🧠 Cerebrum: {OLLAMA_MODEL}")
        print(f"   📁 Workspace: {WORKSPACE_ROOT}")
        print(f"   💾 Memory: {self.memory.db_path}")
        print("   ✅ Ready!\n")
    
    
    def run(self, task: str) -> str:
        """Execute a task.
        
        Args:
            task: The task description.
            
        Returns:
            The task result or error message.
        """
        print(f"📝 Task: {task}\n")
        
        try:
            # Execute with feedback loop
            result = self.orchestrator.execute_task(task)
            
            # Learn from result
            self.memory.analyze_and_learn(
                user_input=task,
                agent_response=result,
                tools_used=[],
                success="error" not in result.lower()
            )
            
            return result
            
        except Exception as e:
            error_msg = f"❌ Error: {str(e)}"
            self.memory.learn_from_error(str(e), "Contact developer")
            return error_msg
    
    def stats(self) -> dict:
        """Get statistics."""
        return self.memory.get_stats()
    
    def close(self):
        """Clean up resources."""
        self.cerebrum.close()


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("""
🧠 SAISA - Super AI Self-Autonomous
===================================

Usage:
    python -m api.cli "your task"
    python -m api.cli --stats
    python -m api.cli --interactive

Examples:
    python -m api.cli "create hello.py"
    python -m api.cli "open google.com"
    python -m api.cli "test localhost:3000"
""")
        sys.exit(1)
    
    arg = sys.argv[1]
    
    if arg == "--stats":
        # Show stats
        from memory.semantic.memory_system import MemorySystem
        mem = MemorySystem()
        stats = mem.get_stats()
        print("\n📊 Learning Statistics:")
        print(f"   Conversations: {stats['conversations']}")
        print(f"   Errors learned: {stats['errors_learned']}")
        print(f"   Errors solved: {stats['errors_solved']}")
        print(f"   Skills: {stats['skills_acquired']}")
        print(f"   Tasks completed: {stats['tasks_completed']}")
        print(f"   Learning score: {stats['learning_score']}/100")
        return
    
    if arg == "--interactive":
        # Interactive mode
        saisa = SAISA()
        print("Interactive mode. Type 'quit' to exit.\n")
        
        while True:
            try:
                task = input("You> ").strip()
                if task.lower() in ("quit", "exit", "q"):
                    break
                if not task:
                    continue
                
                result = saisa.run(task)
                print(f"\n{result}\n")
                
            except KeyboardInterrupt:
                break
            except EOFError:
                break
        
        saisa.close()
        print("\n👋 Goodbye!")
        return
    
    # Simple execution
    task = " ".join(sys.argv[1:])
    saisa = SAISA()
    result = saisa.run(task)
    print(result)
    saisa.close()


if __name__ == "__main__":
    main()
