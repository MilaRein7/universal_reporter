import requests
from typing import List

from universal_reporter.models import Finding, ReportSummary


def build_summary_text(summary: ReportSummary) -> str:
    lines = []
    lines.append("🔔 DevSecOps отчёт готов")
    lines.append(f"Всего проблем: {summary.total}")

    if summary.by_severity:
        lines.append("По уровням:")
        for severity, count in summary.by_severity.items():
            lines.append(f"  - {severity}: {count}")

    if summary.by_tool:
        lines.append("По инструментам:")
        for tool, count in summary.by_tool.items():
            lines.append(f"  - {tool}: {count}")

    return "\n".join(lines)


def send_telegram_message(bot_token: str, chat_id: str, text: str) -> None:
    """
    Отправляет простое текстовое сообщение через Telegram Bot API.
    """
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown",
    }
    response = requests.post(url, json=payload, timeout=10)
    response.raise_for_status()
