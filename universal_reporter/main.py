import os
from typing import List

from .parsers.bandit_parser import BanditParser
from .parsers.flake8_parser import Flake8Parser
from .models import Finding
from .html_reporter import render_html_report, build_summary
from .telegram_notifier import send_telegram_message, build_summary_text
from .parsers.zap_parser import ZapParser
from .parsers.coverage_parser import CoverageParser



BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

REPORTS_DIR = os.path.join(BASE_DIR, "reports")

OUTPUT_REPORT_PATH = os.path.join(BASE_DIR, "devsecops_report.html")

TELEGRAM_BOT_TOKEN = "8570843218:AAFbzOkfiuuOIeBPCpA2QLKALGNtI9SBlPI"

TELEGRAM_CHAT_ID = "1492444629"


def collect_findings() -> List[Finding]:
    """Собирает все найденные проблемы из файлов отчётов в папке REPORTS_DIR."""
    parsers = [
        BanditParser(),
        Flake8Parser(),
        ZapParser(),
        CoverageParser(),
    ]
     
    findings: List[Finding] = []

    if not os.path.isdir(REPORTS_DIR):
        print(f"Папка с отчётами не найдена: {REPORTS_DIR}")
        return findings

    for file_name in os.listdir(REPORTS_DIR):
        file_path = os.path.join(REPORTS_DIR, file_name)
        if not os.path.isfile(file_path):
            continue

        handled = False
        for parser in parsers:
            if parser.can_handle(file_path):
                print(f"Используем {parser.__class__.__name__} для файла {file_name}")
                parsed_findings = parser.parse(file_path)
                findings.extend(parsed_findings)
                handled = True
                break

        if not handled:
            print(f"Нет подходящего парсера для файла: {file_name}")

    return findings


def main():
    print("Сбор результатов проверок...")
    findings = collect_findings()

    print(f"Найдено проблем: {len(findings)}")
    print("Генерация HTML-отчёта...")
    render_html_report(findings, OUTPUT_REPORT_PATH)
    print(f"Отчёт сохранён в {OUTPUT_REPORT_PATH}")

    print("Формирование краткого резюме и отправка в Telegram...")
    summary = build_summary(findings)
    text = build_summary_text(summary)

    if not TELEGRAM_BOT_TOKEN:
        print("TELEGRAM_BOT_TOKEN не настроен, пропускаем отправку сообщения.")
        return

    if not TELEGRAM_CHAT_ID:
        print("TELEGRAM_CHAT_ID не задан, пока не можем отправить сообщение.")
        print("Сначала получи chat_id и пропиши его в main.py.")
        return

    try:
        send_telegram_message(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, text)
        print("Уведомление отправлено в Telegram.")
    except Exception as e:
        print(f"Ошибка отправки в Telegram: {e}")


if __name__ == "__main__":
    main()


#python -m universal_reporter.main запустить 