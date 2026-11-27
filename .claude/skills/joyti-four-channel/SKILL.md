---
name: joyti-four-channel
description: Turn a Joyti note, approved source, or brief into Instagram, Naver Blog, Knowledge iN, and YouTube drafts. Use for four-channel content planning, repurposing, review, and publication handoff.
---

# 조이티 네 채널 운영

1. 서비스 사실, 톤, 사용 가능한 영상·이미지와 지식iN 원본 질문을 확인한다. 네이버 검색 MCP가 연결돼 있으면 `search_kin` 또는 `search_blog`로 후보를 찾고 원문을 확인한다. 승인된 자료는 `python3 joyti.py kin-search '키워드'`로 찾는다. 검색 결과의 요약을 확인된 답변으로 저장하지 않으며, 확인되지 않은 가격·일정·스펙을 채우지 않는다.
2. 같은 주제로 Instagram 캡션, 블로그 본문, 지식iN 질문에 맞는 답변, 유튜브 제목·설명을 각각 만든다. 모델 키가 있는 별도 서비스를 가정하지 않는다. 채널별 원고와 출처를 작성하고 필요한 공개 미디어 URL은 실제 사용 권한이 있는 파일로 지정한다.
3. `workflows/example-drafts.json` 형식으로 준비하고 `python3 channel_workflow.py draft <file>`로 큐에 넣거나 설정된 n8n 웹훅을 이용한다. 예시 URL을 운영 요청에 복사하지 않는다.
4. 사용자에게 원고, 해당 계정, 미디어, 공개 범위와 발행 시각을 보여 준다. 사용자의 게시 승인을 확인한 뒤 `python3 joyti.py approve ID`로 기록한다. 인스타그램·유튜브는 각 승인 건마다 직접 API 또는 Upload-Post·Taisly 중 하나의 경로를 선택한다. 네이버 블로그는 검수한 초안을 편집기에 저장하고, 지식iN은 원본 질문에 직접 답하는 초안을 준비한다. 실제 발행은 승인된 건만 실행한다. [연결 도구 안내](../../../docs/social-mcp-setup.md)
5. 외부에서 발행했다면 실제 게시 결과를 확인한 후 `python3 joyti.py record-published ID URL`로 기록한다. 예약 접수나 임시 저장은 게시 완료로 기록하지 않는다.
