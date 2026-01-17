import re
from typing import List, Dict

class ContentValidator:
    """
    Validates content against a set of guardrails.
    """

    FORBIDDEN_WORDS = ["confidential", "internal use only", "secret"]
    MIN_WORD_COUNT = 100
    REQUIRED_HEADERS = ["Introduction", "Conclusion"]

    @staticmethod
    def validate(content: str) -> Dict[str, str]:
        """
        Runs checks on the content. Returns a dict with status and feedback.
        """
        issues = []

        # 1. Check for forbidden words
        content_lower = content.lower()
        for word in ContentValidator.FORBIDDEN_WORDS:
            if word in content_lower:
                issues.append(f"Contains forbidden word: '{word}'")

        # 2. Check length
        word_count = len(content.split())
        if word_count < ContentValidator.MIN_WORD_COUNT:
            issues.append(f"Content too short ({word_count} words). Minimum is {ContentValidator.MIN_WORD_COUNT}.")

        # 3. Check for headers (Basic heuristic)
        # Assuming markdown headers #, ##, etc.
        # We search for the specific keywords loosely as headers
        for header in ContentValidator.REQUIRED_HEADERS:
            if not re.search(f"#{1,6}\\s*{header}", content, re.IGNORECASE):
                issues.append(f"Missing required section header: '{header}'")

        if issues:
            return {
                "valid": False,
                "feedback": "Validation FAILED. Issues found:\n- " + "\n- ".join(issues) + "\n\nPlease revise the content."
            }
        else:
            return {
                "valid": True,
                "feedback": "Validation PASSED. Content meets all guidelines."
            }
