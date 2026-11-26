# 아이콘 캐시

다이어그램과 카드에 쓸 SVG 아이콘을 이 폴더에 캐싱해둔다. 두 종류를 구분해서 쓴다. `visual-design.md`의 "브랜드 로고는 그 브랜드 자체를 가리킬 때만" 원칙을 참고한다.

- **브랜드 로고** (`{name}.svg`): 특정 서비스를 확정해서 가리킬 때 쓴다
  - 출처: [Simple Icons](https://simpleicons.org) (CC0)
- **범용 아이콘** (`generic-{name}.svg`): 여러 업체 중 하나로 확정되지 않은 카테고리나 기능(이메일, SMS, 알림 등)을 가리킬 때 쓴다
  - 출처: [Heroicons](https://heroicons.com) solid 세트 (MIT)

각 파일은 `<path>`(브랜드 아이콘은 보통 1개, 범용 아이콘은 1-2개)로 된 단색 아이콘이며 `fill` 속성이 없거나 `currentColor`다. 삽입할 때 `fill="currentColor"`나 원하는 색을 직접 지정한다.

## 보유 아이콘

| 파일 | 용도 |
|---|---|
| `vercel.svg` | Vercel (브랜드) |
| `supabase.svg` | Supabase (브랜드) |
| `github.svg` | GitHub (브랜드) |
| `postgresql.svg` | PostgreSQL (브랜드) |
| `docker.svg` | Docker (브랜드) |
| `twilio.svg` | Twilio (브랜드) |
| `nextdotjs.svg` | Next.js (브랜드) |
| `resend.svg` | Resend (브랜드) |
| `generic-bell.svg` | 알림 (범용) |
| `generic-envelope.svg` | 이메일 (범용) |
| `generic-chat-bubble-left-right.svg` | 메시지, SMS (범용) |
| `generic-key.svg` | 인증, OAuth (범용) |
| `generic-server.svg` | 서버, 인프라 (범용) |
| `generic-shield-check.svg` | 보안, 규정 준수 (범용) |
| `generic-wrench-screwdriver.svg` | 설정, 기타 도구 (범용) |
| `generic-globe-alt.svg` | 도메인, 웹 주소 (범용) |
| `generic-cloud.svg` | 관리형 클라우드 서비스 (범용) |

## 새 아이콘이 필요할 때

1. **특정 브랜드**를 가리키는 경우: Simple Icons에 있는지 먼저 확인한다 (slug 이름은 보통 서비스명을 소문자로 붙인 형태이며, 숫자로 시작하면 `dotjs` 같은 접미사가 붙는 경우가 있다. 예: Next.js → `nextdotjs`). `https://cdn.jsdelivr.net/npm/simple-icons@latest/icons/{slug}.svg`에서 받는다.
2. **카테고리나 기능**을 가리키는 경우: Heroicons solid에서 받는다. `https://cdn.jsdelivr.net/npm/heroicons@2/24/solid/{slug}.svg`
3. 받은 파일은 이 폴더에 저장하고 위 표에 행을 추가한다. **파일에 실제로 들어있는 `<path>` 데이터를 그대로 쓴다. 기억으로 재구성하지 않는다.**
4. Simple Icons나 Heroicons 둘 다에 없는 경우(자체 개발 도구, 사내 서비스 등)는 추상 도형을 쓰되, `visual-design.md`의 원칙대로 다이어그램 전체에서 스타일을 통일한다.
