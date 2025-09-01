#!/usr/bin/env bash
cd "$(dirname "$0")"
python3 -m processor.run --input "_chat.txt" --out "digest_ru.txt" --config "config/config.yaml"
