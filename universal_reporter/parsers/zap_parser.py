import json
from typing import List
from .base import BaseParser
from ..models import Finding


class ZapParser(BaseParser):
    def can_handle(self, file_path: str) -> bool:
        return file_path.endswith("zap_report.json")

    def parse(self, file_path: str) -> List[Finding]:
        findings = []

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        for alert in data.get("alerts", []):
            risk = alert.get("risk", "").upper()

            if risk == "HIGH":
                severity = "HIGH"
            elif risk == "MEDIUM":
                severity = "MEDIUM"
            else:
                severity = "LOW"

            message = f"{alert.get('description')} Решение: {alert.get('solution')}"

            findings.append(
                Finding(
                    tool="OWASP ZAP",
                    check_type="DAST",
                    severity=severity,
                    file=alert.get("url"),
                    line=None,
                    message=message,
                    rule_id=alert.get("name"),
                    link=alert.get("url")
                )
            )

        return findings