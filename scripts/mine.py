#!/usr/bin/env python3
"""HARNESS evolution loop, stage 1: mine correction signals.

Extracts the user's short messages from recent Claude Code transcripts
(plus Codex history) and buckets them into corrections/approvals.

Usage: python3 mine.py [--days 7] [--max-len 500]
Env:   MINE_DIR to override the Claude Code projects dir.
Korean patterns ship as defaults; English patterns included. Edit CORRECTION_PATTERNS for your own voice.
"""

def _default_projects_dir():
    import glob as _g
    base = os.path.expanduser("~/.claude/projects")
    cands = sorted(_g.glob(base + "/*"), key=lambda d: sum(os.path.getsize(f) for f in _g.glob(d + "/*.jsonl")) if _g.glob(d + "/*.jsonl") else 0, reverse=True)
    return cands[0] if cands else base

import json, os, glob, re, sys, time, argparse

DIR = os.environ.get("MINE_DIR") or _default_projects_dir()

CORRECTION_PATTERNS = [
    ("incomplete (EN)", r"(?i)\bstill (not|broken|missing|the same)\b|\bnot (fixed|working|deployed)\b"),
    ("why (EN)", r"(?i)^why (did|didn't|is|isn't|do|don't)"),
    ("redo (EN)", r"(?i)^(again|redo|do it again|revert)\b"),
    ("quality (EN)", r"(?i)\b(ugly|looks (bad|off|wrong)|amateur|generic)\b"),
    ("미완/미반영", r"아직 .*(안|못|그대로)|안 됐|안 됨|반영이 안"),
    ("재작업", r"^다시|다시 ?(해|만들|그|되돌)"),
    ("근거 추궁", r"^왜 |왜 .*(했|안 |못 )"),
    ("의도 오해", r"^아니|그게 아니라|아닌데"),
    ("품질 불만", r"어색|촌스|별로|이상해|구려|엉망|올드|저급|AI ?티|티 ?나"),
    ("깨짐/오류", r"깨졌|깨져|에러|오류|안 보여|안 나와|안 열려"),
    ("금지 표현", r"박다|박는|박음|쓰지 ?마|표현"),
    ("책임/자율성", r"책임|한심|니가 알아서|알아서 해"),
    ("확인 요구", r"확인해|체크|봐봐|테스트"),
]
APPROVAL = r"(?i)^(좋아|고|ㄱ|ㄱㄱ|진행|계속|해줘|해라|ㅇㅋ|오케이|ok|okay|yes|yep|go|go ahead|do it|ship it|lgtm|응|어|넵|네|그래|일단 해)"

def text_from_content(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if not isinstance(block, dict):
                return None
            t = block.get("type")
            if t == "text":
                parts.append(block.get("text", ""))
            else:
                return None
        if parts:
            return "\n".join(parts)
    return None

def is_noise(txt):
    if txt is None:
        return True
    s = txt.strip()
    if not s:
        return True
    for marker in ("<system-reminder>", "<command-", "<local-command", "tool_use_id",
                   "[Request interrupted", "This session is being continued", "<task-notification>",
                   "<teammate-message"):
        if marker in s:
            return True
    if s.startswith("Caveat:") or s.startswith("<user-memory"):
        return True
    # Automation artifacts are not the human voice: scheduled check-in prompts, CONTEXT reinjection, quoted emails
    if s.startswith("[자동") or s.startswith("CONTEXT:") or "--- Original Message ---" in s:
        return True
    return False

def classify(txt, corrections, approvals, others, source=""):
    tag = f"[{source}] " if source else ""
    if re.match(APPROVAL, txt):
        approvals.append(tag + txt)
        return
    for theme, pat in CORRECTION_PATTERNS:
        if re.search(pat, txt):
            corrections.append((theme, tag + txt))
            return
    others.append(tag + txt)

def mine_codex(days, max_len, corrections, approvals, others):
    """Mine user inputs from Codex CLI sessions (~/.codex/history.jsonl)."""
    path = os.path.expanduser("~/.codex/history.jsonl")
    if not os.path.exists(path):
        return
    cutoff = time.time() - days * 86400
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            if obj.get("ts", 0) < cutoff:
                continue
            txt = (obj.get("text") or "").strip()
            if not txt or len(txt) > max_len or is_noise(txt):
                continue
            classify(txt, corrections, approvals, others, source="codex")

def mine(days, max_len):
    cutoff = time.time() - days * 86400
    files = [f for f in glob.glob(os.path.join(DIR, "*.jsonl")) if os.path.getmtime(f) >= cutoff]
    corrections, approvals, others = [], [], []
    mine_codex(days, max_len, corrections, approvals, others)
    for f in sorted(files, key=os.path.getmtime):
        try:
            fh = open(f, encoding="utf-8")
        except OSError:
            continue
        with fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue
                m = obj.get("message")
                if not isinstance(m, dict) or m.get("role") != "user":
                    continue
                txt = text_from_content(m.get("content"))
                if is_noise(txt):
                    continue
                txt = txt.strip()
                if not txt or len(txt) > max_len:
                    continue
                classify(txt, corrections, approvals, others)
    return corrections, approvals, others

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=7)
    ap.add_argument("--max-len", type=int, default=500)
    args = ap.parse_args()
    corrections, approvals, others = mine(args.days, args.max_len)
    n_corr, n_appr = len(corrections), len(approvals)
    ratio = f"1 : {n_appr / n_corr:.1f}" if n_corr else "no corrections"
    print(f"# Mining report (last {args.days} days)")
    print(f"\ncorrections {n_corr} / approvals {n_appr} / ratio {ratio}")
    print("(Set your own baseline after the first full-history run; a worsening ratio = harness regression signal)\n")
    by_theme = {}
    for theme, txt in corrections:
        by_theme.setdefault(theme, []).append(txt)
    for theme, items in sorted(by_theme.items(), key=lambda kv: -len(kv[1])):
        print(f"## {theme} ({len(items)}건)")
        seen = set()
        for t in items:
            key = t[:60]
            if key in seen:
                continue
            seen.add(key)
            print(f"- {t[:200]}")
        print()

if __name__ == "__main__":
    main()
