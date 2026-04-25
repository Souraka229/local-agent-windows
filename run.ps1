# ============================================
# SAISA - Super AI Agent Launcher (PowerShell)
# ============================================

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  SAISA - Super AI Self-Autonomous" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Configuration
$env:AGENT_BACKEND = "ollama"
$env:OLLAMA_MODEL = "llama3.2"
$env:OLLAMA_TEMPERATURE = "0.3"

Write-Host "[1/3] Verification de Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "OK: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "ERREUR: Python n'est pas installe!" -ForegroundColor Red
    Read-Host "Appuie sur Entree pour quitter"
    exit 1
}

Write-Host ""
Write-Host "[2/3] Verification d'Ollama..." -ForegroundColor Yellow
try {
    $ollamaVersion = ollama --version 2>&1
    Write-Host "OK: $ollamaVersion" -ForegroundColor Green
} catch {
    Write-Host "ERREUR: Ollama n'est pas installe!" -ForegroundColor Red
    Write-Host "Telecharge-le sur: https://ollama.com" -ForegroundColor Yellow
    Read-Host "Appuie sur Entree pour quitter"
    exit 1
}

Write-Host ""
Write-Host "[3/3] Modeles Ollama disponibles:" -ForegroundColor Yellow
ollama list
Write-Host ""

# Verification du modele
$modelExists = ollama list | Select-String -Pattern $env:OLLAMA_MODEL -Quiet
if (-not $modelExists) {
    Write-Host "ATTENTION: Le modele $env:OLLAMA_MODEL n'est pas installe!" -ForegroundColor Yellow
    Write-Host "Installation en cours..." -ForegroundColor Yellow
    ollama pull $env:OLLAMA_MODEL
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  DEMARRAGE DE SAISA" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Backend: $($env:AGENT_BACKEND)" -ForegroundColor White
Write-Host "Modele: $($env:OLLAMA_MODEL)" -ForegroundColor White
Write-Host "Temperature: $($env:OLLAMA_TEMPERATURE)" -ForegroundColor White
Write-Host ""
Write-Host "Tapes tes commandes dans la fenetre!" -ForegroundColor Green
Write-Host "Pour quitter: /quit" -ForegroundColor Gray
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Lance l'agent
python main.py

Read-Host "Appuie sur Entree pour quitter"