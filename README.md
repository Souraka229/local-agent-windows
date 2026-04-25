# SAISA - Super AI Self-Autonomous Agent

## Description

SAISA (Super AI Self-Autonomous) est un agent IA 100% local ultra-puissant qui fonctionne dans ton terminal.

### Objectif: 1M+ etoiles GitHub

## Fonctionnalites Principales

| Feature | Description |
|---------|-------------|
| IA Locale | Gemma 4 via Ollama - pas de cloud, pas de latence |
| Autonome | Fonctionne sans supervision avec /autopilot |
| Browser Automation | Controle Chrome avec Playwright |
| Docker | Gestion de conteneurs |
| Git integre | Commandes Git directes |
| Memoire Apprenante | SQLite qui apprend de ses erreurs |
| Sandbox securisee | Isolation Docker |
| Skills | Systeme extensible de plugins |

## Architecture

```
local-agent-windows/
├── brain/              # Cerebrum (Gemma 4 - Planification)
├── agents/             # Orchestrateur (7 agents specialises)
├── tools/              # Tool Layer + Browser (Playwright)
├── memory/             # SQLite Learning System
├── sandbox/            # Docker Execution Sandbox
├── api/                # Interface CLI
└── main.py             # CLI Original
```

## Installation Rapide

```bash
# Clone le repo
git clone https://github.com/Souraka229/local-agent-windows.git
cd local-agent-windows

# Installe les dependances
pip install -r requirements.txt

# Configure (optionnel)
cp .env.example .env

# Lance Ollama avec gemma4
ollama run gemma4:latest

# Demarre l'agent
python main.py
```

## Utilisation

```bash
# Mode interactif
python -m api.cli --interactive

# Mode autopilot
python main.py
/autopilot 60 creer un projet Python

# Voir les stats
python -m api.cli --stats
```

## Configuration

Cree un fichier .env:

```env
AGENT_BACKEND=ollama
OLLAMA_MODEL=gemma4:latest
ALLOW_GIT=1
ALLOW_DOCKER=1
ALLOW_SYSTEM_MONITOR=1
ALLOW_POWERSHELL=1
ALLOW_OPEN_BROWSER=1
AUTONOMOUS_MODE=1
LEARNING_MODE=1
AGENT_NAME=SAISA
```

## Comment l'IA Apprend

1. Memoire SQLite - Sauvegarde chaque conversation
2. Analyse des erreurs - Apprend de ses failures
3. Competences acquises - Memorise les taches reussies
4. Score d'apprentissage - Evalue sa progression

## License

Ce projet est sous license MIT - voir le fichier LICENSE pour les details.

## Avertissement

Ce logiciel est fourni "tel quel", sans garantie d'aucune sorte.

---

⭐ Si ce projet t'aide, mets une etoile!

Fait avec amour par @Souraka229
