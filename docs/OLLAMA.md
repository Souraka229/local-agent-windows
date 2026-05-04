# 🧠 Guide Ollama Complet - SAISA Local AI

> Tout pour utiliser SAISA en mode 100% local avec Ollama

---

## 📋 Table des Matières

1. [Pourquoi Ollama ?](#1---pourquoi-ollama-)
2. [Installation](#2---installation)
3. [Configuration](#3---configuration)
4. [Modèles](#4---modèles)
5. [Personnalisation Avancée](#5---personnalisation-avancée)
6. [API Locale](#6---api-locale)
7. [Dépannage](#7---dépannage)
8. [FAQ](#8---faq)

---

## 1. Pourquoi Ollama ?

| Avantage | Description |
|---------|-----------|
| 🔒 **Confidentialité** | Données locales uniquement |
| 💰 **Gratuit** | Pas d'API payante |
| 🚀 **Rapide** | Après premier chargement |
| ✈️ **Hors ligne** | Fonctionne sans Internet |
| 🔧 **Personnalisable** | Fine-tuning |

---

## 2. Installation

### Windows PowerShell
```powershell
irm https://ollama.com/install.ps1 | iex
```

### Vérifier
```powershell
ollama --version
```

---

## 3. Configuration .env

```env
AGENT_BACKEND=ollama
OLLAMA_MODEL=llama3.2
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_TEMPERATURE=0.7
OLLAMA_NUM_CTX=8192
```

---

## 4. Modèles Recommandés

| Modèle | Taille | RAM | Description |
|--------|-------|-----|------------|
| `llama3.2` | 2GB | 4GB | Recommandé |
| `llama3.2:1b` | 1GB | 2GB | PC limités |
| `phi3` | 2GB | 4GB | Microsoft |
| `mistral` | 4GB | 8GB | Équilibre |
| `gemma:2b` | 1GB | 2GB | Google |
| `codellama` | 3GB | 6GB | Code |

### Commandes
```powershell
ollama pull llama3.2    # Télécharger
ollama list               # Liste
ollama rm llama3.2        # Supprimer
```

---

## 5. Personnalisation Avancée

### Changer le modèle
```env
OLLAMA_MODEL=mistral
```

### Température ( créativié )
```env
OLLAMA_TEMPERATURE=0.9   # Plus créatif
OLLAMA_TEMPERATURE=0.3   # Plus précis
```

### Contexte ( mémoire )
```env
OLLAMA_NUM_CTX=4096     # Petit
OLLAMA_NUM_CTX=16384    # Grand
```

---

## 6. API Locale

### Démarrer le serveur
```powershell
ollama serve
```

### Tester l'API
```powershell
curl http://localhost:11434/api/tags -s | ConvertFrom-Json
```

### Avec Python
```python
import httpx

response = httpx.post(
    "http://localhost:11434/api/chat",
    json={
        "model": "llama3.2",
        "messages": [{"role": "user", "content": "hello"}],
        "stream": False
    }
)
print(response.json())
```

---

## 7. Dépannage

### "command not found"
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

### Trop lent
- Modèle plus petit
- Ou utiliser Groq

### Out of Memory
- Fermer apps
- Modèle plus petit

---

## 8. FAQ

### Ollama gratuit ? ✅ Oui

### Avec AMD GPU ? ✅ ROCm

### Plusieurs modèles ? ✅ `%LOCALAPPDATA%\Ollama\models`

### Libérer mémoire ?
```powershell
ollama stop
```

### Ollama vs Groq

| | Ollama | Groq |
|--------|------|
| Prix | Gratuit | Payant |
| Latence | Variable | Ultra-rapide |
| Vie privée | 100% | Cloud |

---

## ✅ Checklist

- [ ] Ollama installé
- [ ] `ollama --version` OK
- [ ] Modèle téléchargé
- [ ] Service démarré
- [ ] `.env` configuré
- [ ] `python main.py` fonctionne

---

**🎉 Bon voyage avec SAISA local !**

<div align="center">

Fait avec ❤️

</div>
