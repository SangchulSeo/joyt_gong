---
name: google-sheets
description: 연결된 Google 스프레드시트를 정확한 범위 기준으로 분석하고 편집합니다. 구글 시트 생성, Drive에서 시트 찾기, 탭·범위 확인, 행 검색, 수식 작성·수정, 차트 생성·복구, 표 정리·재구성, 요약 또는 지정 셀 범위 업데이트에 사용합니다. Use for native Google Sheets creation, search, analysis, charts, formulas, and precise range edits.
---

# Google Sheets

대상 스프레드시트, 탭, 셀 범위, 헤더와 수식을 확인한 뒤 작업한다. 이 문서는 작업 경로 선택, 참고 문서 읽기 순서, 연결 도구를 통한 실시간 조회·검색, 결과 검증과 전달을 다룬다.

## 기본 경로

1. **기존 Google Sheets를 참고해 새 파일을 만드는 경우:** Drive의 파일 복사 도구로 원본 통합 문서 전체를 복사하고 필요한 내용을 정리한다. URL의 `gid`는 최초로 열 탭을 가리킨다. 사용자가 특정 탭만 가져오라고 한 경우에만 탭을 개별 복제한다. 칩, 유효성 검사, 수식, 리치 링크, 서식을 유지해야 하는 파일은 Excel로 다시 만들지 않는다.
2. **그 밖의 새 Google Sheets 생성:** 현재 사용할 수 있는 스킬과 플러그인에서 `$Spreadsheets`, `@Spreadsheets`, `plugin://spreadsheets@openai-primary-runtime` 등의 등록된 Spreadsheets 기능을 확인한다. 시스템 스프레드시트 기능을 사용할 수 있다면 해당 지침대로 로컬 `.xlsx`를 만든 뒤 Drive에서 Google Sheets 형식으로 가져온다. 기존에 준비된 Excel을 사용자가 가져오라고 했다면 해당 파일을 사용한다. 표의 선택형 열은 유효한 예제 값을 한 행에 넣고 가져온 뒤 필요하면 기본 표의 `DROPDOWN` 열로 설정한다.
3. **Spreadsheets 기능이 없는 새 파일 생성:** Google Sheets MCP가 제공하는 생성 도구를 사용한다. 기존 Google Sheets를 읽거나 편집할 때도 Google Sheets MCP를 사용한다. Drive 도구만 제공되면 해당 도구가 Sheets 형식 생성·변환을 지원하는지 확인한다.
4. **필요한 도구가 없는 경우:** 어떤 생성·편집 기능을 호출할 수 없었는지 밝힌다. 이미 사용자가 준비한 로컬 파일이 있으면 재사용한다. 사용자가 Google Sheets를 요구한 경우 로컬 파일만으로 완료 처리하지 않는다.

사용자가 편집을 요청한 기존 파일은 제자리에서 편집한다. 참고로 제공한 시트는 읽기 전용으로 취급한다. 같은 원본을 바탕으로 새 파일을 만들 때는 쓰기 전에 결과의 스프레드시트 ID가 원본과 다른지 확인한다. 사용자가 폴더를 정했다면 그 위치를 따르고, 지정이 없으면 내 드라이브 루트의 `ChatGPT` 폴더를 찾거나 만든다.

## 작업 순서와 조회 범위

1. 자료를 모으고 기본 경로를 고른다. 검증된 경로가 있다면 그대로 사용하고 불필요한 우회 절차를 추가하지 않는다.
2. 정확한 Sheets URL이나 ID를 확인한다. 제목만 주어졌다면 URL을 묻기 전에 연결된 검색 도구로 후보를 찾는다.
3. 범위를 자세히 읽거나 쓰기 전에 메타데이터에서 스프레드시트 ID, 실제 탭 이름, 각 `sheetId`를 확인한다.
4. 좌표 없는 전체 그리드 조회나 큰 범위의 반복 검색을 피한다. 메타데이터에 나온 정확한 탭 이름과 한정된 범위에서 헤더와 값을 확인한다.
5. 편집할 때마다 대상 탭·범위·헤더·수식·유효성 검사 조건을 확인한다. 현재 값, 수식, 서식 또는 검증 규칙이 편집에 영향을 주는 경우 쓰기 직전에 대상 셀을 다시 읽는다.
6. 필요한 범위만 쓰고, 결과의 탭·범위와 Google Sheets 원본 형식을 확인한다. 검증된 작업이 완료되면 종료한다.

