"""
Policy compliance validation engine.

Checks generated SOW documents against a library of organizational
policy rules and returns a structured compliance report.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)


class Severity(str, Enum):
    CRITICAL = "critical"
    WARNING = "warning"
    INFO = "info"


@dataclass
class ComplianceRule:
    """A single compliance policy rule."""
    rule_id: str
    description: str
    category: str
    severity: Severity
    required_keywords: list[str] = field(default_factory=list)
    forbidden_patterns: list[str] = field(default_factory=list)


@dataclass
class ComplianceViolation:
    """A detected compliance violation."""
    rule: ComplianceRule
    section: str
    message: str
    suggestion: str = ""


@dataclass
class ComplianceReport:
    """Full compliance assessment for a document."""
    score: float
    violations: list[ComplianceViolation]
    passed_rules: int
    total_rules: int

    @property
    def grade(self) -> str:
        if self.score >= 90:
            return "A"
        elif self.score >= 80:
            return "B"
        elif self.score >= 70:
            return "C"
        return "F"


class ComplianceChecker:
    """Validates SOW documents against organizational policy rules.

    Parameters
    ----------
    rules : list[ComplianceRule]
        Policy rules to check against.
    """

    def __init__(self, rules: list[ComplianceRule] | None = None) -> None:
        self.rules = rules or self._load_default_rules()

    def check(self, sections: dict[str, str]) -> ComplianceReport:
        """Run all compliance rules against document sections.

        Parameters
        ----------
        sections : dict[str, str]
            Mapping of section title → section content.

        Returns
        -------
        ComplianceReport
            Structured compliance assessment.
        """
        violations: list[ComplianceViolation] = []
        full_text = " ".join(sections.values()).lower()

        for rule in self.rules:
            # Check required keywords
            for keyword in rule.required_keywords:
                if keyword.lower() not in full_text:
                    violations.append(ComplianceViolation(
                        rule=rule,
                        section="Global",
                        message=f"Missing required term: \"{keyword}\"",
                        suggestion=f"Add language addressing \"{keyword}\" per policy {rule.rule_id}.",
                    ))

            # Check forbidden patterns
            for pattern in rule.forbidden_patterns:
                if pattern.lower() in full_text:
                    violations.append(ComplianceViolation(
                        rule=rule,
                        section="Global",
                        message=f"Forbidden pattern found: \"{pattern}\"",
                        suggestion=f"Remove or rephrase per policy {rule.rule_id}.",
                    ))

        passed = len(self.rules) - len(violations)
        score = (passed / len(self.rules) * 100) if self.rules else 100

        return ComplianceReport(
            score=round(score, 1),
            violations=violations,
            passed_rules=passed,
            total_rules=len(self.rules),
        )

    @staticmethod
    def _load_default_rules() -> list[ComplianceRule]:
        """Load default Government of Canada SOW compliance rules."""
        return [
            ComplianceRule(
                rule_id="GOC-001",
                description="Must include official languages clause",
                category="Legal",
                severity=Severity.CRITICAL,
                required_keywords=["official languages", "bilingual"],
            ),
            ComplianceRule(
                rule_id="GOC-002",
                description="Must reference security clearance requirements",
                category="Security",
                severity=Severity.CRITICAL,
                required_keywords=["security clearance", "reliability status"],
            ),
            ComplianceRule(
                rule_id="GOC-003",
                description="Must include intellectual property clause",
                category="Legal",
                severity=Severity.WARNING,
                required_keywords=["intellectual property", "crown copyright"],
            ),
            # ... additional rules loaded from YAML in production
        ]
