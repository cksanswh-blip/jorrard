#!/usr/bin/env python3
"""Orang정보총망라 로드맵 탭 → git 투영 · 소급 이력 도구.

정본은 시트다. git 은 시트의 투영과 이력만 갖는다(시트 → git 한 방향).

  export   XLSX            작업트리에 TSV·SUMMARY.md 를 쓴다(커밋 안 함)
  backfill XLSX           작성·수정일 하루 1커밋의 소급 사슬을 부모 없이 만들고 끝 SHA 를 출력한다.
                          현재 브랜치에는 `git merge --allow-unrelated-histories <SHA>` 로 붙인다
  sync     XLSX           HEAD 의 TSV 와 비교해 바뀐 행만 그 행의 날짜로 소급 커밋한다(정기 갱신용)

XLSX 는 구글 시트 「파일 → 다운로드 → Microsoft Excel」 로 받은 파일이다.
공개 저장소를 전제로 기본 마스킹이 켜져 있다. 비공개 저장소에서만 --no-redact 를 쓴다.
"""
import argparse
import collections
import datetime as dt
import os
import re
import subprocess
import sys
import tempfile

OUT_DIR = "orangpro/roadmap"
KST = "+0900"

# 탭 이름 → (저장 파일명, 날짜 열 이름)
TABS = {
    "로드맵": ("로드맵.tsv", "작성·수정일"),
    "로드맵(미래)": ("로드맵_미래.tsv", "작성·수정일"),
}

AUTHOR = ("Orang정보총망라 (시트 소급)", "roadmap@orangpro.invalid")
COMMITTER = ("Claude", "noreply@anthropic.com")
TRAILER = (
    "\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\n"
    "Claude-Session: https://claude.ai/code/session_01F3Wvgo5RLKV6FLU27p5JZv\n"
)

# ── 마스킹 ───────────────────────────────────────────────────────────────
# 공개 저장소에 나가면 안 되는 것만 가린다. 해시(sha16)·WP 페이지 번호·파일명은 남긴다.
REDACT = [
    (re.compile(r"AKfyc[\w-]+"), "[GAS배포ID]"),
    (re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"), "[이메일]"),
    (re.compile(r"\b19\d\d-\d\d-\d\d\b"), "[생년월일]"),
    (re.compile(r"\b4-\d{4}-\d{6}-\d\b"), "[특허고객번호]"),
    (re.compile(r"\b\d{3}-\d{2}-\d{5}\b"), "[사업자등록번호]"),
    # 드라이브·시트 ID: 영문·숫자가 섞인 28자 이상의 연속 토큰
    (re.compile(r"(?<![\w/.-])(?=[\w-]*\d)(?=[\w-]*[A-Za-z])[\w-]{28,}(?![\w.])"), "[드라이브ID]"),
]

# 실명처럼 코드에 적으면 그 자체로 노출되는 규칙은 커밋하지 않는 로컬 파일에 둔다.
# 한 줄에 「정규식<TAB>바꿀말」. 파일은 .gitignore 에 걸려 있다.
LOCAL_RULES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "redact_local.tsv")
if os.path.exists(LOCAL_RULES):
    with open(LOCAL_RULES, encoding="utf-8") as _f:
        for _ln in _f:
            if _ln.strip() and not _ln.startswith("#") and "\t" in _ln:
                _p, _r = _ln.rstrip("\n").split("\t", 1)
                REDACT.append((re.compile(_p), _r))


def redact(s):
    for pat, rep in REDACT:
        s = pat.sub(rep, s)
    return s


# ── 읽기 ─────────────────────────────────────────────────────────────────
def cell(v):
    if v is None:
        return ""
    if isinstance(v, bool):
        return str(v)
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    if isinstance(v, dt.datetime):
        return v.strftime("%Y-%m-%d %H:%M")
    s = str(v).strip()
    return s.replace("\r\n", "\n").replace("\n", " ⏎ ").replace("\t", "    ")


def parse_when(s):
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try:
            return dt.datetime.strptime(s[:19].strip(), fmt)
        except ValueError:
            pass
    return None


