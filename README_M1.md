
# M1 — Быстрый MVP (ручной импорт, авто-дайджест)

Локальный скрипт: читает `_chat.txt`, берёт «вчера/сегодня», группирует темы, формирует RU-дайджест. Опционально отправляет результат в Telegram/Email.

## Быстрый старт
1) Скопируйте папку в корень репозитория.
2) Скопируйте `config/config_template.yaml` → `config/config.yaml`; при необходимости поправьте `timezone`.
3) Положите `_chat.txt` рядом с лаунчером.
4) Запустите:
   - Windows: `run_daily.bat` (или `run_daily.ps1`)
   - macOS/Linux: `chmod +x run_daily.sh && ./run_daily.sh`
5) Результат: `digest_ru.txt`.

Если PowerShell блокирует запуск: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`
