from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class Finding:
    """
    Одна найденная проблема из отчёта.
    """
    tool: str             # какой инструмент (bandit, flake8 и т.д.)
    check_type: str       # тип проверки: SAST, Lint, DAST, Coverage и т.п.
    severity: str         # уровень: CRITICAL, HIGH, MEDIUM, LOW, INFO
    file: Optional[str]   # файл, где найдена проблема (если есть)
    line: Optional[int]   # строка (если есть)
    message: str          # текст описания проблемы
    rule_id: Optional[str] = None  # код правила (например, B307, E501)
    link: Optional[str] = None     # ссылка на документацию/подробности


@dataclass
class ReportSummary:
    """
    Краткая сводка по отчёту.
    """
    total: int                      # всего найдено проблем
    by_severity: Dict[str, int]     # {severity: количество}
    by_tool: Dict[str, int]         # {tool: количество}
    by_type: Dict[str, int]         # {check_type: количество}
