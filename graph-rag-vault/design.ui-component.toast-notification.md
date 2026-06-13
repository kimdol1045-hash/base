---
id: "design.ui-component.toast-notification"
domain: "design"
type: "pattern"
bloom_level: "토스트 알림은 사용자 작업을 방해하지 않으면서 시스템 상태 변화를 전달하는 비차단형 UI 패턴이다. Android Material Design에서 Snackbar로 체계화했으며, 피드백-알림-확인의 3가지 용도로 사용된다."
tags: ["toast", "notification", "snackbar", "feedback"]
brain_region: "CORTEX"
token_estimate: 380
---

# design.ui-component.toast-notification

> 토스트 알림은 사용자 작업을 방해하지 않으면서 시스템 상태 변화를 전달하는 비차단형 UI 패턴이다. Android Material Design에서 Snackbar로 체계화했으며, 피드백-알림-확인의 3가지 용도로 사용된다.

# 토스트 알림 가이드

## 핵심 원칙
- 비차단형: 사용자 작업 흐름을 방해하지 않음
- 자동 사라짐: 3-5초 후 자동 닫힘
- 명확한 상태: 성공/에러/경고/정보 시각 구분
- 실행 취소(Undo) 옵션 제공 가능

## 유형별 가이드
| 유형 | 색상 | 아이콘 | 지속 시간 |
|------|------|--------|----------|
| 성공 | 초록 | 체크 | 3초 |
| 에러 | 빨강 | 엑스 | 수동 닫기 |
| 경고 | 노랑 | 느낌표 | 5초 |
| 정보 | 파랑 | i | 4초 |

## 위치 및 동작
- 위치: 화면 하단 중앙 또는 우상단
- 진입: 아래에서 슬라이드 업 (200-300ms)
- 퇴장: 페이드 아웃 또는 슬라이드 다운
- 중첩: 최대 3개까지 스택

## 접근성 요구사항
- role="alert" 또는 aria-live="polite" 속성
- 키보드로 닫기 가능 (Escape)
- 충분한 색상 대비 (4.5:1)
- 호버 시 자동 닫힘 일시 중지

## DO
- 삭제 작업에 "실행 취소" 옵션 포함
- 에러 토스트는 수동으로만 닫을 수 있게
- 간결한 메시지 (한 줄, 50자 이내)

## DON'T
- 중요한 에러를 토스트로만 알리지 않기
- 동시에 5개 이상 토스트 표시하지 않기
- 사용자 입력이 필요한 내용을 토스트에 넣지 않기
