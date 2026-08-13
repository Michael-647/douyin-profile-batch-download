# Douyin Profile Batch Download

[中文](#中文说明) · [English](#english)

A privacy-conscious Codex skill for downloading public works from a Douyin creator profile, resuming interrupted jobs, and organizing media into fixed-size numbered batches.

一个注重隐私的 Codex 技能，用于批量下载抖音创作者主页的公开作品、断点续传，并按固定数量整理为编号批次。

> This repository is an orchestration skill. It does not bundle the upstream downloader, user Cookies, profile URLs, downloaded media, or personal download records.
>
> 本仓库是一个编排型技能，不内置上游下载器、用户 Cookie、主页链接、下载媒体或个人下载记录。

## 中文说明

### 功能

- 批量抓取抖音用户主页的公开视频和图文作品
- 支持登录 Cookie、翻页抓取及浏览器风控回退
- 使用 SQLite 与本地文件检查实现去重和断点续传
- 支持限制下载数量或下载全部作品
- 将嵌套目录中的视频按 `1-50`、`51-100` 等批次整理
- 默认使用复制模式，避免意外破坏原始下载目录
- 上传或发布前扫描主页链接、账号标识、Cookie 和本地路径等敏感信息

### 项目结构

```text
douyin-profile-batch-download/
├── SKILL.md                     # Codex 技能工作流
├── agents/openai.yaml           # 技能界面元数据
├── scripts/
│   ├── bootstrap.ps1            # 准备上游下载器和 Python 环境
│   ├── run-download.ps1         # 生成私有配置并执行下载
│   ├── organize-media.py        # 按固定数量复制或移动视频
│   └── privacy-audit.py         # 发布前隐私扫描
├── references/upstream.md       # 上游依赖说明
├── .gitignore                   # 排除 Cookie、日志、媒体和运行数据
└── LICENSE
```

### 环境要求

- Windows 10/11
- PowerShell 5.1 或更高版本
- Python 3.8 或更高版本
- Git
- 可用于扫码登录抖音的图形浏览器

### 安装技能

克隆到 Codex 技能目录：

```powershell
git clone https://github.com/Michael-647/douyin-profile-batch-download.git `
  "$HOME/.codex/skills/douyin-profile-batch-download"
```

重新打开 Codex 后，可通过 `$douyin-profile-batch-download` 显式调用技能。

### 1. 准备下载环境

运行时目录用于保存上游程序、虚拟环境、Cookie、数据库和日志。请将它放在本仓库之外，并保持私有。

```powershell
./scripts/bootstrap.ps1 -RuntimeDirectory "D:/private/douyin-runtime"
```

脚本会在运行时目录克隆开源项目 [`jiji262/douyin-downloader`](https://github.com/jiji262/douyin-downloader)，创建 Python 虚拟环境并安装依赖。

### 2. 登录并保存 Cookie

进入上游项目目录，并运行脚本输出的 Cookie 获取命令。例如：

```powershell
cd "D:/private/douyin-runtime/douyin-downloader"
& ".venv/Scripts/python.exe" -m tools.cookie_fetcher `
  --config "D:/private/douyin-runtime/private-config.yml" `
  --output "D:/private/douyin-runtime/cookies.json" `
  --include-all
```

在弹出的浏览器中扫码登录。确认已登录后，回到终端按 Enter。

不要分享或提交 `cookies.json`。Cookie 等同于临时登录凭证。

### 3. 下载主页作品

```powershell
./scripts/run-download.ps1 `
  -ProfileUrl "<用户提供的抖音主页链接>" `
  -OutputDirectory "D:/downloads/creator" `
  -RuntimeDirectory "D:/private/douyin-runtime" `
  -Limit 0 `
  -Threads 5
```

参数说明：

| 参数 | 说明 |
| --- | --- |
| `ProfileUrl` | 抖音创作者主页链接 |
| `OutputDirectory` | 媒体输出目录 |
| `RuntimeDirectory` | 私有运行时目录 |
| `Limit` | 最大作品数，`0` 表示全部 |
| `Threads` | 并发下载数，默认 `5` |

再次使用相同的运行时目录和输出目录执行命令，即可利用数据库与本地文件检查继续下载并跳过已完成项目。

### 4. 整理视频

默认复制并按每 50 个视频建立一个批次：

```powershell
python ./scripts/organize-media.py `
  --source "D:/downloads/creator" `
  --destination "D:/downloads/creator/batches" `
  --batch-size 50 `
  --mode copy
```

只有在明确需要移动文件时才使用 `--mode move`。脚本发现重名或目标文件已存在时会停止，不会覆盖文件。

### 5. 发布前隐私检查

```powershell
python ./scripts/privacy-audit.py --root .
```

检查通过后再提交到公开仓库。`.gitignore` 已默认排除 Cookie、配置、数据库、日志、PID、下载清单和常见视频格式。

### 常见问题

- **提示 Cookie 无效或接口返回空内容**：重新执行 Cookie 获取流程。
- **只能获取少量作品**：启用可见的浏览器回退，并按页面提示完成人机验证。
- **下载中断**：使用相同目录重新运行下载命令，避免删除数据库和已下载文件。
- **整理时提示文件重名**：保留现场并人工核对，不要强制覆盖。
- **平台更新后失效**：先检查上游项目是否有新版本或配置变更。

### 隐私与合规

- 仅下载你有权保存的内容。
- 遵守著作权、隐私权、平台规则及当地法律。
- 不要公开 Cookie、账号信息、下载记录或未经授权的媒体。
- 本项目仅提供工作流编排，不保证平台接口长期可用。

## English

### Features

- Download public video and image posts from a Douyin creator profile
- Support authenticated Cookies, pagination, and visible-browser fallback
- Resume interrupted jobs with SQLite and local-file deduplication
- Download all works or enforce a configurable item limit
- Organize nested videos into batches such as `1-50` and `51-100`
- Use non-destructive copy mode by default
- Scan for profile URLs, account identifiers, Cookies, and local paths before publication

### Repository layout

```text
douyin-profile-batch-download/
├── SKILL.md                     # Codex workflow instructions
├── agents/openai.yaml           # Skill UI metadata
├── scripts/
│   ├── bootstrap.ps1            # Prepare the upstream downloader and Python environment
│   ├── run-download.ps1         # Generate private config and run the download
│   ├── organize-media.py        # Copy or move videos into numbered batches
│   └── privacy-audit.py         # Scan for private data before publishing
├── references/upstream.md       # Upstream dependency notes
├── .gitignore                   # Exclude Cookies, logs, media, and runtime state
└── LICENSE
```

### Requirements

- Windows 10/11
- PowerShell 5.1 or later
- Python 3.8 or later
- Git
- A graphical browser for Douyin QR-code login

### Install the skill

Clone the repository into the Codex skills directory:

```powershell
git clone https://github.com/Michael-647/douyin-profile-batch-download.git `
  "$HOME/.codex/skills/douyin-profile-batch-download"
```

Restart Codex, then invoke the skill explicitly with `$douyin-profile-batch-download`.

### 1. Bootstrap the runtime

The runtime directory stores the upstream project, virtual environment, Cookies, database, and logs. Keep it private and outside this repository.

```powershell
./scripts/bootstrap.ps1 -RuntimeDirectory "D:/private/douyin-runtime"
```

The script clones [`jiji262/douyin-downloader`](https://github.com/jiji262/douyin-downloader), creates a Python virtual environment, and installs the required dependencies.

### 2. Sign in and capture Cookies

Enter the upstream repository and run the Cookie capture command printed by the bootstrap script. For example:

```powershell
cd "D:/private/douyin-runtime/douyin-downloader"
& ".venv/Scripts/python.exe" -m tools.cookie_fetcher `
  --config "D:/private/douyin-runtime/private-config.yml" `
  --output "D:/private/douyin-runtime/cookies.json" `
  --include-all
```

Sign in with the QR code in the visible browser. When login is complete, return to the terminal and press Enter.

Never share or commit `cookies.json`. Cookies are temporary authentication credentials.

### 3. Download a creator profile

```powershell
./scripts/run-download.ps1 `
  -ProfileUrl "<DOUYIN_PROFILE_URL_FROM_USER>" `
  -OutputDirectory "D:/downloads/creator" `
  -RuntimeDirectory "D:/private/douyin-runtime" `
  -Limit 0 `
  -Threads 5
```

| Parameter | Description |
| --- | --- |
| `ProfileUrl` | Douyin creator profile URL |
| `OutputDirectory` | Media output directory |
| `RuntimeDirectory` | Private runtime directory |
| `Limit` | Maximum number of works; `0` means all |
| `Threads` | Concurrent downloads; default is `5` |

Run the same command again with the same runtime and output directories to resume and skip completed items.

### 4. Organize downloaded videos

Copy videos into batches of 50:

```powershell
python ./scripts/organize-media.py `
  --source "D:/downloads/creator" `
  --destination "D:/downloads/creator/batches" `
  --batch-size 50 `
  --mode copy
```

Use `--mode move` only when moving files is explicitly intended. The script stops on duplicate names or existing targets and never overwrites them.

### 5. Run the privacy audit

```powershell
python ./scripts/privacy-audit.py --root .
```

Only publish after the audit passes. The included `.gitignore` excludes Cookies, generated configuration, databases, logs, PID files, manifests, and common video formats.

### Troubleshooting

- **Invalid Cookies or empty API responses:** capture fresh Cookies.
- **Only a small number of works are returned:** use visible browser fallback and complete any verification prompt.
- **Interrupted download:** rerun with the same directories; keep the database and existing media.
- **Filename collision during organization:** stop and inspect the files; do not force an overwrite.
- **Breakage after platform updates:** check the upstream repository for updates first.

### Privacy and responsible use

- Download only content you are authorized to save.
- Respect copyright, privacy, platform rules, and applicable law.
- Never publish Cookies, account details, download history, or unauthorized media.
- This repository provides workflow orchestration and cannot guarantee permanent compatibility with platform changes.

## Upstream and license

This skill uses the MIT-licensed [`jiji262/douyin-downloader`](https://github.com/jiji262/douyin-downloader) as a runtime dependency. Its source code is not bundled here.

The orchestration files in this repository are released under the [MIT License](LICENSE).
