# Upstream dependency

This skill orchestrates the MIT-licensed project:

- Repository: `https://github.com/jiji262/douyin-downloader`
- Role: profile pagination, authenticated API access, no-watermark media selection, retry, browser fallback, SQLite deduplication, and download integrity checks.

Do not copy upstream source into this skill. Clone it at runtime into a private directory. Preserve its license and attribution when distributing a derived work.

Expected entry points:

- `run.py`: downloader CLI
- `tools.cookie_fetcher`: visible-browser Cookie capture
- `config.example.yml`: upstream configuration reference

Platform behavior can change. When download failures appear after previously successful runs, check the upstream repository for current requirements before modifying this skill.
