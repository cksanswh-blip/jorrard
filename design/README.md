# OrangPro 웹디자인 고도화 × 디자인 레퍼런스 MCP (2026-09-21)

대표님 지시: 릴스에 나온 디자인 레퍼런스 MCP 5종(Mobbin · Nicelydone · Refero · Lazyweb · InspoAI)을 붙여 오랑프로 웹디자인을 고도화한다.

이 폴더는 그 작업의 **진입점**이다. 세 파일이 한 세트다.

| 파일 | 역할 |
| :-- | :-- |
| `README.md` (이 문서) | MCP 설치·인증·요금 · 제1법 아래에서 레퍼런스를 쓰는 규율 · 작업 루프 |
| `DESIGN.md` | **오랑프로 현행 디자인 시스템 기준선**. MCP가 뽑아 주는 레퍼런스 DESIGN.md와 **이것을 대조**한다 |
| `2026-09-21_고도화_백로그.md` | 화면별 조사 질의 · 뽑아 올 것 · 손대면 안 되는 것 · 검증 기준 |
| `무료_확장.md` | **무료로 할 수 있는 것** 전수 조사(2026-09-21): DESIGN.md 컬렉션 · 공식 스킬 · 자기 사이트 검증 MCP · Stitch |
| `reference/awesome-design-md/` | 오랑 대조용으로 고른 실제 사이트 DESIGN.md 8개 (MIT, VoltAgent) |
| `../.claude/skills/frontend-design/` | Anthropic 공식 frontend-design 스킬 (Apache 2.0). 이 저장소를 열면 자동 로드 |
| `../.mcp.json` | 이 저장소를 cwd로 열면 레퍼런스 6개 + 검증 2개(chrome-devtools·playwright) 서버가 자동 등록된다 |

제1법 로드됨(**v2.2 통합정본 + v2.4 개정부록, v2.5 제21조 포함**). 정본 시트(`OrangPro_원전_정본`) 165행 로드됨.
⚠️ 스킬 `orangpro` §0-A는 아직 "최신 = v1.5"로 적혀 있다. 드라이브 실측은 v2.2 통합정본(ID `1WGKc9XL0YpdOFR0SCU9UjLoYD-sW3VLm`) + v2.4 부록(ID `1pFg5WQoLDida8acctPhzmM7mjBc8p487`)이 최신이다. 스킬 갱신은 대표님 판단.

---

## 0. 먼저 알아야 할 것 (정직히)

1. **이 세션(클라우드)에는 다섯 MCP가 하나도 연결돼 있지 않다.** 릴스의 토글은 대표님 로컬 Claude Code(또는 claude.ai 커넥터)에서 켜는 것이다. 이 세션이 한 일은 **설정 파일과 작업 규율을 만드는 것**까지다. 실제 레퍼런스 조회·화면 제작은 MCP가 켜진 로컬 세션에서 한다.
2. **레퍼런스 MCP는 "무엇을 고칠지"를 찾는 도구지, 오랑을 남의 앱처럼 바꾸는 도구가 아니다.** 제1법 제1조 1항(동일성)과 「페이지 제목·파비콘 불가침」이 그대로 살아 있다. §2의 불변 목록을 먼저 읽는다.
3. 다섯 중 **셋은 유료 구독이 전제**다(Mobbin · Nicelydone · Refero 공식). Lazyweb과 오픈소스 Inspo는 무료다. 결제는 대표님 결정이므로 여기서는 **무료 2종으로 먼저 돌리고**, 효용이 확인되면 유료를 붙이는 순서를 권한다.
4. 공식 페이지 5곳(docs.mobbin.com · nicelydone.club · doc.refero.design · lazyweb.com · inspoai.io)이 이 환경의 이그레스 정책에 막혀 **직접 읽지 못했다.** 아래 표의 "검증" 열이 1차 출처를 봤는지 여부다. 미검증 항목은 **설치 전에 공식 페이지에서 한 번 대조**한다.

---

## 1. MCP 6종 설치·인증·요금

`.mcp.json`에 6개를 넣었다. 릴스의 5개 + 오픈소스 Inspo 1개(무료·MIT). InspoAI(inspoai.io, 유료 서비스)와 Inspo(Nutlope, 오픈소스)는 **이름만 비슷한 다른 물건**이다.

