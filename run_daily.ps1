
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir
python -m processor.run --input "_chat.txt" --out "digest_ru.txt" --config "config/config.yaml"
Read-Host "Press Enter to exit"
