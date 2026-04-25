"""
SAISA Simple - Version conversation seulement
Pas d'outils, juste du对话!
"""

import os
import sys

# Configuration
os.environ['AGENT_BACKEND'] = 'ollama'
os.environ['OLLAMA_MODEL'] = 'gemma:2b'

import httpx

OLLAMA_URL = os.environ.get('OLLAMA_BASE_URL', 'http://127.0.0.1:11434')
MODEL = os.environ.get('OLLAMA_MODEL', 'gemma:2b')

def chat(message):
    """Envoie un message et reçoit la réponse"""
    client = httpx.Client(timeout=120.0)
    
    messages = [
        {"role": "system", "content": "Tu es SAISA, un assistant IA utile et aimable en français. Réponds de manière concise et utile."},
        {"role": "user", "content": message}
    ]
    
    response = client.post(
        f"{OLLAMA_URL}/api/chat",
        json={"model": MODEL, "messages": messages, "stream": False}
    )
    
    if response.status_code != 200:
        return f"Erreur: {response.status_code} - {response.text}"
    
    return response.json()['message']['content']

def main():
    print("="*50)
    print("  SAISA - Conversation Simple")
    print("  Modèle: gemma:2b")
    print("="*50)
    print()
    print("Tape 'quit' pour quitter")
    print()
    
    while True:
        try:
            user_input = input("Toi > ").strip()
            
            if user_input.lower() in ('quit', 'exit', 'q', '/quit'):
                print("À bientôt!")
                break
            
            if not user_input:
                continue
            
            print("SAISA > ", end="", flush=True)
            response = chat(user_input)
            print(response)
            print()
            
        except KeyboardInterrupt:
            print("\nÀ bientôt!")
            break
        except Exception as e:
            print(f"Erreur: {e}")

if __name__ == "__main__":
    main()
