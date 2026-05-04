# 🧠 Guide Complet - SAISA avec Ollama (Local AI)

> Tout ce que vous devez savoir pour utiliser SAISA en mode 100% local avec Ollama

---

## 📋 Table des Matières

1. [Pourquoi Ollama ?](#1---pourquoi-ollama-)
2. [Installation d'Ollama](#2---installation-dollama)
3. [Configuration initiale](#3---configuration-initiale)
4. [Téléchargement des modèles](#4---téléchargement-des-modèles)
5. [Démarrage du service](#5---démarrage-du-service)
6. [Configuration de SAISA](#6---configuration-de-saisa)
7. [Premiers pas](#7---premiers-pas)
8. [Personnalisation des modèles](#8---personnalisation-des-modèles)
9. [Dépannage](#9---dépannage)
10. [FAQ](#10---faq)

---

## 1. Pourquoi Ollama ?

| Avantage | Description |
|----------|-------------|
| 🔒 **Confidentialité** | Vos données ne quittent jamais votre machine |
| 💰 **Gratuit** | Pas d'abonnement API |
| 🚀 **Rapide** | Pas de latence réseau après premier chargement |
| 🔧 **Personnalisable** | Modèles fine-tunables |
| ✈️ **Hors ligne** | Fonctionne sans Internet |

**Inconvénients:**
- Requiert un PC puissant (16GB RAM minimum)
- Premier lancement plus lent
- Sans GPU = plus lent

---

## 2. Installation d'Ollama

### Option A: Automatique (Recommandé)

**PowerShell (Administrateur):**
```powershell
irm https://ollama.com/install.ps1 | iex
```

### Option B: Manuelle

1. Téléchargez depuis : https://ollama.com/download/windows
2. Exécutez le fichier `.exe`
3. Suivez les instructions

### Vérifier l'installation

```powershell
ollama --version
```

Devrait afficher :
```
ollama version 0.5.6
```

---

## 3. Configuration Initiale

### Ajouter au PATH (si nécessaire)

**PowerShell:**
```powershell
$env:PATH += ";$env:LOCALAPPDATA\Ollama"
```

**Permanent:**
```powershell
[System.Environment]::SetEnvironmentVariable(
    "PATH",
    [System.Environment]::GetEnvironmentVariable("PATH", "Machine") + ";$env:LOCALAPPDATA\Ollama",
    "Machine"
)
```

### Redémarrer le terminal

Fermez et rouvrez votre terminal.

---

## 4. Téléchargement des Modèles

### Modèles recommandés

| Modèle | Taille | VRAM | Description |
|--------|--------|------|-------------|
| `llama3.2` | 2GB | 4GB | **Recommandé** |
| `llama3.2:1b` | 1GB | 2GB | Pour PC limités |
| `phi3` | 2GB | 4GB | Microsoft |
| `mistral` | 4GB | 8GB |Excellent équilibre |
| `gemma:2b` | 1GB | 2GB | Google |
| `codellama` | 3GB | 6GB | Spécialisé code |

### Commandes

**Télécharger:**
```powershell
ollama pull llama3.2
```

**Lister:**
```powershell
ollama list
```

**Supprimer:**
```powershell
ollama rm llama3.2
```

### Quelle taille pour mon PC ?

| Configuration | Modèle |
|----------------|--------|
| 4GB VRAM | `llama3.2:1b`, `phi3` |
| 8GB VRAM | `llama3.2`, `gemma:2b` |
| 16GB+ VRAM | `llama3.2`, `mistral` |

---

## 5. Démarrage du Service

### Mode serveur

```powershell
ollama serve
```

Le service écoute sur `http://localhost:11434`

### Mode interactif (test)

```powershell
ollama run llama3.2
```

Tapez votre message, puis `Ctrl+Shift+C` pour quitter.

---

## 6. Configuration de SAISA

### Fichier .env

Créez `.env` à la racine :

```env
# =============================================================================
# CONFIGURATION SAISA - MODE OLLAMA (LOCAL)
# =============================================================================

# BACKEND
AGENT_BACKEND=ollama

# OLLAMA
OLLAMA_MODEL=llama3.2
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_TEMPERATURE=0.7
OLLAMA_NUM_CTX=8192
OLLAMA_REQUEST_TIMEOUT_SEC=300

# FEATURES
ALLOW_GIT=1
ALLOW_DOCKER=0
ALLOW_POWERSHELL=1
ALLOW_OPEN_BROWSER=0
ALLOW_FETCH_URL=1
ALLOW_SMTP_SEND=0
ALLOW_SYSTEM_MONITOR=1

# AUTONOMOUS MODE
AUTONOMOUS_MODE=1
AGENT_MAX_TOOL_ROUNDS=25
SELF_EVAL_ENABLED=1

# MEMORY
LEARNING_MODE=1
LOCAL_MEMORY_JOURNAL=memory/journal.md

# PERSONNALISATION
AGENT_NAME=SAISA
AGENT_OWNER_NAME=
```

### Variables temporaires PowerShell

```powershell
$env:AGENT_BACKEND = "ollama"
$env:OLLAMA_MODEL = "llama3.2"
python main.py
```

---

## 7. Premiers Pas

### Lancement

```powershell
python main.py
```

### Tests

Tapez :
```
hello
```
puis
```
search python asyncio tutorial
```
puis
```
write hello.py with print("Hello from SAISA!")
```

### Quitter

Tapez : `quit` ou `exit` ou `q`

---

## 8. Personnalisation

### Changer le modèle

Dans `.env`:
```env
OLLAMA_MODEL=mistral
```

### Modèle smaller (tests)

```env
OLLAMA_MODEL=llama3.2:1b
```

---

## 9. Dépannage

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
- Utilsier modèle plus petit dans `.env`
- Ou passer à Groq

### Out of Memory
1. Fermer les autres apps
2. Utiliser modèle plus petit
3. Ajouter RAM

---

## 10. FAQ

### Q: Ollama est-il gratuit ?
**R:** Oui, 100% gratuit.

### Q: Avec AMD GPU ?
**R:** Oui, via ROCm.

### Q: Comment mettre à jour ?
```powershell
ollama update
```

### Q: Plusieurs modèles ?
**R:** Oui, dans `%LOCALAPPDATA%\Ollama\models`

### Q: Libérer mémoire ?
```powershell
ollama stop
```

### Ollama vs Groq ?

| Critère | Ollama | Groq |
|--------|-------|-----|
| Prix | Gratuit | Payant |
| Latence | Variable | Ultra-rapide |
| Vie privée | 100% local | Cloud |
| Setup | Requis | Minimal |

---

## ✅ Checklist

- [ ] Ollama installé
- [ ] `ollama --version` fonctionne
- [ ] Modèle téléchargé (`ollama list`)
- [ ] Service démarré (`ollama serve`)
- [ ] `.env` créé avec `AGENT_BACKEND=ollama`
- [ ] `python main.py` fonctionne

---

<div align="center">

**🎉 Bon voyage avec SAISA en mode local !**

</div>