def load(xlsx, do_redact):
    """탭별 (header, rows) 를 돌려준다. rows 는 번호 순 (key, cells, when)."""
    try:
        import openpyxl
    except ImportError:
        sys.exit("openpyxl 이 필요하다: pip install openpyxl")
    wb = openpyxl.load_workbook(xlsx, read_only=True, data_only=True)
    out = {}
    for tab, (_, date_col) in TABS.items():
        if tab not in wb.sheetnames:
            continue
        it = wb[tab].iter_rows(values_only=True)
        header = [cell(c) for c in next(it)]
        while header and not header[-1]:
            header.pop()
        width = len(header)
        di = header.index(date_col)
        rows, last_when = [], None
        for raw in it:
            cells = [cell(c) for c in list(raw)[:width]]
            cells += [""] * (width - len(cells))
            if not any(cells):
                continue
            if do_redact:
                cells = [redact(c) for c in cells]
            when = parse_when(cells[di]) if cells[di] else None
            # 날짜가 빈 행은 시트에서 바로 앞 행의 날짜를 물려받는다(번호가 곧 기입 순서라는 가정)
            if when is None:
                when = last_when
            else:
                last_when = when
            rows.append([cells[0], cells, when])
        first = next((r[2] for r in rows if r[2]), dt.datetime(2026, 7, 1))
        for r in rows:
            r[2] = r[2] or first
        rows.sort(key=lambda r: (int(r[0]) if r[0].isdigit() else 10**9, r[0]))
        out[tab] = (header, rows)
    return out


def render(header, rows):
    lines = ["\t".join(header)] + ["\t".join(r[1]) for r in rows]
    return "\n".join(lines) + "\n"


def read_tsv(path):
    if not os.path.exists(path):
        return None, {}
    with open(path, encoding="utf-8") as f:
        lines = f.read().rstrip("\n").split("\n")
    header = lines[0].split("\t")
    rows = {}
    for ln in lines[1:]:
        cells = ln.split("\t")
        rows[cells[0]] = cells
    return header, rows


# ── 요약 ─────────────────────────────────────────────────────────────────
def status_bucket(s):
    if s.startswith("✅") or s.startswith("완료") or "완료(" in s[:8]:
        return "✅ 완료"
    if "진행" in s or s.startswith("🔧") or s.startswith("부분") or "운영중" in s:
        return "🔧 진행·운영"
    if s.startswith("⏳") or "준비" in s or "대기" in s or s.startswith("계획"):
        return "⏳ 준비·대기·계획"
    if "사고" in s or "⚠" in s or "점검" in s:
        return "⚠️ 점검·사고"
    return "· 기타"


def summary(data):
    L = ["# 로드맵 요약 (자동 생성 — 손으로 고치지 않는다)", ""]
    L.append("`python3 tools/roadmap_git.py export|sync` 가 매번 다시 쓴다. 정본은 시트 `Orang정보총망라`.")
    L.append("")
    if "로드맵" in data:
        header, rows = data["로드맵"]
        L += [f"## 로드맵 — {len(rows)}행 (구현·완료 이력)", ""]
        months = collections.Counter(r[2].strftime("%Y-%m") for r in rows)
        L += ["| 월 | 행 |", "| :-- | --: |"] + [f"| {m} | {n} |" for m, n in sorted(months.items())]
        L.append("")
        st = collections.Counter(status_bucket(r[1][4]) for r in rows)
        L += ["| 상태 | 행 |", "| :-- | --: |"] + [f"| {k} | {v} |" for k, v in st.most_common()]
        L.append("")
        area = collections.Counter(r[1][1] for r in rows)
        L += ["| 영역 (상위 25) | 행 |", "| :-- | --: |"] + [f"| {k} | {v} |" for k, v in area.most_common(25)]
        L.append("")
        L += ["### 최근 20행", "", "| 번호 | 영역 | 컴포넌트·기능 | 상태 | 날짜 |", "| --: | :-- | :-- | :-- | :-- |"]
        for r in sorted(rows, key=lambda r: r[2])[-20:][::-1]:
            c = r[1]
            L.append(f"| {c[0]} | {c[1]} | {c[2][:60]} | {c[4][:20]} | {r[2]:%Y-%m-%d} |")
        L.append("")
    if "로드맵(미래)" in data:
        header, rows = data["로드맵(미래)"]
        L += [f"## 로드맵(미래) — {len(rows)}행 (계획·기둥)", ""]
        pr = collections.Counter(r[1][5] or "·" for r in rows)
        L += ["| 우선순위 | 행 |", "| :-- | --: |"] + [f"| {k} | {v} |" for k, v in sorted(pr.items())]
        L.append("")
        L += ["### 열린 P0", "", "| 번호 | 기둥 | 핵심 기능 | 상태 |", "| --: | :-- | :-- | :-- |"]
        for r in rows:
            c = r[1]
            if c[5] == "P0" and status_bucket(c[6]) != "✅ 완료":
                L.append(f"| {c[0]} | {c[1]} | {c[2][:50]} | {c[6][:40]} |")
        L.append("")
    return "\n".join(L)