## 필수 참고 문서 읽기 순서

세부 작업 전에 해당 참고 문서를 읽는다. 사용자가 스타일을 제시하지 않았다면 서식 작성 전에 [스타일 기준](references/style-profiles.md)을 읽는다. 새 파일 생성·가져오기·편집은 모두 최종 검증 전에 [시각 품질 기준](references/reference-visual-quality.md)을 읽는다.

- **Google Sheets 원본 복사:** 편집 흐름 → 실시간 조회·검색 → 기본 셀 구조 → 일괄 업데이트 예시 순으로 읽는다.
- **Spreadsheets 기능으로 작성해 가져오기:** 활성 스킬·플러그인의 지침 → Sheets로 가져오기 순으로 읽는다. 선택형 열을 가져온 뒤 변경할 때는 일괄 업데이트 예시도 읽는다.
- **연결 도구로 기존 파일 편집:** 편집 흐름을 먼저 읽는다. 직접 범위·셀 조회 또는 `search_spreadsheet_rows` 호출 전에는 실시간 조회·검색 지침을 읽는다.
- 여러 작업이 섞여 있으면 관련 파일을 모두 읽는다. 경로가 확실하지 않으면 참고 문서 전체를 확인한다.

| 작업 | 읽을 문서 |
| --- | --- |
| 기존 문서 편집, 검증 목록이 있는 셀, 쓰기 계획 | [편집 흐름](references/reference-edit-workflow.md) |
| 실시간 범위·셀 조회, 행 검색, 범위 오류 복구 | [실시간 조회·검색](references/reference-live-read-search-safety.md) |
| 값이 있는 곳 옆에 행·열 추가, 수식·칩·서식 유지, 원본 템플릿 참고 | [기본 셀 구조](references/reference-native-cell-structure.md) |
| Sheets 쓰기 요청과 일괄 업데이트 | [일괄 업데이트 예시](references/reference-batch-update-recipes.md) |
| Excel을 Google Sheets로 가져오기, 기본 표 변환 | [Sheets로 가져오기](references/reference-import-spreadsheet-to-native-sheets.md) |
| 수식 설계·수리·적용 | [수식 패턴](references/reference-formula-patterns.md) |
| 차트 만들기·수리·이동 | [차트 작업](references/reference-chart-recipes.md) |
| 서식 기본값 | [스타일 기준](references/style-profiles.md) |
| 최종 품질 확인 | [시각 품질 기준](references/reference-visual-quality.md) |

## 결과 전달

- 생성하거나 수정한 파일마다 연결 도구에서 확인한 Google Sheets URL을 결과로 한 번 인용한다. 앱이 파일 인용 지시자를 지원하면 출력마다 독립 문단에 `:codex-file-citation{path="확인된 실제 URL" purpose="output"}` 형식을 사용한다. 지원하지 않으면 확인한 실제 URL을 링크한다.
- 질문 답변이나 요약에 근거가 된 파일은 지원되는 경우 `purpose="source"`로 인용하고, 그 인용을 파일명 대신 쓴다. 단순 검사하거나 변경하지 않은 파일에 출력 인용을 붙이지 않는다.
- 사용자 요청으로 원본 형식을 유지하는 경우를 제외하면 Google Sheets 원본 URL을 전달한다. 임시 Excel 파일은 사용자가 요청한 경우에만 별도로 전달한다. 확인되지 않은 ID 또는 URL을 만들지 않는다.
