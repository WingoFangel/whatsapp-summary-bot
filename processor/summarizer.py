
from dataclasses import dataclass
from typing import List
from datetime import datetime, timedelta
from collections import Counter
from zoneinfo import ZoneInfo

from .whatsapp_parser import Message
from .utils import tokenize

@dataclass
class Summary:
    text: str

def filter_period(messages: List[Message], tz: str):
    tzinfo = ZoneInfo(tz)
    now = datetime.now(tzinfo)
    start = (now - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    end = now
    subset = [m for m in messages if start <= m.dt <= end]
    return subset, start, end

def group_by_keywords(messages: List[Message], top_n: int = 8):
    all_tokens = []
    per_message_tokens = []
    for m in messages:
        if m.is_system: 
            per_message_tokens.append(set()); continue
        toks = set(tokenize(m.text))
        per_message_tokens.append(toks)
        all_tokens.extend(list(toks))
    cnt = Counter(all_tokens)
    labels = [w for w,_ in cnt.most_common(top_n)]
    groups = []
    for w in labels:
        idxs = [i for i,toks in enumerate(per_message_tokens) if w in toks]
        if idxs: groups.append((w, idxs))
    groups.sort(key=lambda x: len(x[1]), reverse=True)
    return groups

def participants_stats(messages: List[Message]):
    c = Counter()
    for m in messages:
        if m.author: c[m.author] += 1
    return c

def pick_quotes(messages: List[Message], idxs: List[int], max_quotes: int = 2):
    out = []
    for i in idxs:
        if messages[i].is_system: continue
        line = messages[i].text.strip().splitlines()[0]
        if len(line) < 6: continue
        author = messages[i].author or "Система"
        out.append(f"— {line} — {author}")
        if len(out) >= max_quotes: break
    return out

def extract_questions(messages: List[Message], max_q: int = 5):
    qs = []
    for m in messages:
        if m.is_system: continue
        line = m.text.strip().splitlines()[0]
        if line.endswith("?"):
            qs.append(f"— {line} — {m.author}")
            if len(qs) >= max_q: break
    return qs

def extract_decisions(messages: List[Message], max_items: int = 5):
    keys = ["решили","итог","договорились","вывод","резюме"]
    res = []
    for m in messages:
        if m.is_system: continue
        low = m.text.lower()
        if any(k in low for k in keys):
            one = m.text.strip().splitlines()[0]
            res.append(f"— {one} — {m.author}")
            if len(res) >= max_items: break
    return res

def format_period(start: datetime, end: datetime) -> str:
    months = ["янв","фев","мар","апр","мая","июн","июл","авг","сен","окт","ноя","дек"]
    def fmt(d: datetime): return f"{d.day} {months[d.month-1]}"
    return fmt(start) if start.date()==end.date() else f"{fmt(start)} — {fmt(end)}"

def build_summary_ru(messages: List[Message], tz: str) -> Summary:
    subset, start, end = filter_period(messages, tz)
    if not subset:
        return Summary(text=(
            "🗓 За вчера/сегодня сообщений не найдено.\n"
            "Проверьте, что вы экспортировали чат без медиа и положили файл «_chat.txt» рядом со скриптом."
        ))
    c_part = participants_stats(subset)
    participants = ", ".join([f"{name} ({cnt})" for name,cnt in c_part.most_common(5)])
    groups = group_by_keywords(subset, top_n=8)
    lines = []
    lines.append(f"🗓 Период: {format_period(start, end)}")
    lines.append(f"Сообщений: {len(subset)} • Участников: {len(c_part)}")
    if participants: lines.append(f"Топ активность: {participants}")
    lines.append("")
    if groups:
        lines.append("Темы дня:")
        for i,(label, idxs) in enumerate(groups[:5], start=1):
            quotes = pick_quotes(subset, idxs, max_quotes=2)
            group_part = Counter([subset[j].author for j in idxs if subset[j].author])
            ppl = ", ".join([n for n,_ in group_part.most_common(3)])
            lines.append(f"{i}) {label} — {len(idxs)} сообщ.; участники: {ppl if ppl else '—'}")
            lines.extend(quotes); lines.append("")
    else:
        lines.append("Темы дня: —"); lines.append("")
    qs = extract_questions(subset); 
    if qs: lines.append("Вопросы:"); lines.extend(qs); lines.append("")
    ds = extract_decisions(subset);
    if ds: lines.append("Итоги/решения:"); lines.extend(ds); lines.append("")
    lines.append("⨯ Автодайджест (M1)")
    return Summary(text="\n".join(lines))
