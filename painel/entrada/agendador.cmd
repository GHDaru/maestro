@echo off
REM ============================================================
REM  Chamado 068 — Agendador Windows do orquestrador (T2-04)
REM  Roda a cada 5 min via Agendador de Tarefas do Windows.
REM  Chama: python -m painel.entrada.orquestrador
REM ============================================================
REM
REM  Instalar (PowerShell, como o usuario):
REM    schtasks /create /tn "Maestro-Chamado068" /tr "C:\caminho\para\este\arquivo.cmd" /sc minute /mo 5
REM
REM  Desinstalar:
REM    schtasks /delete /tn "Maestro-Chamado068" /f
REM
REM  Variaveis de ambiente necessarias:
REM    MAESTRO_DADOS_DIR   — diretorio com entrada.db
REM    MAESTRO_WEBHOOK_URL — URL do webhook n8n (opcional em P2)
REM    MAESTRO_HMAC_SEGREDO — segredo HMAC (opcional em P2)
REM    MAESTRO_CFG_JSON    — config JSON para le_chamados() (opcional)
REM
REM ============================================================

setlocal

REM Diretorio base do projeto (um nivel acima de painel/).
cd /d "%~dp0\.."

REM Python 3.12+ no PATH.
python -m painel.entrada.orquestrador

if errorlevel 1 (
    echo [%date% %time%] Chamado 068: erro %errorlevel% >> "%MAESTRO_DADOS_DIR%\entrada-erro.log"
)

endlocal
