
from dataclasses import dataclass
from typing import List, Optional
import re
from datetime import datetime
from zoneinfo import ZoneInfo

HEADER_BRACKET_RE = re.compile(r"^\[(?P<dt>.+?)\]\s+(?P<author>.*?):\s(?P<text>.*)$")
HEADER_STD_RE = re.compile(r"^(?P<dt>[^-]+?)\s-\s(?P<author>.*?):\s(?P<text>.*)$")
HEADER_SYSTEM_RE = re.compile(r"^(?P<dt>[^-]+?)\s-\s(?P<text>.*)$")

DT_FORMATS = ["%d/%m/%Y, %H:%M","%d/%m/%Y, %H:%M:%S","%d/%m/%y, %H:%M","%d/%m/%y, %H:%M:%S","%d.%m.%Y, %H:%M","%d.%m.%y, %H:%M","%d.%м.%Y, %H:%M:%S","%m/%d/%Y, %I:%M %p","%m/%d/%y, %I:%M %p","%m/%d/%Y, %I:%M:%S %p","%m/%d/%y, %I:%M:%S %p","%Y-%m-%d, %H:%M","%d/%m/%Y %H:%M","%d.%m.%Y %H:%M","%d/%m/%Y, %I:%M %p","%d.%m.%Y, %I:%M %p"]

@dataclass
class Message:
    dt: datetime
    author: Optional[str]
    text: str
    is_system: bool = False

def try_parse_dt(s: str):
    s = s.strip()
    for fmt in DT_FORMATS:
        try:
            return datetime.strptime(s, fmt)
        except Exception:
            continue
    alt = s.replace(',', '')
    for fmt in ["%d/%m/%Y %H:%M", "%d/%m/%y %H:%M", "%d.%m.%Y %H:%M", "%d.%m.%y %H:%M"]:
        try: return datetime.strptime(alt, fmt)
        except Exception: continue
    return None

def parse_chat(path: str, tz: str = "America/Argentina/Buenos_Aires") -> List[Message]:
    tzinfo = ZoneInfo(tz)
    messages: List[Message] = []
    last = None
    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.rstrip("\n")
            if not line.strip():
                if last: last.text += "\n"
                continue
            m = HEADER_BRACKET_RE.match(line)
            if m:
                dt = try_parse_dt(m.group("dt"))
                if dt is None:
                    if last: last.text += "\n"+line
                    continue
                msg = Message(dt=dt.replace(tzinfo=tzinfo), author=m.group("author").strip(), text=m.group("text"), is_system=False)
                messages.append(msg); last = msg; continue
            m = HEADER_STD_RE.match(line)
            if m:
                dt = try_parse_dt(m.group("dt"))
                if dt is None:
                    if last: last.text += "\n"+line
                    continue
                msg = Message(dt=dt.replace(tzinfo=tzinfo), author=m.group("author").strip(), text=m.group("text"), is_system=False)
                messages.append(msg); last = msg; continue
            m = HEADER_SYSTEM_RE.match(line)
            if m:
                dt = try_parse_dt(m.group("dt"))
                if dt is None:
                    if last: last.text += "\n"+line
                    continue
                msg = Message(dt=dt.replace(tzinfo=tzinfo), author=None, text=m.group("text"), is_system=True)
                messages.append(msg); last = msg; continue
            if last: last.text += "\n"+line
    return messages
