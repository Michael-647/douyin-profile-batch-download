#!/usr/bin/env python3
import argparse
import re
from pathlib import Path

TEXT_EXTENSIONS = {".md", ".py", ".ps1", ".yml", ".yaml", ".json", ".toml", ".txt", ".gitignore"}
FORBIDDEN_NAMES = re.compile(r"(^|[._-])(cookies?|logs?|pid|database|manifest)([._-]|$)|^downloads?$", re.I)
PATTERNS = {
    "Douyin profile/video URL": re.compile(r"https?://(?:www\.)?douyin\.com/(?:user|video|note)/[^\s\"'<>]+", re.I),
    "Douyin secure user id": re.compile(r"MS4wLjAB[A-Za-z0-9_-]{20,}"),
    "Windows absolute path": re.compile(r"\b[A-Za-z]:[\\/](?!private\b|downloads\b)[^\r\n\"']+"),
    "Cookie value": re.compile(r"\b(?:sessionid|sid_guard|ttwid|odin_tt|passport_csrf_token|msToken)\s*[:=]\s*[\"']?(?!\s|\"\"|'')[^\s,}\"']+", re.I),
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan a skill/repository for private runtime data.")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    root = args.root.resolve()
    findings: list[str] = []

    for path in root.rglob("*"):
        if ".git" in path.parts or not path.is_file():
            continue
        relative = path.relative_to(root)
        if FORBIDDEN_NAMES.search(path.name) and path.name not in {"privacy-audit.py"}:
            findings.append(f"forbidden runtime filename: {relative}")
        if path.suffix.lower() not in TEXT_EXTENSIONS and path.name != ".gitignore":
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            findings.append(f"non-UTF-8 text or binary file: {relative}")
            continue
        for label, pattern in PATTERNS.items():
            for match in pattern.finditer(text):
                line = text.count("\n", 0, match.start()) + 1
                findings.append(f"{label}: {relative}:{line}")

    if findings:
        print("Privacy audit failed:")
        print("\n".join(f"- {item}" for item in findings))
        return 1
    print(f"Privacy audit passed: {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
