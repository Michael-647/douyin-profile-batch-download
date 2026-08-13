#!/usr/bin/env python3
import argparse
import shutil
from pathlib import Path

VIDEO_EXTENSIONS = {".mp4", ".mov", ".mkv", ".webm", ".avi", ".m4v"}


def main() -> int:
    parser = argparse.ArgumentParser(description="Organize nested videos into numbered batches.")
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--destination", required=True, type=Path)
    parser.add_argument("--batch-size", type=int, default=50)
    parser.add_argument("--mode", choices=("copy", "move"), default="copy")
    args = parser.parse_args()

    source = args.source.resolve()
    destination = args.destination.resolve()
    if args.batch_size < 1:
        parser.error("--batch-size must be positive")
    if source == destination:
        parser.error("source and destination must differ")

    videos = sorted(
        (p for p in source.rglob("*") if p.is_file() and p.suffix.lower() in VIDEO_EXTENSIONS
         and destination not in p.parents),
        key=lambda p: (p.stat().st_mtime, p.name),
        reverse=True,
    )
    duplicate_names = sorted({p.name for p in videos if sum(q.name == p.name for q in videos) > 1})
    if duplicate_names:
        raise SystemExit(f"Duplicate filenames detected; refusing to overwrite: {duplicate_names[:10]}")

    total = len(videos)
    for index, video in enumerate(videos, 1):
        start = ((index - 1) // args.batch_size) * args.batch_size + 1
        end = min(start + args.batch_size - 1, total)
        batch = destination / f"{start}-{end}"
        batch.mkdir(parents=True, exist_ok=True)
        target = batch / video.name
        if target.exists():
            raise SystemExit(f"Target exists; refusing to overwrite: {target}")
        (shutil.copy2 if args.mode == "copy" else shutil.move)(video, target)

    verb = "Copied" if args.mode == "copy" else "Moved"
    print(f"{verb} {total} video(s) into {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
