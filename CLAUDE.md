# CLAUDE.md — Public 문서 저장소 작업 가이드

> 세션이 바뀌어도 이어서 작업할 수 있도록 현황을 기록한다. 작업 후 "현황/TODO"를 갱신할 것.

## 개요
- 저장소: https://github.com/ntames8/Public.git (Public, 기본 브랜치 **`pages`**)
- 로컬 경로: `D:/ai/my_git/semiconductor-monitor` (원격 저장소는 사용자가 생성 예정, 이름/공개 여부 미정)
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
