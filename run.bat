@echo off
REM ============================================
REM SAISA - Super AI Agent Launcher
REM ============================================

echo.
echo ========================================
echo   SAISA - Super AI Self-Autonomous
echo ========================================
echo.

REM Configuration
set AGENT_BACKEND=ollama
set OLLAMA_MODEL=gemma:2b
set OLLAMA_TEMPERATURE=0.3

echo [1/3] Verification que Python est installe...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Python n'est pas installe!
    pause
    exit /b 1
)
echo OK: Python detecte

echo.
echo [2/3] Verification qu'Ollama est installe...
ollama --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Ollama n'est pas installe!
    echo Telecharge-le sur: https://ollama.com
    pause
    exit /b 1
)
echo OK: Ollama detecte

echo.
echo [3/3] Verification des modeles Ollama...
echo Modeles disponibles:
ollama list
echo.

REM Verifie que le modele existe
ollama list | findstr /I "%OLLAMA_MODEL%" >nul
if errorlevel 1 (
    echo ATTENTION: Le modele %OLLAMA_MODEL% n'est pas installe!
    echo Installation en cours...
    ollama pull %OLLAMA_MODEL%
)

echo.
echo ========================================
echo   DEMARRAGE DE SAISA
echo ========================================
echo Backend: %AGENT_BACKEND%
echo Modele: %OLLAMA_MODEL%
echo Temperature: %OLLAMA_TEMPERATURE%
echo.
echo Tapes tes commandes dans la fenetre!
echo Pour quitter: /quit
echo.
echo ========================================
echo.

REM Lance l'agent
python main.py

pause