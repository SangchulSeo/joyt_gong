"""Prepare a short-video storyboard and generate a draft clip with Gemini and Veo."""

import argparse
from contextlib import closing
import json
import os
from pathlib import Path
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, build_opener

from publishers import NoRedirect

HOST = "generativelanguage.googleapis.com"
API = f"https://{HOST}/v1beta"
VIDEO_LIMIT = 120 * 1024 * 1024
MODEL_ID = re.compile(r"[a-zA-Z0-9][a-zA-Z0-9._-]*")
OPERATION_ID = re.compile(r"(?:models/[a-zA-Z0-9._-]+/)?operations/[a-zA-Z0-9._-]+")
FILE_PATH = re.compile(r"/v1beta/files/[a-zA-Z0-9._-]+:download")


class GeminiError(RuntimeError):
    pass


def open_api(path, payload=None):
    key = os.getenv("JOYTI_GEMINI_API_KEY", "").strip()
    if not key or any(c.isspace() for c in key):
        raise ValueError("환경 설정에 JOYTI_GEMINI_API_KEY를 등록하세요.")
    data = json.dumps(payload).encode() if payload is not None else None
    headers = {"x-goog-api-key": key}
    if data is not None:
        headers["Content-Type"] = "application/json"
    request = Request(f"{API}/{path}", data=data, headers=headers)
    try:
        return build_opener(NoRedirect()).open(request, timeout=60)
    except HTTPError as exc:
        code = exc.code
        exc.close()
        raise GeminiError(f"Gemini API HTTP {code}. 키, 모델 접근 권한, 할당량과 접속 설정을 확인하세요.") from None
    except (URLError, TimeoutError):
        raise GeminiError("Gemini API에 접속하지 못했습니다. 접속 설정을 확인하세요.") from None


def api_json(path, payload=None):
    with closing(open_api(path, payload)) as response:
        try:
            data = json.load(response)
        except (ValueError, UnicodeError):
            raise GeminiError("Gemini API의 JSON 응답을 읽을 수 없습니다.") from None
    if not isinstance(data, dict):
        raise GeminiError("Gemini API 응답 형식을 확인할 수 없습니다.")
    return data


def model_id(value, label):
    if not value or not MODEL_ID.fullmatch(value):
        raise ValueError(f"{label} 모델 ID를 확인하세요.")
    return value


def operation_id(value):
    if not isinstance(value, str) or not OPERATION_ID.fullmatch(value):
        raise ValueError("Veo 작업 ID 형식이 올바르지 않습니다.")
    return value


def storyboard(brief, model):
    model_id(model, "Gemini")
    direction = (
        "조이티 스포츠 팀웨어·유니폼 스타일링 릴스/쇼츠의 한국어 기획 초안을 작성하세요. "
        "처음 3초의 훅, 장면 순서와 대략의 시간, 화면 문구, 촬영 컷, "
        "실사로 확인할 항목을 구분하세요. 제공되지 않은 사양·가격·납기·성과를 만들지 마세요. "
        "가상 장면은 콘셉트라고 적고 실제 납품 사례로 표현하지 마세요."
    )
    response = api_json(f"models/{model}:generateContent", {
        "systemInstruction": {"parts": [{"text": direction}]},
        "contents": [{"role": "user", "parts": [{"text": brief}]}],
    })
    try:
        parts = response["candidates"][0]["content"]["parts"]
        result = "\n".join(p["text"] for p in parts if isinstance(p.get("text"), str) and not p.get("thought"))
    except (KeyError, IndexError, AttributeError, TypeError):
        raise GeminiError("사용할 대본이 반환되지 않았습니다.") from None
    if not result.strip():
        raise GeminiError("사용할 대본이 반환되지 않았습니다.")
    return result


def start_video(prompt, model, ratio):
    model_id(model, "Veo")
    result = api_json(f"models/{model}:predictLongRunning", {
        "instances": [{"prompt": prompt}],
        "parameters": {"aspectRatio": ratio, "sampleCount": 1},
    })
    return {"operation": operation_id(result.get("name"))}


def video_uri(operation):
    if operation.get("error"):
        raise GeminiError("Veo 작업이 실패했습니다. 제공자 콘솔에서 작업 상태를 확인하세요.")
    if not operation.get("done"):
        return None
    try:
        uri = operation["response"]["generateVideoResponse"]["generatedSamples"][0]["video"]["uri"]
    except (KeyError, TypeError, IndexError):
        raise GeminiError("완료 응답에 내려받을 영상이 없습니다.") from None
    if not isinstance(uri, str) or not uri:
        raise GeminiError("완료 응답에 내려받을 영상이 없습니다.")
    return uri


def download_path(uri):
    parsed = urlsplit(uri)
    if parsed.scheme != "https" or parsed.netloc != HOST or not FILE_PATH.fullmatch(parsed.path):
        raise GeminiError("Google Gemini 파일 경로를 확인할 수 없습니다.")
    return parsed.path.removeprefix("/v1beta/") + "?alt=media"


def save_video(uri, output):
    output.parent.mkdir(parents=True, exist_ok=True)
    with closing(open_api(download_path(uri))) as response:
        first = response.read(16)
        if len(first) < 12 or first[4:8] != b"ftyp":
            raise GeminiError("응답이 MP4 영상 형식이 아닙니다.")
        with output.open("xb") as target:
            try:
                target.write(first)
                total = len(first)
                for chunk in iter(lambda: response.read(1024 * 1024), b""):
                    total += len(chunk)
                    if total > VIDEO_LIMIT:
                        raise GeminiError("영상 파일이 다운로드 크기 한도를 초과했습니다.")
                    target.write(chunk)
            except (OSError, GeminiError, TimeoutError):
                output.unlink(missing_ok=True)
                raise
    return {"saved": str(output), "bytes": total}


def read_input(path):
    text = path.read_text(encoding="utf-8").strip()
    if not text or len(text) > 15000:
        raise ValueError("입력 파일에 1~15,000자의 텍스트를 넣으세요.")
    return text


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    script = commands.add_parser("storyboard")
    script.add_argument("brief", type=Path)
    script.add_argument("--model", default=os.getenv("JOYTI_GEMINI_TEXT_MODEL", "gemini-flash-latest"))
    video = commands.add_parser("veo-start")
    video.add_argument("prompt", type=Path)
    video.add_argument("--model", default=os.getenv("JOYTI_VEO_MODEL"))
    video.add_argument("--aspect-ratio", choices=("9:16", "16:9"), default="9:16")
    video.add_argument("--generate", action="store_true",
                       help="실제 Veo 영상 생성 요청을 1회 전송합니다.")
    commands.add_parser("veo-status").add_argument("operation")
    download = commands.add_parser("veo-download")
    download.add_argument("operation")
    download.add_argument("output", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "storyboard":
            print(storyboard(read_input(args.brief), args.model))
            return 0
        if args.command == "veo-start":
            if not args.generate:
                raise ValueError("실제 영상 생성 요청에는 --generate가 필요합니다.")
            result = start_video(read_input(args.prompt), args.model, args.aspect_ratio)
        else:
            operation = api_json(operation_id(args.operation))
            uri = video_uri(operation)
            if args.command == "veo-status":
                result = {"operation": args.operation, "state": "ready" if uri else "pending"}
            elif uri:
                result = save_video(uri, args.output)
            else:
                raise GeminiError("아직 생성 중입니다. 같은 작업 ID를 다시 확인하세요.")
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except (GeminiError, ValueError, OSError) as exc:
        print(f"오류: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
