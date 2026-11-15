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
debug/                     # 디버깅 기록 (XML 덤프 포함)
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
- git user: 조성현 / sunghyun1.cho@gmail.com (global 설정)
- GitHub Action이 manifest를 커밋하므로, 이후 push 전엔 `git pull --rebase` 먼저

## 현황 / TODO
- [x] 저장소 clone (2026-11-15)
- [x] index.html 뷰어, manifest 생성 스크립트, Action 워크플로 작성
- [ ] 최초 commit/push 및 GitHub Pages 활성화 확인 (Settings → Pages → Branch: `pages` / root)
- [ ] 첫 push 후 Action 권한 확인 (Settings → Actions → Workflow permissions: Read and write)
- [ ] `docs/stockmonitor/` 는 비어 있음(.gitkeep)
- [ ] 주제별 폴더 재편 여부 결정 (현재 서비스별: honeybot / stockmonitor / shared)
