# 조이티 4채널 작업 흐름

하나의 기획 자료에서 인스타그램, 네이버 블로그, 지식iN, 유튜브 초안을 만들고 기존 SQLite 큐에서 검토합니다. Codex나 Claude Code는 `joyti-four-channel` 스킬로 원본 자료를 확인하고 채널별 원고를 만듭니다. n8n 입력에는 작성된 원고가 들어갑니다. 웹훅 자체에는 모델 호출이나 발행 노드가 없습니다.

## 로컬 검증

저장소 루트에서 아래 명령을 실행합니다. 예시에는 테스트용 미디어와 질문 URL이 들어 있습니다.

```sh
./setup.sh
python3 channel_workflow.py --db .local/four-channel-demo.sqlite3 draft workflows/example-drafts.json
python3 channel_workflow.py --db .local/four-channel-demo.sqlite3 status sample-uniform-01
```

각 초안에는 고유 ID가 생깁니다. 같은 `request_id`로 같은 데이터를 다시 보내면 같은 ID를 받습니다. 내용이 바뀌었다면 새 요청 번호를 사용합니다. 운영 DB와 테스트 DB를 구분하고 `joyti.py --db 경로 show ID`로 초안을 검토하세요.

## n8n으로 실행

Node.js 24, npm, uv와 Python 3.13이 있는 환경에서 `./setup-channel-tools.sh`를 실행하면 n8n, n8n MCP, Taisly CLI, 네이버 블로그 MCP를 `.local/`에 설치합니다. 이 경로는 실행 환경마다 준비하며 Git에는 설정과 워크플로를 보관합니다.

두 터미널에서 아래 순서대로 서비스를 시작합니다. 새 운영용 백엔드 토큰을 환경 설정에 등록한 뒤 사용하세요. 검증은 같은 머신에서 n8n과 Python을 실행하는 구성입니다.

1. `JOYTI_WORKFLOW_TOKEN`이 설정된 첫 터미널에서 `python3 channel_workflow.py serve`를 실행합니다. 기본 주소는 `127.0.0.1:8765`입니다.
2. 두 번째 터미널에서 n8n 전용 상태 디렉터리를 지정하고 워크플로를 가져옵니다. 초기 설치 시 한 번만 가져오고 게시합니다. n8n에서 워크플로를 게시한다는 것은 **초안 수신 웹훅**을 활성화하는 것입니다.

```sh
export N8N_USER_FOLDER="$PWD/.local/joyti-n8n"
export N8N_LISTEN_ADDRESS=127.0.0.1 N8N_PORT=5687
export N8N_DIAGNOSTICS_ENABLED=false N8N_VERSION_NOTIFICATIONS_ENABLED=false N8N_TEMPLATES_ENABLED=false
mkdir -p "$N8N_USER_FOLDER"
.local/n8n-runtime/node_modules/.bin/n8n import:workflow --input=workflows/four-channel-drafts.json
.local/n8n-runtime/node_modules/.bin/n8n publish:workflow --id=joyti4ChannelDrafts
.local/n8n-runtime/node_modules/.bin/n8n start
```

3. n8n 시작이 끝나면 같은 머신의 `POST http://127.0.0.1:5687/webhook/joyti-four-channel-drafts`에 JSON과 `Authorization: Bearer <워크플로 토큰>`을 보냅니다. 응답은 신규 `201`, 중복 재전송 `200`, 내용이 달라진 동일 요청 `409`, 인증 실패 `401`입니다. 예시 요청을 HTTP로 확인할 때는 전용 테스트 DB 토큰과 워커를 사용합니다.

n8n MCP 문서·검증 모드는 `MCP_MODE=stdio LOG_LEVEL=error DISABLE_CONSOLE_OUTPUT=true`와 `.local/n8n-runtime/node_modules/.bin/n8n-mcp`로 실행합니다. 실행 중인 인스턴스를 MCP로 관리하려면 별도로 `N8N_API_URL`과 권한이 있는 `N8N_API_KEY`를 시크릿에 설정합니다.

## 검토와 발행

`python3 joyti.py show ID`로 본문과 미디어를 확인합니다. 사용자의 게시 승인을 받은 ID만 `python3 joyti.py approve ID`로 승인합니다. `python3 joyti.py publish ID`로 승인된 초안을 다시 볼 수 있습니다.

| 채널 | 승인 후 연결 방식 |
| --- | --- |
| 인스타그램 이미지 | 기존 Graph API 설정으로 `python3 joyti.py publish ID --send`를 사용합니다. |
| 인스타그램 릴스·유튜브 | Taisly의 계정 연결을 마친 뒤 대상 계정과 공개 범위를 확인합니다. `.local/taisly-runtime/node_modules/.bin/taisly help`에서 검증·발행·결과 확인 명령을 확인합니다. 예약 요청이 접수됐다는 응답은 발행 완료로 기록하지 않습니다. |
| 네이버 블로그 | `.local/skill-bin/naver-blog-mcp`에 `NAVER_BLOG_ID`와 사용자가 직접 로그인해 만든 `NAVER_STATE` 파일의 경로를 설정합니다. 초안 저장 도구로 에디터 결과를 확인하고 승인 범위에 따라 게시합니다. 세션 파일은 저장소 밖이나 무시되는 경로에 보관합니다. |
| 지식iN | 초안과 정확한 질문 URL을 큐에 보관합니다. 원본 질문과 답변을 검토한 후 사용자 세션의 편집기에서 게시합니다. 브라우저의 자동 로그인·답변 제출은 이 워크플로에 연결되지 않았습니다. |

외부 편집기·CLI로 게시한 건은 실제 URL을 확인한 뒤 `python3 joyti.py record-published ID URL`로 기록합니다. 스케줄러, 계정 권한, 쿠키와 원격 발행 결과는 별도 실계정 검증이 필요합니다.

[Codex용 소셜 MCP 연결 안내](social-mcp-setup.md) · [공식 n8n 스킬](https://github.com/n8n-io/skills/tree/626f50fdf2934116eea2c5469339e03d2d524e83) · [네이버 블로그 MCP 설치 안내](https://github.com/Johnhyeon/naver-blog-mcp) · [Taisly Agent](https://github.com/taisly/agent)
