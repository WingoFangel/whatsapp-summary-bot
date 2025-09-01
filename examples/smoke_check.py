# examples/smoke_check.py
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ok = True

# 1) config template exists
template_path = ROOT / "config" / "config_template.yaml"
if template_path.exists():
    print("✅ Структура ок. Найден config/config_template.yaml.")
else:
    print("❌ Не найден config/config_template.yaml.")
    ok = False

# 2) .gitignore has required sections
gi_path = ROOT / ".gitignore"
required_markers = [
    "Logs & temp".lower(),
    "Secrets & tokens".lower(),
    "Exports (чаты/медиа)".lower(),
    "Configs (разрешаем только шаблоны)".lower(),
]
if gi_path.exists():
    content = gi_path.read_text(encoding="utf-8").lower()
    if all(marker in content for marker in required_markers):
        print("✅ .gitignore содержит правила для логов, токенов, экспортов чатов и медиа.")
    else:
        print("❌ .gitignore не содержит всех обязательных правил.")
        ok = False
else:
    print("❌ Не найден .gitignore.")
    ok = False

if ok:
    print("🎉 Smoke‑test пройден. Можно двигаться к M1+.")
else:
    print("⚠️  Исправьте замечания выше и запустите снова.")
