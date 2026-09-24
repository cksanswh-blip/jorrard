# orangpro/ — 로드맵(git 정본은 orangpro-roadmap)과 2.0 동시 준비

| 경로 | 무엇 |
| :-- | :-- |
| `2.0_지원사업_동시준비.md` | ⭐ 오랑프로 2.0(11/1)과 자금·행정 레인을 한 줄로 묶은 주차별 계획 |
| `roadmap/` | (없음) 정본 TSV 는 비공개 저장소 `orangpro-roadmap` 에 — **아래 「현황」 참고** |
| `../tools/roadmap_git.py` | 로드맵 기입(`add`)·검사(`check`)·요약(`summary`)·시트 가져오기(`sync`) 도구 — 사본 |
| `../roadmap/` | 청년 창업 지원·세액감면·이전·자금 캘린더 판정 문서(2026-09-19~) |

**정본은 git 이다(2026-09-24부터).** 시트는 거울. 쓰기는 `orangpro-roadmap` 에서 `add` 로, 시트에는 붙여넣기(번호 N = 시트 N+1 행)로 맞춘다.

---

## 현황 — 로드맵 정본은 비공개 저장소 `orangpro-roadmap` 의 git 이다 (2026-09-24)

**2026-09-24 대표 결정: 로드맵의 정본은 시트가 아니라 git 이다.** 정본 TSV 3장(`로드맵` 527행 · `로드맵(미래)` 126행 · `총책임자전용_100억` 77행)과 2026-07-25 부터의 날짜별 이력은 **비공개 저장소 `cksanswh-blip/orangpro-roadmap`** `main` 에 있다. 시트 `Orang정보총망라`·`총책임자전용` 은 사람이 보는 거울이고, git 에 넣은 행을 붙여넣어 맞춘다.

**앞으로의 기입은 그쪽에서** `python3 tools/roadmap_git.py add <탭> <델타.tsv>` 한 줄로 한다(검사 → 행 날짜별 커밋 → 요약 갱신). 이 저장소(`jorrard`)는 공개라 시트 데이터를 두지 않는다. 여기 `roadmap/` 의 델타 TSV·판정 문서와 `tools/roadmap_git.py` 는 같은 판본의 사본이다.

## 소급 방식 — 무엇이 되고 무엇이 안 되나

- **하루 1커밋.** 각 행의 `작성·수정일` 날짜로 묶고, 커밋 시각을 그날 가장 늦은 행 시각(KST)으로 찍는다. `git log` 가 2026-07-25부터 날짜순으로 읽힌다
- **`git blame` 이 행마다 그 행이 들어온 날의 커밋을 가리킨다**
- **부모 없는 사슬로 만들고 병합으로 붙인다.** 기존 커밋을 다시 쓰지 않으므로 강제 푸시가 필요 없다
- ⚠️ 시트는 행별 수정 이력을 남기지 않는다. `작성·수정일`은 **마지막 수정일**이라, 7월에 쓰고 9월에 고친 행은 **9월에 처음 등장**한다. 중간 판본은 복원할 수 없다
- ⚠️ 날짜가 빈 행은 시트에서 **바로 앞 행의 날짜를 물려받는다**(번호가 곧 기입 순서라는 가정)
- 셀 안 줄바꿈은 ` ⏎ `, 탭은 공백 4칸으로 바뀐다

## 실행 절차

시트에서 **파일 → 다운로드 → Microsoft Excel(.xlsx)** 로 받는다. `pip install openpyxl` 한 번.

```bash
# ① 1회 — 소급 이력 만들기
python3 tools/roadmap_git.py backfill 로드맵.xlsx          # 날짜별 커밋 목록과 끝 SHA 출력
git merge --allow-unrelated-histories --no-ff <끝SHA> -m "로드맵 소급 이력 병합"
python3 tools/roadmap_git.py export 로드맵.xlsx            # SUMMARY.md 생성
git add orangpro/roadmap && git commit -m "로드맵 요약"

# ② 이후 — /org:save 로 시트를 고칠 때마다
python3 tools/roadmap_git.py sync 로드맵.xlsx --dry-run    # 무엇이 바뀌나 먼저 본다
python3 tools/roadmap_git.py sync 로드맵.xlsx              # 바뀐 행만 그 행의 날짜로 커밋

# 확인
git log --date=iso -- orangpro/roadmap
git blame orangpro/roadmap/로드맵.tsv
```

`sync` 는 새 행·고친 행을 **각 행의 날짜로** 커밋하고, 시트에서 사라진 행은 따로 한 커밋으로 남긴다. 바뀐 게 없으면 아무것도 하지 않는다.

## 마스킹

공개 저장소를 전제로 **기본으로 켜져 있다.** 가리는 것: GAS 배포 ID · 이메일 · 1900년대 생년월일 · 특허고객번호 · 사업자등록번호 · 영문·숫자 섞인 28자 이상 토큰(드라이브·시트 ID). sha16 해시·WP 페이지 번호·파일명은 남긴다.

**실명처럼 규칙 자체가 노출인 것**은 `tools/redact_local.tsv`(커밋 안 됨, `.gitignore`)에 한 줄씩 `정규식<TAB>바꿀말` 로 넣는다.

비공개 저장소에서는 `--no-redact` 로 원문 그대로 둘 수 있다.
