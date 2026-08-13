---
name: douyin-profile-batch-download
description: Batch-download public works from a Douyin creator profile with authenticated cookies, resumable deduplication, progress logs, and optional fixed-size batch organization. Use when Codex needs to archive a Douyin user homepage, download hundreds of creator videos or image posts, resume an interrupted profile download, organize downloaded media into numbered batches such as 1-50 and 51-100, or consolidate nested video files into one directory.
---

# Douyin Profile Batch Download

Use the upstream open-source `jiji262/douyin-downloader` project as the download engine. Keep this skill as an orchestration layer; do not vendor upstream source code into the skill.

## Safety and privacy

- Download only content the user is authorized to save. Respect copyright, privacy, platform terms, and local law.
- Never expose, print, commit, or return Cookie values. Treat `cookies.json`, generated configs, databases, manifests, logs, PIDs, and downloaded media as private runtime data.
- Put runtime state outside the skill directory. Never use a Git repository as the default download directory.
- Never hard-code profile URLs, creator IDs, usernames, local paths, or prior download records.
- Do not delete source media or metadata unless the user explicitly requests deletion.

## Workflow

1. Confirm the profile URL, output directory, batch size, and whether to download all works or a limit.
2. Run `scripts/bootstrap.ps1` to clone or update the upstream downloader in a private runtime directory and create its virtual environment.
3. Run the upstream cookie capture utility in a visible browser. Ask the user to sign in and confirm in the terminal. Store the result only in the runtime directory.
4. Run `scripts/run-download.ps1` with explicit `-ProfileUrl`, `-OutputDirectory`, and `-RuntimeDirectory` arguments. The script generates a private configuration and starts or resumes the download.
5. Verify completion from the downloader summary, manifest, database, and actual media count. Do not infer completion merely because the process exited.
6. If numbered folders are requested, run `scripts/organize-media.py`. Use `--mode copy` by default; use `--mode move` only when the user explicitly requests moving files.
7. Run `scripts/privacy-audit.py` on the skill or proposed Git repository before publishing.

## Commands

Bootstrap on Windows:

```powershell
./scripts/bootstrap.ps1 -RuntimeDirectory "D:/private/douyin-runtime"
```

Download a profile after Cookie capture:

```powershell
./scripts/run-download.ps1 `
  -ProfileUrl "<PROFILE_URL_FROM_USER>" `
  -OutputDirectory "D:/downloads/creator" `
  -RuntimeDirectory "D:/private/douyin-runtime" `
  -Limit 0
```

Organize media into batches of 50:

```powershell
python ./scripts/organize-media.py `
  --source "D:/downloads/creator" `
  --destination "D:/downloads/creator/batches" `
  --batch-size 50 `
  --mode move
```

Before GitHub upload:

```powershell
python ./scripts/privacy-audit.py --root .
```

## Recovery

- Reuse the same runtime directory and output directory to resume; the upstream SQLite database and local-file checks provide deduplication.
- If API requests return empty responses or login-required errors, recapture Cookies instead of embedding them in config templates.
- If pagination triggers a verification page, keep browser fallback visible and let the user complete the verification.
- If filenames collide during organization, stop and report the collisions. Do not overwrite.

Read `references/upstream.md` when installing, updating, licensing, or troubleshooting the upstream project.
