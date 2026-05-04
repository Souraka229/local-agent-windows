"""
SAISA Simple - Conversation-only version
No tools, just chat!
"""

import os
import sys
from typing import Optional

import httpx

# Configuration
OLLAMA_URL = os.environ.get("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2")
TIMEOUT = 120.0

SYSTEM_PROMPT = """You are SAISA, an intelligent and helpful AI assistant.

Your creator is Souraka HAMIDA. Be loyal and helpful.
Respond clearly and concisely in French."""


def chat(message: str) -> str:
    """Send a message and get the response.
    
    Args:
        message: The user message to send.
        
    Returns:
        The AI response or error message.
    """
    client = httpx.Client(timeout=TIMEOUT)
    
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": message}
    ]
    
    try:
        response = client.post(
            f"{OLLAMA_URL}/api/chat",
            json={"model": MODEL, "messages": messages, "stream": False}
        )
        
        if response.status_code != 200:
            return f"Error: {response.status_code} - {response.text}"
        
        return response.json()["message"]["content"]
    finally:
        client.close()


def main() -> None:
    """Main entry point."""
    print("=" * 50)
    print("  SAISA - Simple Conversation")
    print(f"  Model: {MODEL}")
    print("=" * 50)
    print()
    print("Type 'quit' to exit")
    print()
    
    while True:
        try:
            user_input = input("You > ").strip()
            
            if user_input.lower() in ("quit", "exit", "q", "/quit"):
                print("👋 Goodbye!")
                break
            
            if not user_input:
                continue
            
            print("SAISA > ", end="", flush=True)
            response = chat(user_input)
            print(response)
            print()
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
