import json
from typing import List
from .base import BaseParser
from ..models import Finding


class CoverageParser(BaseParser):
    def can_handle(self, file_path: str) -> bool:
        return file_path.endswith("coverage_summary.json")

    def parse(self, file_path: str) -> List[Finding]:
        findings = []

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        coverage = data.get("line_coverage", 0)

        findings.append(
            Finding(
                tool="Coverage",
                check_type="Coverage",
                severity="INFO",
                file=None,
                line=None,
                message=f"Покрытие строк: {coverage}%",
                rule_id=None,
                link=None
            )
        )

        return findings
