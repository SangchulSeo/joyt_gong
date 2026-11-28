"""Create and verify Joyti's Knowledge iN tracker as a native Google Sheet."""

import argparse
from contextlib import closing
import json
import os
from pathlib import Path
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, build_opener

from publishers import NoRedirect

API = "https://sheets.googleapis.com/v4/spreadsheets"
TEMPLATE = Path(__file__).with_name("workflows") / "kin-sheet-template.json"


class SheetsError(RuntimeError):
    pass


def call_api(path="", payload=None):
    token = os.getenv("JOYTI_SHEETS_ACCESS_TOKEN", "").strip()
    if not token or any(c.isspace() for c in token):
        raise ValueError("Sheets 쓰기 권한이 있는 Google OAuth 토큰을 JOYTI_SHEETS_ACCESS_TOKEN에 등록하세요.")
    headers = {"Authorization": f"Bearer {token}"}
    body = None
    if payload is not None:
        headers["Content-Type"] = "application/json"
        body = json.dumps(payload).encode()
    req = Request(API + path, data=body, headers=headers)
    try:
        with closing(build_opener(NoRedirect()).open(req, timeout=40)) as response:
            result = json.load(response)
    except HTTPError as exc:
        code = exc.code
        exc.close()
        raise SheetsError(f"Sheets API HTTP {code}. OAuth 범위, 토큰 만료, API 사용 설정과 접속 정책을 확인하세요.") from None
    except (URLError, TimeoutError, ValueError):
        raise SheetsError("Sheets API의 응답을 확인하지 못했습니다.") from None
    if not isinstance(result, dict):
        raise SheetsError("Sheets API 응답 형식을 확인할 수 없습니다.")
    return result


def sheet_template():
    return json.loads(TEMPLATE.read_text(encoding="utf-8"))


def sheet_payload(template):
    sheets = []
    green = {"red": 0.09, "green": 0.39, "blue": 0.29}
    white = {"red": 1, "green": 1, "blue": 1}
    widths = [[110, 110, 150, 290, 240, 280, 320, 130, 130, 100, 180],
              [110, 180, 170, 330, 130, 180]]
    for sheet_id, tab in enumerate(template):
        validators = {
            p["column"]: {
                "condition": {"type": "ONE_OF_LIST", "values": [
                    {"userEnteredValue": option} for option in p["choices"]
                ]},
                "strict": True, "showCustomUi": True,
            } for p in tab["options"]
        }
        data = []
        for row in range(tab["rows"]):
            raw = tab["values"][row] if row < len(tab["values"]) else []
            cells = []
            for col in range(tab["columns"]):
                cell = {}
                if col < len(raw) and raw[col] is not None:
                    cell["userEnteredValue"] = {"stringValue": raw[col]}
                if row == 3:
                    cell["userEnteredFormat"] = {
                        "backgroundColor": green,
                        "textFormat": {"bold": True, "foregroundColor": white},
                        "wrapStrategy": "WRAP",
                    }
                if row >= 4 and col in validators:
                    cell["dataValidation"] = validators[col]
                cells.append(cell)
            data.append({"values": cells})
        sheets.append({
            "properties": {"sheetId": sheet_id, "title": tab["name"], "gridProperties": {
                "rowCount": tab["rows"], "columnCount": tab["columns"],
                "frozenRowCount": 4,
            }},
            "merges": [{"sheetId": sheet_id, "startRowIndex": row, "endRowIndex": row + 1,
                        "startColumnIndex": 0, "endColumnIndex": tab["columns"]} for row in (0, 1)],
            "basicFilter": {"range": {"sheetId": sheet_id, "startRowIndex": 3,
                                      "endRowIndex": tab["rows"], "startColumnIndex": 0,
                                      "endColumnIndex": tab["columns"]}},
            "data": [{"rowData": data, "columnMetadata": [
                {"pixelSize": width} for width in widths[sheet_id]
            ]}],
        })
    return {"properties": {"title": "조이티 지식iN 관리시트", "locale": "ko_KR",
                           "timeZone": "Asia/Seoul"}, "sheets": sheets}


def create_kin_sheet():
    template = sheet_template()
    created = call_api(payload=sheet_payload(template))
    sheet_id = created.get("spreadsheetId", "")
    if not isinstance(sheet_id, str) or not re.fullmatch(r"[a-zA-Z0-9_-]+", sheet_id):
        raise SheetsError("생성 응답에서 문서 ID를 확인하지 못했습니다. 다시 만들기 전에 Drive를 확인하세요.")
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/edit"
    ranges = ["'질문·답변 관리'!A4:K4", "'검색 키워드'!A4:D33"]
    try:
        data = call_api(f"/{sheet_id}/values:batchGet?" + urlencode({"ranges": ranges}, doseq=True))
        a, b = data["valueRanges"]
        if a["values"] != [template[0]["values"][3]]:
            raise SheetsError("질문·답변 관리 탭의 헤더가 다릅니다.")
        expected = [row[:4] for row in template[1]["values"][3:]]
        if b["values"] != expected:
            raise SheetsError("검색 키워드 탭의 값이 다릅니다.")
    except (SheetsError, KeyError, TypeError, ValueError) as exc:
        raise SheetsError(f"문서는 생성됐지만 검증을 완료하지 못했습니다. 새로 만들기 전에 {url} 확인: {exc}") from None
    return {"spreadsheet_id": sheet_id, "url": url, "tabs": [tab["name"] for tab in template],
            "keywords": len(expected) - 1}


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("preview", "create"))
    args = cli.parse_args()
    try:
        if args.action == "preview":
            template = sheet_template()
            result = {"title": "조이티 지식iN 관리시트", "tabs": [t["name"] for t in template],
                      "keywords": len(template[1]["values"]) - 4}
        else:
            result = create_kin_sheet()
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except (SheetsError, OSError, ValueError) as exc:
        print(f"오류: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
