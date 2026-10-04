@echo off
rem Abre o site desta pasta em http://localhost:8081 para conferencia. Feche esta janela para encerrar.
cd /d "%~dp0.."
where python >nul 2>nul
if %errorlevel%==0 (
  start "" http://localhost:8081/
  python -m http.server 8081
  goto :eof
)
where py >nul 2>nul
if %errorlevel%==0 (
  start "" http://localhost:8081/
  py -m http.server 8081
  goto :eof
)
where npx >nul 2>nul
if %errorlevel%==0 (
  start "" http://localhost:8081/
  npx --yes serve -l 8081 .
  goto :eof
)
echo Nao encontrei Python nem Node neste computador.
pause
