"""
SAISA Web Interface
Graphical interface in the browser!
Run: python web.py
Then open: http://localhost:7860
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
You can search the web, create files, run commands, etc.
Respond clearly and concisely."""


def chat(message: str, history: Optional[list] = None) -> str:
    """Send a message to the AI.
    
    Args:
        message: The user message.
        history: Previous conversation history.
        
    Returns:
        AI response or error message.
    """
    client = httpx.Client(timeout=TIMEOUT)

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    # Add history
    if history:
        for user_msg, bot_msg in history:
            messages.append({"role": "user", "content": user_msg})
            messages.append({"role": "assistant", "content": bot_msg})

    messages.append({"role": "user", "content": message})

    try:
        response = client.post(
            f"{OLLAMA_URL}/api/chat",
            json={"model": MODEL, "messages": messages, "stream": False}
        )

        if response.status_code != 200:
            return f"❌ Error: {response.status_code}"

        return response.json()["message"]["content"]
    except Exception as e:
        return f"❌ Error: {e}"
    finally:
        client.close()


# ==== WEB INTERFACE with Flask ====
try:
    from flask import Flask, jsonify, render_template_string, request
    HAS_FLASK = True
except ImportError:
    HAS_FLASK = False
    print("⚠️ Flask not installed. Install with: pip install flask")


def create_app() -> Flask:
    """Create Flask application."""
    app = Flask(__name__)

    HTML_TEMPLATE = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>🧠 SAISA - Web Interface</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * { box-sizing: border-box; }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background: #1a1a2e;
                color: #eee;
            }
            h1 { text-align: center; color: #00ff88; }
            #chat {
                height: 400px;
                overflow-y: auto;
                border: 1px solid #333;
                border-radius: 8px;
                padding: 15px;
                margin-bottom: 15px;
                background: #16213e;
            }
            .message { margin: 10px 0; padding: 10px; border-radius: 8px; }
            .user { background: #0f3460; text-align: right; }
            .assistant { background: #1a1a2e; }
            input, button {
                padding: 12px;
                font-size: 16px;
                border: none;
                border-radius: 8px;
            }
            input { flex: 1; background: #16213e; color: #eee; }
            button { background: #00ff88; color: #1a1a2e; cursor: pointer; font-weight: bold; }
            button:hover { background: #00cc6a; }
            #controls { display: flex; gap: 10px; }
        </style>
    </head>
    <body>
        <h1>🧠 SAISA - Web Interface</h1>
        <div id="chat"></div>
        <div id="controls">
            <input type="text" id="message" placeholder="Type your message..." onkeypress="handleKey(event)">
            <button onclick="sendMessage()">Send</button>
            <button onclick="clearChat()" style="background: #e94560;">Clear</button>
        </div>
        
        <script>
            let history = [];
            
            function addMessage(role, text) {
                const chat = document.getElementById('chat');
                const div = document.createElement('div');
                div.className = 'message ' + role;
                div.textContent = (role === 'user' ? '👤 ' : '🤖 ') + text;
                chat.appendChild(div);
                chat.scrollTop = chat.scrollHeight;
            }
            
            function handleKey(event) {
                if (event.key === 'Enter') sendMessage();
            }
            
            async function sendMessage() {
                const input = document.getElementById('message');
                const text = input.value.trim();
                if (!text) return;
                
                addMessage('user', text);
                input.value = '';
                
                try {
                    const response = await fetch('/api/chat', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({message: text, history: history})
                    });
                    const result = await response.json();
                    history.push([text, result.response]);
                    addMessage('assistant', result.response);
                } catch (e) {
                    addMessage('assistant', '❌ Error: ' + e);
                }
            }
            
            function clearChat() {
                history = [];
                document.getElementById('chat').innerHTML = '';
            }
        </script>
    </body>
    </html>
    """

    @app.route("/")
    def index():
        return render_template_string(HTML_TEMPLATE)

    @app.route("/api/chat", methods=["POST"])
    def api_chat():
        data = request.get_json()
        message = data.get("message", "")
        history = data.get("history", [])

        response = chat(message, history)
        return jsonify({"response": response})

    return app


def main():
    """Main entry point."""
    if not HAS_FLASK:
        print("❌ Flask not installed!")
        print("Install with: pip install flask")
        sys.exit(1)

    app = create_app()
    print("=" * 50)
    print("🧠 SAISA Web Interface")
    print("=" * 50)
    print("🌐 Open: http://localhost:7860")
    print("Press Ctrl+C to stop")
    print()

    app.run(host="0.0.0.0", port=7860, debug=False)


if __name__ == "__main__":
    main()
