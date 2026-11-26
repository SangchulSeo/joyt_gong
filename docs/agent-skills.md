# 조이티 공 에이전트 스킬

[Wikidocs 스킬 추천 목록](https://wikidocs.net/446636)의 57개 항목을 기준으로 관리합니다. 한 항목이 여러 스킬을 포함할 수 있습니다.

- Claude Code에서 저장소 루트를 열면 `.claude/skills/`의 프로젝트 스킬을 사용할 수 있습니다. 예: `/humanizer`.
- Codex에서는 `.agents/skills/`의 저장소 내부 링크를 사용합니다. 예: `$humanizer`. 체크아웃 시 심볼릭 링크가 실제 링크로 유지되어야 합니다.
- 스킬 파일은 Git에 포함됩니다. 별도 다운로드는 필요 없습니다. 외부 앱 로그인, MCP 연결, CLI, 원본 플러그인 훅은 쓰려는 기능별로 구성합니다.
- 세부 스킬 이름, 원본 커밋, 중복 또는 제외 항목과 이유는 [agent-skills.json](agent-skills.json)에서 확인합니다. 복사한 스킬의 라이선스는 [skill-licenses](skill-licenses/)와 원본 스킬 폴더에 있습니다.
- 원본 확인 대기 항목은 Wikidocs 개별 설치 안내에서 설치 대상을 먼저 확인해야 합니다.

- SkillSpector 실행 도구는 Python 3.13과 uv가 있는 환경에서 `./setup-skill-tools.sh`로 현재 프로젝트의 `.local/`에 설치합니다. 설치 후 `.local/skill-bin/skillspector`를 실행합니다.

| 번호 | 목록 항목 | 상태 | 원본 | 비고 |
| --- | --- | --- | --- | --- |
| 01-02 | [pm-skills](https://wikidocs.net/431817) | 등록 72개 | [phuryn/pm-skills](https://github.com/phuryn/pm-skills/tree/9af7bfd0bc47fdad43c2eaa7a43cd13918e7aaef) |  |
| 01-03 | [distilly](https://wikidocs.net/431818) | 등록 1개 | [titanwings/distilly](https://github.com/titanwings/distilly/tree/0afc45c29c360ba7bc8260f1bb0bf34e9155f4fa) |  |
| 01-04 | [wondelai/skills](https://wikidocs.net/431819) | 등록 66개 | [wondelai/skills](https://github.com/wondelai/skills/tree/c37678106e63ef1c5472d848fb3d8b8c5b33fafe) |  |
| 01-05 | [yc-office-hours](https://wikidocs.net/431922) | 원본 확인 대기 | — | 검색에서 동명 저장소를 찾았지만 문서 원본과 라이선스를 확인하지 못했습니다. |
| 01-06 | [research](https://wikidocs.net/431923) | 원본 확인 대기 | — | 개별 설치 문서를 열 수 없어 원본과 배포 조건을 확인하지 못했습니다. |
| 01-07 | [flow-map](https://wikidocs.net/431924) | 원본 확인 대기 | — | 개별 설치 문서를 열 수 없어 원본과 배포 조건을 확인하지 못했습니다. |
| 01-08 | [meeting-agenda](https://wikidocs.net/431925) | 원본 확인 대기 | — | 개별 설치 문서를 열 수 없어 원본과 배포 조건을 확인하지 못했습니다. |
| 02-01 | [marketingskills](https://wikidocs.net/431821) | 등록 52개 | [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills/tree/8fd2fcade2fd6629026e9dfe6d133b55b36968b9) | 1개 중복 또는 구성 확인 항목은 상세 목록에 기록했습니다. |
| 02-02 | [humanizer](https://wikidocs.net/431822) | 등록 1개 | [blader/humanizer](https://github.com/blader/humanizer/tree/a32f24407364c74c812b43c15926d638bee1e072) |  |
| 02-03 | [claude-ads](https://wikidocs.net/431823) | 등록 33개 | [AgriciDaniel/claude-ads](https://github.com/AgriciDaniel/claude-ads/tree/fc3908e786c318776df89a3a098333da377364be) | 스킬 파일을 등록했습니다. 플러그인 명령, 광고 계정 및 일부 분석 도구는 별도 연결이 필요합니다. |
| 02-04 | [blog-post](https://wikidocs.net/431824) | 원본 확인 대기 | — | 개별 설치 문서를 열 수 없어 원본과 배포 조건을 확인하지 못했습니다. |
| 02-05 | [blog-topic-judge](https://wikidocs.net/431926) | 원본 확인 대기 | — | 개별 설치 문서를 열 수 없어 원본과 배포 조건을 확인하지 못했습니다. |
| 02-06 | [technical-writer](https://wikidocs.net/431927) | 원본 확인 대기 | — | 개별 설치 문서를 열 수 없어 원본과 배포 조건을 확인하지 못했습니다. |
| 02-07 | [korean-writing-style](https://wikidocs.net/431928) | 등록 1개 | [seungjoonH/korean-writing-style](https://github.com/seungjoonH/korean-writing-style/tree/e62dbe81061f06729488eae8bc6a6abcdde7e503) |  |
| 02-08 | [card-news](https://wikidocs.net/431929) | 원본 확인 대기 | — | 개별 설치 문서를 열 수 없어 원본과 배포 조건을 확인하지 못했습니다. |
| 02-09 | [brunch-apply](https://wikidocs.net/435007) | 원본 확인 대기 | — | 개별 설치 문서를 열 수 없어 원본과 배포 조건을 확인하지 못했습니다. |
| 03-01 | [last30days-skill](https://wikidocs.net/431826) | 등록 1개 | [mvanhorn/last30days-skill](https://github.com/mvanhorn/last30days-skill/tree/ed7ec6752b766ea3eb62239b374900764e9b5453) | 연구 엔진에는 Python 3.12 이상과 해당 데이터 소스 설정이 필요할 수 있습니다. |
| 03-02 | [nature-skills](https://wikidocs.net/431827) | 등록 24개 | [Yuan1z0825/nature-skills](https://github.com/Yuan1z0825/nature-skills/tree/96a89bc7ef78e3bece9a50bb9ad08ddea4dc0e1e) | 논문 작성 스킬과 도형 스킬을 등록했습니다. 외부 논문 그림 샘플은 원본 링크에서 확인합니다. |
| 03-03 | [notebooklm-py](https://wikidocs.net/431828) | 등록 1개 | [teng-lin/notebooklm-py](https://github.com/teng-lin/notebooklm-py/tree/77d6ab4187cd7bd6d9af80ef6d74d524f77e7b68) | 별도 notebooklm-py CLI와 Google 로그인이 필요합니다. |
| 03-04 | [insane-search](https://wikidocs.net/431930) | 별도 구성 필요 | [fivetaku/insane-search](https://github.com/fivetaku/insane-search/tree/8d04ddace174b9008aea0c0f1b968b159f220fa4) | 원본 플러그인과 브라우저·검색 연결이 필요합니다. 자동 업데이트와 계정 작업을 활성화하지 않았습니다. |
| 03-05 | [apps-script-collector](https://wikidocs.net/431931) | 원본 확인 대기 | — | 개별 설치 문서를 열 수 없어 원본과 배포 조건을 확인하지 못했습니다. |
| 04-02 | [archify](https://wikidocs.net/431831) | 원본 확인 대기 | — | 개별 설치 문서를 열 수 없어 원본과 배포 조건을 확인하지 못했습니다. |
| 04-03 | [diagram-design](https://wikidocs.net/431832) | 원본 확인 대기 | — | 개별 설치 문서를 열 수 없어 원본과 배포 조건을 확인하지 못했습니다. |
| 04-04 | [huashu-design](https://wikidocs.net/431833) | 등록 1개 | [alchaincyf/huashu-design](https://github.com/alchaincyf/huashu-design/tree/59065698ad63f87ea1532c126c87f488d4f93fd6) | 스킬과 렌더링 자료를 등록했습니다. 별도 라이선스의 외부 스티커는 포함하지 않았습니다. |
| 04-05 | [architecture-drawio-diagram](https://wikidocs.net/431932) | 원본 확인 대기 | — | 개별 설치 문서를 열 수 없어 원본과 배포 조건을 확인하지 못했습니다. |
| 04-06 | [lecture-slide-make](https://wikidocs.net/431933) | 원본 확인 대기 | — | 개별 설치 문서를 열 수 없어 원본과 배포 조건을 확인하지 못했습니다. |
| 04-07 | [lecture-slides](https://wikidocs.net/431934) | 원본 확인 대기 | — | 개별 설치 문서를 열 수 없어 원본과 배포 조건을 확인하지 못했습니다. |
| 04-08 | [notebooklm-slides](https://wikidocs.net/431935) | 원본 확인 대기 | — | 개별 설치 문서를 열 수 없어 원본과 배포 조건을 확인하지 못했습니다. |
| 05-01 | [superpowers](https://wikidocs.net/431835) | 등록 15개 | [obra/superpowers](https://github.com/obra/superpowers/tree/22f0b463e7a5e579904dd6211a520321035526f7) | 스킬 문서를 등록했습니다. 원본 플러그인의 시작 훅과 에이전트 구성은 별개입니다. |
| 05-02 | [agent-skills](https://wikidocs.net/431836) | 등록 25개 | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/e997ac5b9a74eab332d5e9793bb38a38c8cfdd74) | 프로젝트 스킬을 등록했습니다. 플러그인 훅과 MCP 설정은 별개입니다. 1개 중복 또는 구성 확인 항목은 상세 목록에 기록했습니다. |
| 05-03 | [n8n-skills](https://wikidocs.net/431945) | 등록 15개 | [czlonkowski/n8n-skills](https://github.com/czlonkowski/n8n-skills/tree/ecdeca6f760b56bb1b11c0a7c961f11b69cb87d5) | 워크플로 실행에는 n8n 인스턴스와 기능별 연결이 필요합니다. |
| 05-04 | [n8n-route](https://wikidocs.net/431946) | 원본 확인 대기 | — | 개별 설치 문서를 열 수 없어 원본과 배포 조건을 확인하지 못했습니다. |
| 05-05 | [n8n-workflow-builder](https://wikidocs.net/431947) | 원본 확인 대기 | — | 개별 설치 문서를 열 수 없어 원본과 배포 조건을 확인하지 못했습니다. |
| 05-06 | [n8n-debugger](https://wikidocs.net/431948) | 원본 확인 대기 | — | 개별 설치 문서를 열 수 없어 원본과 배포 조건을 확인하지 못했습니다. |
| 05-07 | [rea](https://wikidocs.net/452096) | 원본 확인 대기 | — | 개별 설치 문서를 열 수 없어 원본과 배포 조건을 확인하지 못했습니다. |
| 06-01 | [obsidian-skills](https://wikidocs.net/431840) | 등록 7개 | [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills/tree/79e85b73ef041fdfb6437ab3824e2fe29eda9244) | CLI 연동 스킬에는 해당 Obsidian 도구가 필요합니다. |
| 06-02 | [gmail-search](https://wikidocs.net/431939) | 원본 확인 대기 | — | 개별 설치 문서를 열 수 없어 원본과 배포 조건을 확인하지 못했습니다. |
| 06-03 | [email-draft](https://wikidocs.net/431940) | 원본 확인 대기 | — | 개별 설치 문서를 열 수 없어 원본과 배포 조건을 확인하지 못했습니다. |
| 06-04 | [add-launchd-job](https://wikidocs.net/431941) | 원본 확인 대기 | — | 개별 설치 문서를 열 수 없어 원본과 배포 조건을 확인하지 못했습니다. |
| 06-05 | [new-project](https://wikidocs.net/431942) | 원본 확인 대기 | — | 개별 설치 문서를 열 수 없어 원본과 배포 조건을 확인하지 못했습니다. |
| 06-06 | [markdown-to-pdf](https://wikidocs.net/431943) | 원본 확인 대기 | — | 개별 설치 문서를 열 수 없어 원본과 배포 조건을 확인하지 못했습니다. |
| 06-07 | [aside-browser](https://wikidocs.net/431944) | 원본 확인 대기 | — | 개별 설치 문서를 열 수 없어 원본과 배포 조건을 확인하지 못했습니다. |
| 07-01 | [i-have-adhd](https://wikidocs.net/431837) | 원본 확인 대기 | — | 개별 설치 문서를 열 수 없어 원본과 배포 조건을 확인하지 못했습니다. |
| 07-02 | [grilling](https://wikidocs.net/431938) | 원본 확인 대기 | — | 관련 저장소의 스킬 이름이 바뀌어 문서의 원본 항목을 확정하지 못했습니다. |
| 07-03 | [plan](https://wikidocs.net/431936) | 원본 확인 대기 | — | 개별 설치 문서를 열 수 없어 원본과 배포 조건을 확인하지 못했습니다. |
| 07-04 | [planning-with-files](https://wikidocs.net/431841) | 등록 1개 | [OthmanAdi/planning-with-files](https://github.com/OthmanAdi/planning-with-files/tree/189fd09fecb246a4064f2cd0635153b5297f5369) | 프로젝트에서 수동으로 실행하는 형태입니다. 원본 자동 훅은 활성화하지 않았습니다. |
| 07-05 | [session-wrap](https://wikidocs.net/431838) | 원본 확인 대기 | — | 개별 설치 문서를 열 수 없어 원본과 배포 조건을 확인하지 못했습니다. |
| 07-06 | [skill-creator](https://wikidocs.net/431937) | 등록 1개 | [anthropics/skills](https://github.com/anthropics/skills/tree/e4bb5d960d87126ff3b3a8af1a104b7db67560ba) | 스킬 작성 문서를 등록했습니다. 평가 기능은 Claude CLI와 별도 라이브러리가 필요할 수 있습니다. |
| 07-07 | [skill-recorder](https://wikidocs.net/431843) | 원본 확인 대기 | — | 개별 설치 문서를 열 수 없어 원본과 배포 조건을 확인하지 못했습니다. |
| 07-08 | [SkillSpector](https://wikidocs.net/431842) | 등록 1개 | [NVIDIA/SkillSpector](https://github.com/NVIDIA/SkillSpector/tree/02894ec5b8a0a70637df5a6b45763de92940cedd) | 스킬과 설치 절차를 등록했습니다. CLI는 setup-skill-tools.sh로 프로젝트에 설치합니다. |
| 08-01 | [gstack](https://wikidocs.net/431816) | 별도 구성 필요 | [garrytan/gstack](https://github.com/garrytan/gstack/tree/89825888c57ec5ed472f8fea4a715882b401a9e5) | 브라우저 실행 파일 빌드는 성공했습니다. 원본 설치기는 읽기 전용 전역 홈의 .gstack 디렉터리 생성에서 중단되어 프로젝트 스킬 등록까지 완료되지 않았습니다. |
| 08-02 | [taste-skill](https://wikidocs.net/431830) | 등록 1개 | [leonxlnx/taste-skill](https://github.com/leonxlnx/taste-skill/tree/d1a2bb41d927083ac7118f60cfc9cdf711810ea0) | 프로젝트 스킬을 등록했습니다. 원본 자동 훅은 활성화하지 않았습니다. |
| 08-03 | [korean-privacy-terms](https://wikidocs.net/435361) | 원본 확인 대기 | — | 개별 설치 문서를 열 수 없어 원본과 배포 조건을 확인하지 못했습니다. |
| 08-04 | [ponytail](https://wikidocs.net/435504) | 원본 확인 대기 | — | 개별 설치 문서를 열 수 없어 원본과 배포 조건을 확인하지 못했습니다. |
| 08-05 | [ui-ux-pro-max](https://wikidocs.net/435505) | 등록 1개 | [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/tree/01706130e32f2af1d12923cce8d64a85fd76a3cd) |  |
| 08-06 | [Understand-Anything](https://wikidocs.net/435506) | 등록 9개 | [Egonex-AI/Understand-Anything](https://github.com/Egonex-AI/Understand-Anything/tree/b232f356446295e4eaa05b9b285e08ce5cd5e8a0) | 스킬을 등록했습니다. 그래프 생성에는 원본 플러그인과 Node 런타임 빌드가 별도로 필요합니다. |
| 08-07 | [open-code-review](https://wikidocs.net/435507) | 원본 확인 대기 | — | 개별 설치 문서를 열 수 없어 원본과 배포 조건을 확인하지 못했습니다. |
