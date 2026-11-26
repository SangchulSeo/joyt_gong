---
name: joyti-four-channel
description: Turn a Joyti note, approved source, or brief into Instagram, Naver Blog, Knowledge iN, and YouTube drafts. Use for four-channel content planning, repurposing, review, and publication handoff.
---

# 조이티 네 채널 운영

1. 서비스 사실, 톤, 사용 가능한 영상·이미지와 지식iN 원본 질문을 확인한다. 필요하면 `python3 joyti.py kin-search '키워드'`로 승인된 자료를 찾아 보고, 사용자 자료로 확인되지 않은 가격·일정·스펙을 채우지 않는다.
2. 같은 주제로 Instagram 캡션, 블로그 본문, 지식iN 질문에 맞는 답변, 유튜브 제목·설명을 각각 만든다. 모델 키가 있는 별도 서비스를 가정하지 않는다. 채널별 원고와 출처를 작성하고 필요한 공개 미디어 URL은 실제 사용 권한이 있는 파일로 지정한다.
3. `workflows/example-drafts.json` 형식으로 준비하고 `python3 channel_workflow.py draft <file>`로 큐에 넣거나 설정된 n8n 웹훅을 이용한다. 예시 URL을 운영 요청에 복사하지 않는다.
4. 사용자에게 원고, 해당 계정, 미디어, 공개 범위를 보여 준다. 사용자의 게시 승인을 확인한 뒤 `python3 joyti.py approve ID`로 기록한다. 실제 발행은 승인된 건만 실행하고 [4채널 운영 안내](../../../docs/four-channel-workflow.md)의 채널별 절차를 따른다.
5. 외부에서 발행했다면 실제 게시 결과를 확인한 후 `python3 joyti.py record-published ID URL`로 기록한다. 예약 접수나 임시 저장은 게시 완료로 기록하지 않는다.