# ── git ──────────────────────────────────────────────────────────────────
def git(*args, env=None, input=None):
    e = dict(os.environ)
    if env:
        e.update(env)
    r = subprocess.run(["git", *args], env=e, input=input, capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"git {' '.join(args)} 실패: {r.stderr.strip()}")
    return r.stdout.strip()


def dated_env(when):
    stamp = when.strftime("%Y-%m-%dT%H:%M:00") + KST
    return {
        "GIT_AUTHOR_NAME": AUTHOR[0], "GIT_AUTHOR_EMAIL": AUTHOR[1], "GIT_AUTHOR_DATE": stamp,
        "GIT_COMMITTER_NAME": COMMITTER[0], "GIT_COMMITTER_EMAIL": COMMITTER[1], "GIT_COMMITTER_DATE": stamp,
    }


def day_message(kind, day, added, changed, areas):
    parts = []
    for tab in TABS:
        a, c = added.get(tab, 0), changed.get(tab, 0)
        if a or c:
            parts.append(f"{tab} " + " · ".join(x for x in (f"+{a}" if a else "", f"~{c}" if c else "") if x))
    head = f"로드맵 {kind} {day}: " + " / ".join(parts)
    top = ", ".join(f"{k} {v}" for k, v in areas.most_common(4))
    body = (
        f"\n\n영역: {top}\n\n"
        "시트 작성·수정일 기준 소급. 행은 그 날짜의 마지막 수정 내용으로 들어간다 —\n"
        "시트는 행별 수정 이력을 남기지 않으므로 중간 판본은 복원할 수 없다."
    )
    return head + body + TRAILER


def cmd_export(a):
    data = load(a.xlsx, not a.no_redact)
    os.makedirs(OUT_DIR, exist_ok=True)
    for tab, (header, rows) in data.items():
        with open(os.path.join(OUT_DIR, TABS[tab][0]), "w", encoding="utf-8") as f:
            f.write(render(header, rows))
        print(f"{tab}: {len(rows)}행")
    with open(os.path.join(OUT_DIR, "SUMMARY.md"), "w", encoding="utf-8") as f:
        f.write(summary(data))


def cmd_backfill(a):
    data = load(a.xlsx, not a.no_redact)
    by_day = collections.defaultdict(list)  # day -> [(tab, row)]
    for tab, (_, rows) in data.items():
        for r in rows:
            by_day[r[2].date()].append((tab, r))
    state = {tab: [] for tab in data}
    parent = None
    with tempfile.TemporaryDirectory() as td:
        idx = {"GIT_INDEX_FILE": os.path.join(td, "index")}
        for day in sorted(by_day):
            added, areas = collections.Counter(), collections.Counter()
            latest = max(r[2] for _, r in by_day[day])
            for tab, r in by_day[day]:
                state[tab].append(r)
                added[tab] += 1
                areas[r[1][1]] += 1
            for tab, rows in state.items():
                if not rows:
                    continue
                rows.sort(key=lambda r: (int(r[0]) if r[0].isdigit() else 10**9, r[0]))
                blob = git("hash-object", "-w", "--stdin", input=render(data[tab][0], rows))
                git("update-index", "--add", "--cacheinfo", f"100644,{blob},{OUT_DIR}/{TABS[tab][0]}", env=idx)
            tree = git("write-tree", env=idx)
            args = ["commit-tree", tree, "-m", day_message("소급", day, added, {}, areas)]
            if parent:
                args[2:2] = ["-p", parent]
            parent = git(*args, env=dated_env(latest))
            print(f"{day}  {sum(added.values()):>3}행  {parent[:10]}")
    print(parent)


