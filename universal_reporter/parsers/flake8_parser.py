from typing import List
from .base import BaseParser
from ..models import Finding


class Flake8Parser(BaseParser):
    def can_handle(self, file_path: str) -> bool:
        return file_path.endswith("flake8_report.txt")

    def parse(self, file_path: str) -> List[Finding]:
        findings: List[Finding] = []

        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                try:
                    file_part, line_str, col_str, rest = line.split(":", 3)
                except ValueError:
                    continue

                rest = rest.strip()
                parts = rest.split(" ", 1)
                if len(parts) == 2:
                    code, message = parts
                else:
                    code = rest
                    message = rest

                if code.startswith("F"):
                    severity = "HIGH"
                elif code.startswith("E"):
                    severity = "MEDIUM"
                elif code.startswith("W"):
                    severity = "LOW"
                else:
                    severity = "INFO"

                try:
                    line_num = int(line_str)
                except ValueError:
                    line_num = None

                findings.append(
                    Finding(
                        tool="flake8",
                        check_type="Lint",
                        severity=severity,
                        file=file_part,
                        line=line_num,
                        message=message,
                        rule_id=code,
                        link=None,
                    )
                )

        return findings
