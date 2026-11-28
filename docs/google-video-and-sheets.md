# 조이티 Gemini·Veo 및 Google Sheets 연결

## 영상 제작

조이티 환경 시크릿 `JOYTI_GEMINI_API_KEY`를 `generativelanguage.googleapis.com`에 연결합니다. Gemini 텍스트 모델의 기본값은 `gemini-flash-latest`입니다. Veo 모델은 계정에 사용 권한이 있는 모델 ID를 `JOYTI_VEO_MODEL` 또는 `--model`로 지정합니다. Veo 사용 권한과 요금은 프로젝트에 적용된 설정을 따릅니다.

```sh
python3 gemini_video.py storyboard 영상기획.txt
python3 gemini_video.py veo-start 장면프롬프트.txt --generate
python3 gemini_video.py veo-status '반환된_작업_ID'
python3 gemini_video.py veo-download '반환된_작업_ID' .local/joyti-clip.mp4
```

영상 기획에는 첫 3초의 도입 문구와 촬영 컷을 포함합니다. 생성 명령은 기본 9:16 영상 한 건을 요청합니다. 생성 요청은 과금될 수 있습니다. 결과가 불확실하면 제공자에서 기존 작업을 확인한 뒤 다시 요청하세요. 내려받은 MP4는 검토 후 사용할 편집 소스입니다.

[Gemini 동영상 생성 API](https://ai.google.dev/gemini-api/docs/video)

## Google 관리시트

Google Cloud 프로젝트에서 Sheets API를 활성화합니다. 조이티 Google 계정으로 `https://www.googleapis.com/auth/drive.file` 또는 `https://www.googleapis.com/auth/spreadsheets` 범위의 OAuth 액세스 토큰을 발급받아 환경 시크릿 `JOYTI_SHEETS_ACCESS_TOKEN`으로 등록합니다. 네트워크 대상은 `sheets.googleapis.com`입니다. 만료된 액세스 토큰은 갱신해 교체합니다. Gemini 키와 Sheets OAuth 토큰은 각각 해당 API에 사용합니다.

```sh
python3 google_sheets.py preview
python3 google_sheets.py create
```

`preview`는 로컬에서 탭과 키워드 수를 확인합니다. `create`는 인증된 계정의 내 드라이브 루트에 새 Google 스프레드시트를 만들고, 질문·답변 관리 탭의 헤더와 검색 키워드 29개를 다시 읽은 뒤 URL을 출력합니다. 새 문서에는 상태 드롭다운, 필터, 고정 헤더가 포함됩니다. 실행마다 새 문서가 만들어집니다. 생성 응답이나 읽기 검증에 문제가 생기면 다시 실행하기 전에 Drive의 최근 파일을 확인하세요.

[Sheets 생성 및 OAuth 범위](https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/create?hl=ko) · [Sheets 범위 일괄 조회](https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets.values/batchGet?hl=ko)