| 서버 | 무엇을 주나 | 설치 (Claude Code) | 인증 | 요금 | 검증 |
| :-- | :-- | :-- | :-- | :-- | :-- |
| **Mobbin** | 실제 출시 앱 60만+ 화면·플로우. 모바일 강함 | `claude mcp add mobbin --scope user --transport http https://api.mobbin.com/mcp` → 새 세션에서 `/mcp` → mobbin → Authenticate(브라우저 OAuth) | Mobbin 계정 OAuth | **유료 플랜 필수** (Pro 월 $10 안내) | 엔드포인트·명령은 2차 출처 3곳 일치. claude.ai 커넥터 디렉터리에도 `Mobbin`(tools: search_flows · search_screens · search_sections) 등재 확인 |
| **Nicelydone** | SaaS 웹앱 14만+ 화면·플로우·컴포넌트. **웹 대시보드형에 가장 가깝다** | `claude mcp add --transport http nicelydone https://nicelydone.club/mcp` | 계정 로그인(별도 키 없음) | **Pro 구독 필수** | ⚠️ **미검증**. URL은 검색 요약이 추정한 값. nicelydone.club/mcp 의 "Install" 스니펫을 복사해 `.mcp.json`의 `nicelydone.url`을 덮어쓸 것 |
| **Refero** (커뮤니티 래퍼) | styles.refero.design 큐레이션 약 200사이트의 **DESIGN.md**(색·타이포·간격·do/don't) | `claude mcp add refero -- npx -y fidgetcoding-refero-mcp` | 없음. `OPENAI_API_KEY`(선택, 시맨틱 검색) · `REFERO_MCP_VAULT_DIR`(선택, DESIGN.md 파일 저장 위치) | 무료 (npm `fidgetcoding-refero-mcp` v0.2.0, MIT) | ✅ npm + GitHub README 확인, **이 세션에서 stdio 기동 확인**(7 tools). `.mcp.json`에서 빈 `REFERO_MCP_VAULT_DIR` 치환이 오류를 내 제거함. 6 tools: refero_search · refero_get · refero_similar · refero_list · refero_facets · refero_design_md |
| Refero **공식** MCP | Refero 본 라이브러리(화면 스크린샷) | doc.refero.design/mcp/getting-started 참조 | Refero 계정 | 유료 | ⚠️ 미검증(문서 차단). 커뮤니티 래퍼로 먼저 쓰고 필요하면 교체 |
| **Lazyweb** | 25.7만 화면 + A/B 실험 데이터 + 디자인 스킬 6종 | `curl -fsSL https://www.lazyweb.com/install.sh \| bash` (실행 전 스크립트를 열어 읽는다) → `~/.lazyweb/lazyweb_mcp_token` 생성 → `export LAZYWEB_MCP_TOKEN=$(cat ~/.lazyweb/lazyweb_mcp_token)` | Bearer 토큰(자동 발급) | **무료(조건부)**. 설치·토큰은 무료, 데이터 툴은 플랜을 따른다는 문구가 README에 있어 설치 후 검색 1회로 확인 | ✅ GitHub `aboul3ata/lazyweb-skill` README 직접 확인. HTTP `https://www.lazyweb.com/mcp`. tools: lazyweb_search_screens · search_flows · search_experiments · compare_image · growth_score. 스킬 `/lazyweb-apply-design-best-practices` |
| **InspoAI** (inspoai.io) | 9.2만 UI 스크린샷 + 웹 인스피레이션, 3 tools | `.mcp.json`의 `inspoai` 항목. 키는 app.inspoai.io/mcp 에서 발급 → `export INSPOAI_API_KEY=...` | API 키 | 무료 플랜 있음 | ⚠️ **미검증**. 검색 요약은 `npx -y @inspoai/mcp`라 했으나 **npm 레지스트리에 그 패키지가 없다**(2026-09-21 조회). 공식 페이지의 스니펫으로 `command/args`를 교체할 것 |
| **Inspo** (Nutlope, 오픈소스) | 실제 출시 832사이트·2,320페이지. 사이트별 DESIGN.md · 팔레트 · **find_by_color(hex)** · 데스크톱+모바일 쌍 | `claude mcp add --transport http inspo https://inspomcp.dev/api/mcp` 또는 `npx -y inspo-mcp install` | 없음 | **무료·MIT** | ✅ npm `inspo-mcp` v0.1.16 + GitHub README 직접 확인. 15 tools(search_screens · recommend · get_design_system · compare · find_by_color · find_similar · find_components …) |

### 권장 착수 순서

1. **무료 2종부터**: Inspo(웹 랜딩·디자인시스템·색 매칭) + Lazyweb(화면·플로우·A/B 근거). 둘 다 계정 없이 5분.
2. Refero 커뮤니티 래퍼(무료)로 **DESIGN.md 대조 루프**를 익힌다(§3).
3. 효용이 보이면 **Nicelydone**(웹앱 대시보드·필터·빈 상태 레퍼런스가 오랑 메인 피드와 가장 가깝다) → Mobbin(모바일 하단 탭바·온보딩) 순으로 유료 결제 판단.

### 등록 확인

```
claude mcp list
```
6개가 `connected`로 보여야 한다. 미검증 2개(nicelydone · inspoai)는 실패할 수 있으니 공식 스니펫으로 교체한 뒤 재확인.

---

## 2. 불변 목록: 레퍼런스가 뭐라 하든 바꾸지 않는 것

MCP가 "요즘 앱은 이렇게 한다"고 보여 줘도 아래는 그대로다. 제1법 조문 번호를 병기한다.

| 불변 | 근거 |
| :-- | :-- |
| 상단 OrangPro 로고 바, 좌·우·하단 툴바의 **모양·hover·active·전환** | 제1조 1항, 제11-1 |
| 브랜드 토큰(오랑 `#f97316`·`#ea580c`·`#fff7ed` / 다크 `#191f28` / 잉크 `#0f172a` / 기관색 4종) | 제5조 1항, 시트 11행 |
| 브랜드 3층 경계(본사 에메랄드 / 오랑 오렌지 / 개인 자체). 오랑 연출이 본사에 새면 위반 | 제1조 6항 |
| 페이지 제목 4종 · 파비콘 `opfavi` | 「제목·파비콘 불가침」(잠금) |
| 로그인/가입 = **그 자리 모달**, 이동 없음. 성공 후 그 페이지 새로고침 | 제2조 10항, 제21조 3항 |
| 팝업 6대 표준(body 직속·fixed 정중앙·균일 딤·배경/× 닫힘·등장 애니·불필요 로더 없음). 네이티브 confirm/alert 금지 | 제2조 8항 |
| **잔상 금지**. 클릭 후 흔적은 상태 표시가 아니면 제거 | 제3조 1항 |
| 툴바 버튼 3상태(활성/잠김 자물쇠/없음 미렌더). **흐림 폐기** | 제3조 12항 |
| 발바닥·로고·파비콘은 정본에서만(page 6245 PAW 상수 · media 5615). 임의로 그리지 않는다 | 시트 156행 |
| em dash(전각 대시) 사용 금지. 읽는 시간 같은 장식 수치 금지 | 시트 104·105행 |
| 수치 하드코딩 금지(REST 실시간) | 제4조 7항 |
| 로그인 뒤에서 그리는 화면은 크롤 경로가 아니다. SEO 노출은 서버 HTML에 문자로 | 제21조(v2.5) |
| 정본 1곳 수정 원칙(툴바 4종·오랑픽 셸 page 6245·로그인 공통 블록). 개별 글 수정 금지 | 제11-1, 시트 94행 |

### 대표님 취향 필터 (시트 118행 「Jay의 취향 요약」)

레퍼런스를 고를 때 이 필터를 먼저 건다. 걸리지 않는 건 보여 주지도 않는다.

- 구성보다 **디테일**. 여백·위계·**순차 등장** 연출을 중시.
- 결론 앞세운 제목, AI 상투어(em dash) 즉시 알아봄.
- 장식성 수치 싫어함. 강조는 절제하되 핵심에는 확실히.
- 시각 자료 자주 원함(인라인 SVG 우선).
- 구조 요소(툴바·버튼)는 폭이 변해도 배치가 흔들리지 않아야.
- **한 곳 고치면 전체 반영** 구조 선호.

---

## 3. 작업 루프: 레퍼런스에서 라이브 반영까지

제1법 제9조(요청 해석 기본값)에 MCP 단계를 끼워 넣은 것이다. 한 화면당 이 루프 1회.

```
① 기준선   design/DESIGN.md 를 읽는다 (우리 토큰·형태·모션·금지)
② 조사     MCP 3~4개에 같은 질의 → 화면 8~12장 + DESIGN.md 2~3개 확보
           · Nicelydone/Lazyweb: 화면·플로우 (구조·빈 상태·로딩·필터 UX)
           · Inspo/Refero:     DESIGN.md (간격 스케일·타입 램프·모션 규칙)
           · Inspo find_by_color("#f97316"): 오렌지 포인트를 쓰는 실제 사이트
③ 대조     레퍼런스 DESIGN.md ↔ 우리 DESIGN.md 를 표로 놓는다
           바꿀 후보 = 우리에게 없거나 약한 것 (예: 8pt 간격 스케일, 스켈레톤 규격, 빈 상태 일러스트)
           버릴 후보 = §2 불변과 충돌하는 것 (즉시 폐기, 이유 한 줄)
④ 제안서   화면 1개 = 제안 1장. "무엇을 · 왜(레퍼런스 근거) · 어디(정본 위치·마커) · 검증 기준"
           A안/B안 선택지로 대표님께 (제16조 3항 의도 파악 프로토콜)
⑤ 확정     대표님 "이대로/확정" → 시트 확정로그 1행
⑥ 집행     정본 1곳만 수정 (시트 추적맵에서 위치 확인). WP는 REST+앵커치환, 전역은 options.php POST,
           페이지 6245 셸은 base64 1줄. 배포 전 new Function 파싱 검사 (제7조 8항)
⑦ 검증     제8조 전 항목: 로그인/로그아웃 양쪽 · 실클릭 · getComputedStyle · 콘솔 0 · 부재 확인
           + 모바일 폭(≤782px · ≤1180px) 실측. Lazyweb compare_image 로 전/후 비교 가능
⑧ 기록     시트 추적맵/확정로그/현재상태 갱신 · 기능정의 시트(gid 476153821) 행 갱신 (제17조)
           · 반복 규칙이면 웹제1법 개정부록 1줄 · DESIGN.md 갱신
```

### 조사 단계 표준 질의 (복붙용)

MCP가 켜진 로컬 세션에서 그대로 쓴다. 한 화면당 세 문장이 한 세트다.

```
[화면] 오랑프로 메인 피드 (/orangpro/) 고도화 조사.
[제약] design/DESIGN.md 의 토큰·형태·모션은 고정. 툴바·로고·로그인 모달은 손대지 않는다.
[질의] Nicelydone·Lazyweb 에서 "news feed with filters, role tabs, empty state, skeleton loading" 화면 10장,
       Inspo recommend(brief="Korean education/admissions intelligence dashboard, white background, orange #f97316 accent, card feed"),
       Refero refero_search("clean SaaS dashboard, warm accent, generous whitespace").
[산출] 레퍼런스 DESIGN.md 와 우리 DESIGN.md 대조표 → 바꿀 후보 5개 이내 · 버릴 후보와 이유 → A안/B안 제안서.
```

### 산출물 저장 규약

- 조사 결과: `design/research/YYYY-MM-DD_<화면>_<MCP>.md` (스크린샷 URL·슬러그·뽑은 규칙만. 이미지 파일은 저장하지 않는다)
- 제안서: `design/proposals/YYYY-MM-DD_<화면>_제안.md` (A안/B안·근거·정본 위치·검증 기준)
- 확정된 규칙: `design/DESIGN.md` 해당 절에 반영 + 시트 `분류=스타일지침` 1행
- 드라이브 도서관 규율(제18조): 이 폴더는 **B_기록**에 준한다. 상시 자산은 시트와 DESIGN.md 뿐.

---

## 4. 이번 턴에 한 일 / 안 한 일

**한 일**
- `.mcp.json` 6개 서버 등록(환경변수 치환식). 검증 2건·미검증 2건 표기.
- `design/DESIGN.md` 현행 오랑프로 디자인 시스템 기준선을 제1법 제5조·시트 스타일지침에서 추출.
- `design/2026-09-21_고도화_백로그.md` 화면 9개 × (조사 질의 · 뽑아 올 것 · 불변 · 검증 기준).
- `roadmap/2026-09-21_로드맵미래_델타_디자인MCP.tsv` 로드맵(미래) 기입 대기 2행.

**안 한 일 (못 한 일)**
- MCP 실제 연결·조회. 이 세션에 도구가 없다.
- 라이브 화면 수정. 레퍼런스 없이 손대는 것은 이 작업의 취지와 반대다.
- 시트 쓰기. 대표님 확인 뒤 집행(저장소 규약).
- Nicelydone·InspoAI 설치 스니펫 1차 검증. 공식 페이지 차단.

**대표님 결정이 필요한 것**
1. 유료 3종(Mobbin · Nicelydone · Refero 공식) 결제 여부와 순서. 권장: 무료 2종 먼저.
2. 첫 대상 화면. 권장 1순위는 **메인 피드**(트래픽·회원 전환 지점), 2순위 **구독·결제 화면**(신규라 레퍼런스 효용 최대, 로드맵 유료 구독 예정과 맞물림).
3. 스킬 `orangpro` §0-A의 "최신 v1.5" 표기를 v2.2+v2.4로 갱신할지.
