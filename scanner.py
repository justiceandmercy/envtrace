"""Scan source files for environment variable references."""
import re
from pathlib import Path

PATTERNS = [
    re.compile(r"process\.env\.([A-Za-z_][A-Za-z0-9_]*)"),
    re.compile(r"process\.env\[['\"]([A-Za-z_][A-Za-z0-9_]*)['\"]\]"),
    re.compile(r"os\.environ\[['\"]([A-Za-z_][A-Za-z0-9_]*)['\"]\]"),
    re.compile(r"os\.environ\.get\(['\"]([A-Za-z_][A-Za-z0-9_]*)['\"]"),
    re.compile(r"os\.getenv\(['\"]([A-Za-z_][A-Za-z0-9_]*)['\"]"),
    re.compile(r"getenv\(['\"]([A-Za-z_][A-Za-z0-9_]*)['\"]"),
    re.compile(r"env\(['\"]([A-Za-z_][A-Za-z0-9_]*)['\"]"),
]

DEFAULT_IGNORE = {
    ".git", "node_modules", ".venv", "venv", "__pycache__",
    "dist", "build", ".next", "target", "vendor",
}

TEXT_EXTS = {
    ".py", ".js", ".ts", ".jsx", ".tsx", ".go", ".rs", ".rb", ".php",
    ".java", ".kt", ".c", ".cpp", ".h", ".sh", ".yml", ".yaml", ".toml",
    ".json", ".md",
}


def scan_file(path: Path) -> set:
    found = set()
    try:
        text = path.read_text(errors="ignore")
    except (OSError, UnicodeError):
        return found
    for pat in PATTERNS:
        found.update(pat.findall(text))
    return found


def scan_directory(root: Path, ignores) -> dict:
    used = {}
    ignore_set = set(DEFAULT_IGNORE) | set(ignores or [])
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if any(part in ignore_set for part in p.parts):
            continue
        if p.suffix.lower() not in TEXT_EXTS and p.name not in (".env",):
            continue
        for v in scan_file(p):
            used.setdefault(v, []).append(str(p.relative_to(root)))
    return used


def parse_dotenv(path: Path) -> set:
    names = set()
    try:
        for raw in path.read_text().splitlines():
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                names.add(line.split("=", 1)[0].strip())
    except (OSError, UnicodeError):
        pass
    return names