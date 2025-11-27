import json
import os
from typing import List

from universal_reporter.models import Finding
from universal_reporter.parsers.base_parser import BaseParser


class BanditParser(BaseParser):
    def can_handle(self, file_path: str) -> bool:
        return os.path.basename(file_path).lower().startswith("bandit") and file_path.endswith(".json")

    def parse(self, file_path: str) -> List[Finding]:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        findings: List[Finding] = []

        results = data.get("results", [])
        for item in results:
            severity = item.get("issue_severity", "LOW").upper()
            filename = item.get("filename")
            line_number = item.get("line_number")
            message = item.get("issue_text", "")
            test_id = item.get("test_id")
            more_info = item.get("more_info")

            finding = Finding(
                tool="bandit",
                check_type="SAST",
                severity=severity,
                file=filename,
                line=line_number,
                message=message,
                rule_id=test_id,
                link=more_info,
            )
            findings.append(finding)

        return findings