def cmd_sync(a):
    data = load(a.xlsx, not a.no_redact)
    if git("status", "--porcelain", "--", OUT_DIR):
        sys.exit(f"{OUT_DIR} 에 커밋 안 된 변경이 있다. 먼저 정리한다.")
    plan = collections.defaultdict(list)  # day -> [(tab, row, is_new)]
    removed = {}
    current = {}
    for tab, (header, rows) in data.items():
        path = os.path.join(OUT_DIR, TABS[tab][0])
        _, old = read_tsv(path)
        current[tab] = dict(old)
        new_keys = set()
        for r in rows:
            new_keys.add(r[0])
            if old.get(r[0]) != r[1]:
                plan[r[2].date()].append((tab, r, r[0] not in old))
        removed[tab] = sorted(set(old) - new_keys, key=lambda k: int(k) if k.isdigit() else 10**9)
    if not plan and not any(removed.values()):
        print("바뀐 행 없음")
        return
    for day in sorted(plan):
        n = collections.Counter(("신규" if new else "수정") for _, _, new in plan[day])
        print(f"{day}  신규 {n['신규']} · 수정 {n['수정']}")
    for tab, ks in removed.items():
        if ks:
            print(f"{tab}: 시트에서 사라진 행 {len(ks)} — {', '.join(ks[:10])}")
    if a.dry_run:
        return

    def write(tab):
        header = data[tab][0]
        rows = sorted(current[tab].items(), key=lambda kv: int(kv[0]) if kv[0].isdigit() else 10**9)
        with open(os.path.join(OUT_DIR, TABS[tab][0]), "w", encoding="utf-8") as f:
            f.write("\n".join(["\t".join(header)] + ["\t".join(v) for _, v in rows]) + "\n")

    os.makedirs(OUT_DIR, exist_ok=True)
    for day in sorted(plan):
        added, changed, areas = collections.Counter(), collections.Counter(), collections.Counter()
        latest = max(r[2] for _, r, _ in plan[day])
        for tab, r, new in plan[day]:
            current[tab][r[0]] = r[1]
            (added if new else changed)[tab] += 1
            areas[r[1][1]] += 1
        for tab in {t for t, _, _ in plan[day]}:
            write(tab)
        git("add", OUT_DIR)
        git("commit", "-q", "-m", day_message("동기화", day, added, changed, areas), env=dated_env(latest))
    if any(removed.values()):
        for tab, ks in removed.items():
            for k in ks:
                current[tab].pop(k, None)
            write(tab)
        git("add", OUT_DIR)
        msg = "로드맵 동기화: 시트에서 사라진 행 반영\n\n" + "\n".join(
            f"{t}: {', '.join(ks)}" for t, ks in removed.items() if ks) + TRAILER
        git("commit", "-q", "-m", msg)
    with open(os.path.join(OUT_DIR, "SUMMARY.md"), "w", encoding="utf-8") as f:
        f.write(summary(data))
    if git("status", "--porcelain", "--", OUT_DIR):
        git("add", OUT_DIR)
        git("commit", "-q", "-m", "로드맵 요약 갱신" + TRAILER)
    print("완료 — git log --date=iso -- orangpro/roadmap 로 확인")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    for name, fn in (("export", cmd_export), ("backfill", cmd_backfill), ("sync", cmd_sync)):
        s = sub.add_parser(name)
        s.add_argument("xlsx")
        s.add_argument("--no-redact", action="store_true", help="마스킹 끔 — 비공개 저장소에서만")
        if name == "sync":
            s.add_argument("--dry-run", action="store_true")
        s.set_defaults(fn=fn)
    a = p.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
