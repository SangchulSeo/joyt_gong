# 조이티 Codex 소셜 MCP 연결

저장소 루트에서 `./setup-social-mcp.sh`를 실행합니다. Node.js, npm, uv와 Python 3.13이 필요합니다. 설치 스크립트가 `config/codex-social-mcp.example.toml`에 현재 저장소의 실행 경로를 넣어 `.local/codex-social-mcp.toml`을 생성합니다. 기존 설정 파일은 보존합니다. 네이버 블로그 실행 파일은 `./setup-channel-tools.sh`에서 설치합니다.

사용할 서버 블록을 Codex의 `config.toml`에 병합하고 해당 블록만 `enabled = true`로 바꿉니다. `env_vars`에 나온 이름으로 실행 환경 또는 시크릿 저장소에 값을 준비합니다. 파일 경로가 필요한 경우 보관 위치만 전달합니다. 실제 토큰과 로그인 세션 파일은 Git과 설정 예시에 넣지 않습니다.

| 설정 블록 | 기능 | 필요한 인증과 준비 |
| --- | --- | --- |
| `joyti_naver_search` | `search_kin`, `search_blog`, 데이터랩 | Naver API Hub의 `NCP_APIGW_API_KEY_ID` 및 `NCP_APIGW_API_KEY`, 또는 보유한 네이버 개발자센터 키 쌍. 현재 지원되는 발급·사용 기간은 [원본 안내](https://github.com/isnow890/naver-search-mcp)에서 확인합니다. |
| `joyti_naver_blog` | 네이버 블로그 초안 저장과 게시 | `NAVER_BLOG_ID`, 사용자가 직접 로그인해 만든 브라우저 상태 파일의 경로 `NAVER_STATE`. 먼저 초안 저장을 검증합니다. |
| `joyti_instagram` | Instagram Login을 통한 게시·댓글·인사이트 | 권한 범위가 맞는 `INSTAGRAM_ACCESS_TOKEN`. 쓰기 가능한 `INSTAGRAM_DATA_DIR`을 설정합니다. 원본은 FastMCP v1을 사용해 SDK를 `1.30.0`으로 고정했습니다. |
| `joyti_youtube` | 유튜브 데이터·분석과 업로드 | 공개 조회는 `YOUTUBE_API_KEY`, 계정 작업은 `YOUTUBE_MCP_CLIENT_SECRET`의 OAuth 클라이언트 파일과 채널 소유자의 동의. 쓰기 가능한 `YOUTUBE_MCP_CONFIG_DIR`을 설정합니다. |
| `joyti_upload_post` | Instagram·YouTube 등을 한 경로에서 예약·업로드 | `UPLOAD_POST_API_KEY`와 Upload-Post에서 연결한 대상 계정. 저장소 HEAD의 `0.28.1`은 npm에서 확인되지 않아 배포된 `0.28.0`으로 고정했습니다. |

직접 Instagram·YouTube MCP와 Upload-Post·Taisly는 대체 경로입니다. 같은 승인 ID를 둘 이상의 발행 도구에 보내지 마세요. 승인 전에는 검색·상태 확인·검증·초안만 실행합니다. 예약 접수와 실제 발행을 구분하고, 공개된 결과를 확인한 뒤 큐에 URL을 기록합니다. 지식iN 검색 MCP는 답변을 제출하지 않습니다.

제한 네트워크 환경에서는 선택한 커넥터의 목적지가 허용돼야 합니다. 확인한 대표 목적지는 Naver API Hub의 `naverapihub.apigw.ntruss.com` 또는 기존 `openapi.naver.com`, Instagram Login의 `graph.instagram.com`, YouTube의 Google API 및 OAuth 호스트, Upload-Post의 `api.upload-post.com`입니다. 이 설정 파일은 클라우드 네트워크 정책을 변경하지 않습니다.

## 원본과 대안

- [charlie947/social-media-skills](https://github.com/charlie947/social-media-skills/tree/10ca79c0ec0be0f7654d19cd4f0c86b6fa6ed23b) 17개 및 [naver-search-mcp](https://github.com/isnow890/naver-search-mcp/tree/f8dca091120810644e1d8f97043235d7b2324fc7)의 스킬 1개를 프로젝트에 등록했습니다.
- [mcpware/instagram-mcp](https://github.com/mcpware/instagram-mcp)는 확인한 저장소에서 Python 및 Facebook Graph 설정을 사용합니다. 조이티의 기본 Instagram Login 연결에는 [William-Gao/instagram-mcp](https://github.com/William-Gao/instagram-mcp)를 선택했습니다.
- [anwerj/youtube-uploader-mcp](https://github.com/anwerj/youtube-uploader-mcp)는 Go로 제공되는 업로드 중심 대안입니다. 기본 연결에는 공개 데이터 조회와 분석이 함께 있는 [pauling-ai/youtube-mcp-server](https://github.com/pauling-ai/youtube-mcp-server)를 선택했습니다.
- `neneungyul2/ne-naver-api-mcp`는 해당 GitHub 주소에서 공개 원본 커밋을 확인하지 못했습니다. 데이터랩 상대 지수는 월간 절대 검색량으로 기록하지 않습니다.
