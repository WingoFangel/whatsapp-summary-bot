
@echo off
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"
python -m processor.run --input "_chat.txt" --out "digest_ru.txt" --config "config\config.yaml"
pause
