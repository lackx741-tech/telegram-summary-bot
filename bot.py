"""Minimal Telegram summary bot for local and Docker deployment."""

from __future__ import annotations

import json
import logging
import os
import signal
import time
from collections import defaultdict, deque
from typing import Any

import urllib3
from dotenv import load_dotenv


load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
POLL_TIMEOUT = int(os.getenv("POLL_TIMEOUT", "30"))
MAX_STORED_MESSAGES = int(os.getenv("MAX_STORED_MESSAGES", "100"))
SUMMARY_SENTENCES = int(os.getenv("SUMMARY_SENTENCES", "5"))

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger(__name__)

http = urllib3.PoolManager()
chat_messages: dict[int, deque[str]] = defaultdict(lambda: deque(maxlen=MAX_STORED_MESSAGES))
running = True


def handle_shutdown(_signum: int, _frame: Any) -> None:
    global running
    running = False


def telegram_api(method: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    if not BOT_TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is required")

    response = http.request(
        "POST",
        f"https://api.telegram.org/bot{BOT_TOKEN}/{method}",
        body=json.dumps(payload or {}).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        timeout=urllib3.Timeout(connect=10.0, read=POLL_TIMEOUT + 10.0),
    )
    data = json.loads(response.data.decode("utf-8"))
    if not data.get("ok"):
        raise RuntimeError(f"Telegram API error for {method}: {data}")
    return data


def send_message(chat_id: int, text: str, reply_to_message_id: int | None = None) -> None:
    payload: dict[str, Any] = {"chat_id": chat_id, "text": text[:4096]}
    if reply_to_message_id:
        payload["reply_to_message_id"] = reply_to_message_id
    telegram_api("sendMessage", payload)


def summarize_text(text: str) -> str:
    cleaned = " ".join(text.split())
    if not cleaned:
        return "No text found to summarize."

    sentences = [
        sentence.strip()
        for sentence in cleaned.replace("!", ".").replace("?", ".").split(".")
        if sentence.strip()
    ]
    if not sentences:
        return cleaned[:1000]

    summary = ". ".join(sentences[:SUMMARY_SENTENCES])
    return f"{summary}."


def help_text() -> str:
    return (
        "Telegram Summary Bot\n\n"
        "Commands:\n"
        "/start - Check that the bot is running\n"
        "/help - Show this help message\n"
        "/summary <text> - Summarize the text after the command\n"
        "/summary - Summarize recent text messages from this chat\n\n"
        "Tip: In groups, disable BotFather privacy mode if you want the bot to read all messages."
    )


def process_message(message: dict[str, Any]) -> None:
    chat = message.get("chat", {})
    chat_id = chat.get("id")
    text = message.get("text", "")
    message_id = message.get("message_id")

    if not isinstance(chat_id, int) or not text:
        return

    if text.startswith("/start"):
        send_message(chat_id, "Bot is running. Send /help for commands.", message_id)
        return

    if text.startswith("/help"):
        send_message(chat_id, help_text(), message_id)
        return

    if text.startswith("/summary"):
        command_text = text.removeprefix("/summary").strip()
        if command_text:
            source_text = command_text
        else:
            source_text = " ".join(chat_messages[chat_id])
        send_message(chat_id, summarize_text(source_text), message_id)
        return

    chat_messages[chat_id].append(text)


def poll_updates() -> None:
    offset = 0
    while running:
        try:
            data = telegram_api("getUpdates", {"offset": offset, "timeout": POLL_TIMEOUT})
            for update in data.get("result", []):
                offset = update["update_id"] + 1
                message = update.get("message") or update.get("edited_message")
                if message:
                    process_message(message)
        except Exception:
            logger.exception("Polling failed; retrying shortly")
            time.sleep(5)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, handle_shutdown)
    signal.signal(signal.SIGTERM, handle_shutdown)
    logger.info("Starting Telegram summary bot")
    poll_updates()
