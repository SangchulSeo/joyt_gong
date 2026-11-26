# 조이티 채널 운영

Python 3.11 이상과 내장 SQLite로 실행합니다. 패키지 설치나 상시 서버가 필요 없습니다. 프로젝트 폴더에서 다음 명령을 실행합니다.

```sh
./setup.sh
```

이 명령은 DB를 초기화하고 오프라인 테스트를 실행합니다. Claude 인수인계는 [CLAUDE.md](CLAUDE.md), 프로젝트 스킬 설치 상태는 [에이전트 스킬 목록](docs/agent-skills.md)에 정리했습니다.

기본 DB는 `.local/joyti.sqlite3`에 저장됩니다. 별도 저장 위치는 `JOYTI_DB` 또는 명령 앞의 `--db 경로`로 지정합니다. 운영 DB는 지속 저장소에 두고 백업하세요. 토큰과 운영 데이터는 Git에 올리지 마세요.

## 게시 준비

1. 본문을 UTF-8 텍스트 파일로 작성합니다. `python3 joyti.py draft blog --title '제목' --body-file 본문.txt`로 등록합니다. 채널은 `blog`, `cafe`, `instagram` 중 하나입니다. 인스타그램에는 Meta에서 읽을 수 있는 공개 JPEG URL을 `--image-url`로 넘기고, 본문에는 캡션을 넣습니다. 인스타그램 제목은 내부 관리용입니다.
2. `python3 joyti.py list`로 번호를 확인하고 `python3 joyti.py show 1`로 초안을 검토합니다. `python3 joyti.py approve 1`로 승인합니다.
3. 블로그는 네이버 편집기에 제목과 본문을 붙여넣어 게시합니다. `python3 joyti.py record-published 1 게시물_URL`로 결과를 기록합니다.
4. 인스타그램과 카페는 `python3 joyti.py publish 1`로 발행 전 내용을 확인합니다. 실제 발행은 `python3 joyti.py publish 1 --send`를 실행한 경우에만 시도합니다. 카페는 멤버 공개 텍스트 글을 발행합니다.
5. 전송 후 결과가 불확실하면 상태가 `needs_review`로 남습니다. 프로세스가 중단되면 `sending`일 수 있습니다. 실행이 끝났는지 확인한 뒤 플랫폼에서 실제 게시 여부를 확인하세요. 게시가 확인되면 `record-published`로 URL을 기록합니다. 게시되지 않았음이 확인된 뒤에만 새 초안을 만들어 발행하세요.

| 채널 | 실행에 필요한 설정 |
| --- | --- |
| 인스타그램 | 조이티 프로페셔널 계정과 Instagram Login을 설정한 Meta 앱. `JOYTI_IG_USER_ID`, 앱이 지원하는 `JOYTI_IG_API_VERSION`(예: `v25.0`), `instagram_business_basic`과 `instagram_business_content_publish` 권한으로 발급된 `JOYTI_IG_ACCESS_TOKEN`. 네트워크 대상은 `graph.instagram.com`. |
| 네이버 카페 | 카페 글쓰기 권한을 가진 조이티 네이버 계정과 카페 API를 설정한 네이버 로그인 앱. `JOYTI_NAVER_CAFE_ID`, `JOYTI_NAVER_MENU_ID`, 해당 사용자에게 발급된 `JOYTI_NAVER_ACCESS_TOKEN`. 네트워크 대상은 `openapi.naver.com`. |
| 네이버 블로그 | 조이티 블로그의 편집 권한. 도구는 초안, 승인과 게시 URL을 관리합니다. |

환경변수 이름은 [.env.example](.env.example)에 모아 두었습니다. Claude나 Codex에서는 환경 설정에 값을 넣고, 토큰은 시크릿으로 등록하세요. 로컬 셸을 사용한다면 템플릿을 `.env`로 복사하고 필요한 항목의 주석을 풀어 입력한 뒤 `. ./.env`로 불러옵니다. 토큰 발급·갱신, 이미지 호스팅, 예약 실행은 별도로 운영해야 합니다. 연결 후에는 발행할 채널과 게시판을 확인하고 검수한 글 한 건으로 처음부터 끝까지 점검하세요.

[Meta 인스타그램 게시 문서](https://developers.facebook.com/docs/instagram-platform/instagram-api-with-instagram-login/content-publishing/) · [네이버 카페 API 문서](https://github.com/naver/naver-openapi-guide/blob/master/ko/login/cafe-api/cafe-api.md)

## 지식iN 자료 적재

권한이 있는 기존 자료를 UTF-8 JSONL 파일로 준비합니다. 줄마다 원본 URL, 질문, 답변을 넣습니다. 다음 값은 형식 설명용입니다.

```json
{"url":"https://kin.naver.com/qna/detail.naver?docId=123456","question":"질문 내용","answer":"답변 내용"}
```

```sh
python3 joyti.py kin-import 자료.jsonl
python3 joyti.py kin-search '검색어'
```

적재 전에 보관할 자료의 개인정보를 검토하세요. 같은 `docId`를 다시 적재하면 기존 항목을 갱신합니다. 검색은 질문과 답변의 문자열을 기준으로 최대 100건을 반환합니다.
