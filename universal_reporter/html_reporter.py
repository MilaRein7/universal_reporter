import os
from datetime import datetime
from typing import List

from jinja2 import Environment, FileSystemLoader, select_autoescape

from .models import Finding, ReportSummary


def build_summary(findings: List[Finding]) -> ReportSummary:
    """
    Строит сводку по всем найденным проблемам.
    """
    by_severity = {}
    by_tool = {}
    by_type = {}

    for f in findings:
        by_severity[f.severity] = by_severity.get(f.severity, 0) + 1
        by_tool[f.tool] = by_tool.get(f.tool, 0) + 1
        by_type[f.check_type] = by_type.get(f.check_type, 0) + 1

    return ReportSummary(
        total=len(findings),
        by_severity=by_severity,
        by_tool=by_tool,
        by_type=by_type,
    )


def render_html_report(findings: List[Finding], output_path: str) -> None:
    """
    Рендерит HTML-отчёт и сохраняет в output_path.
    """
    summary = build_summary(findings)

    # Папка, где лежит шаблон
    templates_dir = os.path.join(os.path.dirname(__file__), "templates")

    env = Environment(
        loader=FileSystemLoader(templates_dir),
        autoescape=select_autoescape(["html", "xml"]),
    )

    # Имя файла шаблона
    template = env.get_template("report_template.html")

    rendered = template.render(
        findings=findings,
        summary=summary,
        generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(rendered)
