# processor/run.py
import argparse, os, sys, json, smtplib, ssl, urllib.parse, urllib.request
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from .whatsapp_parser import parse_chat
from .summarizer import build_summary_ru

def send_telegram(bot_token: str, chat_id: str, text: str):
    base = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = urllib.parse.urlencode({"chat_id": chat_id, "text": text}).encode("utf-8")
    req = urllib.request.Request(base, data=data, method="POST")
    with urllib.request.urlopen(req, timeout=30) as resp:
        resp.read()

def send_email(conf: dict, subject: str, text: str):
    msg = MIMEMultipart()
    msg["From"] = conf.get("username", "")
    msg["To"] = conf.get("to", "")
    msg["Subject"] = subject
    msg.attach(MIMEText(text, "plain", "utf-8"))
    context = ssl.create_default_context()
    with smtplib.SMTP(conf["smtp_host"], conf.get("smtp_port", 587)) as server:
        server.starttls(context=context)
        server.login(conf["username"], conf["password"])
        server.send_message(msg)

def load_config(path: str) -> dict:
    if not path or not os.path.exists(path):
        return {}
    text = open(path, "r", encoding="utf-8").read()
    try:
        return json.loads(text)
    except Exception:
        conf = {}
        for line in text.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if ":" in line:
                k, v = line.split(":", 1)
                conf[k.strip()] = v.strip().strip("'\"")
        return conf

def main():
    ap = argparse.ArgumentParser(description="WhatsApp _chat.txt -> RU дайджест (вчера/сегодня)")
    ap.add_argument("--input", "-i", default="_chat.txt")
    ap.add_argument("--out", "-o", default="digest_ru.txt")
    ap.add_argument("--config", "-c", default="config/config.yaml")
    args = ap.parse_args()

    conf = load_config(args.config)
    tz = conf.get("timezone", "America/Argentina/Buenos_Aires")

    messages = parse_chat(args.input, tz=tz)
    summary = build_summary_ru(messages, tz=tz).text

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(summary)
    print(summary)

    # Optional: Telegram
    tel_enabled = str(conf.get("telegram.enabled", conf.get("telegram_enabled", "false"))).lower() in ["true","1","yes"]
    if tel_enabled:
        bt = conf.get("telegram.bot_token", conf.get("telegram_bot_token", ""))
        cid = conf.get("telegram.chat_id", conf.get("telegram_chat_id", ""))
        if bt and cid:
            try:
                send_telegram(bt, cid, summary)
                print("Sent to Telegram.")
            except Exception as e:
                print(f"Telegram send failed: {e}", file=sys.stderr)

    # Optional: Email
    email_enabled = str(conf.get("email.enabled", conf.get("email_enabled", "false"))).lower() in ["true","1","yes"]
    if email_enabled:
        try:
            ec = {
                "smtp_host": conf.get("email.smtp_host", conf.get("email_smtp_host", "")),
                "smtp_port": int(conf.get("email.smtp_port", conf.get("email_smtp_port", "587"))),
                "username": conf.get("email.username", conf.get("email_username", "")),
                "password": conf.get("email.password", conf.get("email_password", "")),
                "to": conf.get("email.to", conf.get("email_to", "")),
            }
            send_email(ec, "Дайджест чата (вчера/сегодня)", summary)
            print("Sent email.")
        except Exception as e:
            print(f"Email send failed: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
