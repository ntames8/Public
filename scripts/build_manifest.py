#!/usr/bin/env python3
"""저장소를 스캔해 루트의 manifest.json 을 생성한다. (표준 라이브러리만 사용)

사용: python scripts/build_manifest.py
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCLUDE_DIRS = {".git", ".github", "node_modules", "scripts", "NVIDIA Corporation"}
EXCLUDE_FILES = {"index.html", "manifest.json", "CLAUDE.md", ".gitkeep", ".nojekyll"}
VIEWABLE = {".md", ".markdown", ".html", ".htm", ".txt", ".xml", ".json",
            ".csv", ".log", ".pdf", ".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"}


def title_of(path, ext):
    """md/html 의 제목(첫 # 헤딩 또는 <title>)을 뽑는다. 없으면 None."""
    try:
        with open(path, encoding="utf-8", errors="ignore") as f:
            head = f.read(4096)
    except OSError:
        return None
    if ext in (".md", ".markdown"):
        m = re.search(r"^#\s+(.+?)\s*$", head, re.M)
    elif ext in (".html", ".htm"):
        m = re.search(r"<title[^>]*>(.*?)</title>", head, re.I | re.S)
    else:
        return None
    return m.group(1).strip() if m else None


def scan(rel=""):
    abs_dir = os.path.join(ROOT, rel) if rel else ROOT
    folders, files = [], []
    for name in sorted(os.listdir(abs_dir), key=str.lower):
        if name.startswith("."):
            continue
        p = os.path.join(abs_dir, name)
        r = f"{rel}/{name}" if rel else name
        if os.path.isdir(p):
            if name in EXCLUDE_DIRS:
                continue
            children = scan(r)
            if children:  # 빈 폴더는 숨김
                folders.append({"type": "dir", "name": name, "children": children})
        else:
            ext = os.path.splitext(name)[1].lower()
            if name in EXCLUDE_FILES or ext not in VIEWABLE:
                continue
            node = {"type": "file", "name": name, "path": r}
            t = title_of(p, ext)
            if t:
                node["title"] = t
            files.append(node)
    return folders + files  # 폴더 먼저, 그 다음 파일


def main():
    manifest = {"version": 1, "tree": scan()}
    out = os.path.join(ROOT, "manifest.json")
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
        f.write("\n")
    n = json.dumps(manifest, ensure_ascii=False).count('"type": "file"')
    print(f"manifest.json 생성 완료 (파일 {n}개)")


if __name__ == "__main__":
    sys.exit(main())
