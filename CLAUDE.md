# CLAUDE.md — Public 문서 저장소 작업 가이드

> 세션이 바뀌어도 이어서 작업할 수 있도록 현황을 기록한다. 작업 후 "현황/TODO"를 갱신할 것.

## 개요
- 저장소: https://github.com/ntames8/Public.git (Public, 기본 브랜치 **`pages`**)
- 로컬 경로: `D:\ai\my_git\Public` (상위 `D:\ai\my_git` 는 git 저장소 아님)
- 목적: 주제별 `.md` / `.html` 문서를 모아 두고, 최상위 `index.html` 뷰어에서 폴더 트리로 탐색.
- 배포: GitHub Pages (`pages` 브랜치 루트). 예상 URL `https://ntames8.github.io/Public/` (Pages 설정 확인 필요)

## 구조
```
index.html                 # 뷰어 (좌측 접이식 트리 + 우측 본문). 수정 시 단일 파일 유지
manifest.json              # 자동 생성물. 직접 편집 금지
scripts/build_manifest.py  # 저장소를 스캔해 manifest.json 생성 (Python 표준 라이브러리만)
.github/workflows/manifest.yml  # push 시 manifest.json 자동 갱신/커밋
.nojekyll                  # Jekyll 처리 비활성화
docs/<서비스>/             # 문서 (honeybot, stockmonitor, shared …)
docs/hr/                   # 인사 관련 문서 (공개 자료 기반)
docs/news/semiconductor/dashboard.html  # AI·반도체 대시보드 '결과물만' 게시 (원본 프로젝트는 별도 저장소)
```

## 문서 추가 방법
1. 아무 하위 폴더에 `.md`/`.html`/`.txt`/`.xml` 등 추가 (폴더 구조 = 트리 구조)
2. `python scripts/build_manifest.py` 로 manifest 갱신 (원격에서는 push 시 GitHub Action이 자동 수행)
3. commit & push

- manifest 제외: `.`으로 시작하는 파일/폴더, `.github`, `scripts`, `node_modules`, `index.html`, `manifest.json`, `CLAUDE.md`, `.gitkeep`, 빈 폴더
- 확장자 허용 목록은 `scripts/build_manifest.py` 의 `VIEWABLE`
- 파일명 규칙(기존 관행): `YYYYMMDD_제목.md`

## 뷰어 동작
- `manifest.json` fetch → 트리 렌더. 선택 파일은 URL 해시(`#경로`)로 딥링크
- `.md`: marked(CDN, v12.0.2)로 렌더, 상대 이미지/링크 보정, 다른 md 링크는 뷰어 내부 이동
- `.html`/`.pdf`: iframe, 이미지: `<img>`, 그 외 텍스트: `<pre>`
- 사이드바: 접기(«/☰), 폭 드래그, 폴더 전체 접기/펼치기, 검색. 상태는 localStorage 저장
- 로컬 확인: `file://` 에선 fetch 불가 → `python -m http.server 8000` 후 http://localhost:8000

## 인증 (push 시)
- clone/pull 은 인증 불필요(Public). **push 는 GitHub 인증 필요**
- 이 PC: git 2.35.1, credential helper `manager-core`(Windows 자격 증명 관리자) — 첫 push 때 브라우저 로그인 창이 뜸
- 대안: PAT(Fine-grained, 해당 repo `Contents: Read and write`)를 비밀번호로 사용
- git user: global 설정 사용 (본문에 이메일/이름 등 개인정보를 적지 않는다)
- 토큰 권한: `.github/workflows/*` 를 push하려면 토큰에 Workflows(`workflow`) 권한 필요. 평소엔 꺼 둘 것
- 토큰은 `.env` 등 파일에 저장하지 않는다. Windows 자격 증명 관리자 사용, 기계(PC/Linux)마다 별도 토큰 또는 SSH 키
- Bash 도구에서 Windows 경로는 `D:/ai/my_git/Public` 처럼 슬래시 사용 (`\` 는 이스케이프됨)
- GitHub Action이 manifest를 커밋하므로, 이후 push 전엔 `git pull --rebase` 먼저

## 외부 프로젝트 결과물 게시 방식
- 코드·원자료가 큰 프로젝트는 **별도 저장소**에 두고, 이 저장소에는 결과 `.html` 만 복사해 올린다
- AI·반도체 모니터링: 로컬 `D:/ai/my_git/semiconductor-monitor` (원격 저장소는 사용자가 생성 예정, 이름/공개 여부 미정)
  - 갱신: 해당 프로젝트에서 `python -I -X utf8 src/update.py` → `dashboard/index.html` 생성 → 이 저장소 `docs/news/semiconductor/dashboard.html` 로 복사 → commit/push

## ⚠ Public 저장소 — 개인정보/비밀 금지 규칙
이 저장소는 **Public**이고 Pages로 전부 노출된다. push 한 내용은 git 이력에 남아 완전히 회수할 수 없다.
- **올리지 말 것**: 토큰·API 키·PIN·비밀번호(일부/앞부분 포함), chat_id·기기 ID, 가족/지인 이름·전화번호·이메일, 계좌·잔액·거래내역·가맹점, 앱 화면 덤프(XML/스크린샷/로그), 사내 비공개 자료
- 디버깅 기록·덤프·로그는 올리지 않는다 (`debug/` 폴더는 이력에서도 삭제됨). 필요하면 Private 저장소나 로컬에 둔다
- 식별자는 `**********` 로 마스킹해서 기술한다
- **commit 전 점검**: 새/수정 파일을 훑고, 아래로 의심 패턴 검색
  `grep -rnIE "[0-9]{8,10}:[A-Za-z0-9_-]{30,}|01[016789][-. ]?[0-9]{3,4}[-. ]?[0-9]{4}|[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}|ghp_|github_pat_" --exclude-dir=.git .`
- 문서가 공개 자료 기반인지 불명확하면 올리기 전에 사용자에게 확인한다
- 사고 이력: 2026-11-15 debug/·텔레그램 토큰 앞부분·chat_id·가족 연락처가 노출돼 `git filter-repo` + force push 로 이력 재작성함 (commit 해시 전부 변경, 다른 clone은 새로 받아야 함). 로컬 백업 `Public_backup` 은 개인정보 포함이므로 삭제 대상

## 현황 / TODO
- [x] 저장소 clone, index.html 뷰어 / manifest 스크립트 / Action 작성 및 push (2026-11-15)
- [x] `docs/hr/` 삼성전자 인사운영 분석 페이지 추가 (공개 문서)
- [x] 개인정보 정리 및 이력 재작성, force push
- [ ] GitHub 설정 확인: Pages(Branch `pages` / root), Actions Workflow permissions = Read and write
- [ ] 뷰어(https://ntames8.github.io/Public/) 동작 확인, Action `Update manifest` 성공 확인
- [x] semiconductor 프로젝트 분리: 별도 로컬 저장소 commit 완료, Public에는 dashboard.html 만 게시
- [ ] semiconductor-monitor 원격 저장소 생성 후 remote 연결·push (사용자 작업)
- [ ] `docs/stockmonitor/` 는 비어 있음(.gitkeep)
- [ ] 주제별 폴더 재편 여부 결정 (현재: docs/honeybot, docs/stockmonitor, docs/shared, docs/hr)
