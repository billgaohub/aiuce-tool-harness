"""
Keyword-based file routing engine with chain rules.
"""

from typing import Dict, Any, List


class SmartFileRouter:
    """
    Keyword-driven file classification engine with rule chaining.
    Supports multiple categories with priority-based routing.
    """

    DEFAULT_RULES = [
        {"keywords": ["medical", "health", "diagnosis", "prescription", "weight", "hospital"], "target": "DATA/Medical/", "priority": 10},
        {"keywords": ["contract", "order", "invoice", "client", "meeting", "project"], "target": "WORK/Business/", "priority": 9},
        {"keywords": ["family", "personal", "home", "kids", "children", "parents"], "target": "LIFE/Personal/", "priority": 8},
        {"keywords": ["code", "git", "development", "design", "plan", "milestone"], "target": "WORK/Projects/", "priority": 7},
        {"keywords": ["study", "course", "notes", "lecture", "paper", "thesis", "research"], "target": "KNOWLEDGE/Research/", "priority": 6},
        {"keywords": ["decision", "choice", "option", "analysis", "evaluation"], "target": "KNOWLEDGE/Decisions/", "priority": 6},
        {"keywords": ["review", "reflection", "summary", "lessons", "experience"], "target": "KNOWLEDGE/Reviews/", "priority": 5},
    ]

    def __init__(self, custom_rules: List[Dict[str, Any]] = None):
        self.rules = (custom_rules or []) + self.DEFAULT_RULES
        self.rules.sort(key=lambda r: r["priority"], reverse=True)

    def classify(self, text: str) -> Dict[str, Any]:
        """
        Classify text based on keyword rules.
        Returns routing result with confidence score.
        """
        text_lower = text.lower()
        matched_rules = []

        for rule in self.rules:
            matched_kws = [kw for kw in rule["keywords"] if kw.lower() in text_lower]
            if matched_kws:
                matched_rules.append({
                    "rule": rule,
                    "matched_keywords": matched_kws,
                    "score": len(matched_kws) * rule["priority"],
                })

        if not matched_rules:
            return {
                "target": "DATA/INBOX/",
                "confidence": 0.5,
                "keywords": [],
                "routed_by": "default",
            }

        # Get highest scoring rule
        best = max(matched_rules, key=lambda r: r["score"])
        confidence = min(best["score"] / 20.0, 1.0)

        return {
            "target": best["rule"]["target"],
            "confidence": confidence,
            "keywords": best["matched_keywords"],
            "routed_by": "keyword_rule",
        }