import re
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class FailureSummary:
    error_lines: List[str]
    probable_root_cause: Optional[str]


COMMON_PATTERNS = [
    (re.compile(r"ModuleNotFoundError: No module named '(.+)'"), "Missing Python dependency"),
    (re.compile(r"SyntaxError:"), "Python syntax error"),
    (re.compile(r"AssertionError"), "Test assertion failed"),
    (re.compile(r"npm ERR!"), "Node/npm install or build error"),
    (re.compile(r"docker:.*(error|failed)", re.IGNORECASE), "Docker build/runtime error"),
    (re.compile(r"permission denied", re.IGNORECASE), "Permission issue"),
]


def extract_error_lines(log_text: str, max_lines: int = 25) -> List[str]:
    lines = log_text.splitlines()
    hits = []
    for line in lines:
        if any(x in line.lower() for x in ["error", "failed", "exception", "traceback", "fatal"]):
            hits.append(line.strip())
    # keep last N (usually most relevant)
    return hits[-max_lines:]


def guess_root_cause(error_lines: List[str]) -> Optional[str]:
    joined = "\n".join(error_lines)
    for pattern, label in COMMON_PATTERNS:
        if pattern.search(joined):
            return label
    return None


def summarize_failure(log_text: str) -> FailureSummary:
    errs = extract_error_lines(log_text)
    root = guess_root_cause(errs)
    return FailureSummary(error_lines=errs, probable_root_cause=root)

