"""Create and review a four-channel batch through the CLI or a local n8n webhook."""

import argparse
from contextlib import closing
from hashlib import sha256
from hmac import compare_digest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import re
import sqlite3
import sys

from joyti import https_url, open_db

CHANNELS = ("instagram", "blog", "kin", "youtube")
MAX_PAYLOAD = 512 * 1024


class BatchConflict(ValueError):
    pass


def text(obj, key, maximum):
    value = obj.get(key)
    if not isinstance(value, str) or not value.strip() or len(value) > maximum:
        raise ValueError(f"{key}: 1~{maximum}자의 텍스트가 필요합니다.")
    return value.strip()


def url(obj, key, host=None):
    if key not in obj:
        return None
    value = text(obj, key, 2048)
    if any(ch.isspace() for ch in value):
        raise ValueError(f"{key}: URL에 공백을 넣을 수 없습니다.")
    https_url(value, host)
    return value


def normalize(payload):
    if not isinstance(payload, dict):
        raise ValueError("요청은 JSON 객체여야 합니다.")
    request_id = text(payload, "request_id", 80)
    if not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9._-]*", request_id):
        raise ValueError("request_id에는 영문, 숫자, 점, 밑줄, 하이픈을 사용하세요.")
    note = text(payload, "source_note", 12000)
    drafts = payload.get("drafts")
    if not isinstance(drafts, dict) or set(drafts) != set(CHANNELS):
        raise ValueError("drafts에 instagram, blog, kin, youtube 초안을 각각 넣으세요.")
    normalized = {}
    for channel in CHANNELS:
        draft = drafts[channel]
        if not isinstance(draft, dict):
            raise ValueError(f"{channel} 초안은 JSON 객체여야 합니다.")
        title = text(draft, "title", 160)
        body = text(draft, "body", 25000)
        source_url = url(draft, "source_url", "kin.naver.com" if channel == "kin" else None)
        image_url = url(draft, "image_url")
        video_url = url(draft, "video_url")
        if channel == "kin" and not source_url:
            raise ValueError("지식iN 원본 질문 URL이 필요합니다.")
        if channel == "instagram" and bool(image_url) == bool(video_url):
            raise ValueError("인스타그램은 image_url 또는 video_url 중 하나가 필요합니다.")
        if channel == "youtube" and not video_url:
            raise ValueError("유튜브 영상의 video_url이 필요합니다.")
        if (image_url and channel != "instagram") or (
            video_url and channel not in {"instagram", "youtube"}
        ):
            raise ValueError(f"{channel}에서는 지정한 게시 미디어 형식을 사용할 수 없습니다.")
        normalized[channel] = {
            "title": title, "body": body, "image_url": image_url,
            "source_url": source_url, "video_url": video_url,
        }
    return request_id, note, normalized


def batch_status(db, request_id):
    batch = db.execute(
        "SELECT source_note FROM channel_batches WHERE request_id = ?", (request_id,)
    ).fetchone()
    if batch is None:
        raise ValueError("해당 요청 번호가 없습니다.")
    posts = db.execute(
        """SELECT posts.id, posts.channel, posts.state, posts.remote_id
           FROM batch_posts JOIN posts ON batch_posts.post_id = posts.id
           WHERE batch_posts.request_id = ? ORDER BY posts.id""",
        (request_id,),
    )
    return {"request_id": request_id, "source_note": batch["source_note"],
            "posts": [dict(p) for p in posts]}


def create_batch(db, payload):
    request_id, note, drafts = normalize(payload)
    data = json.dumps((note, drafts), sort_keys=True, ensure_ascii=False).encode()
    fingerprint = sha256(data).hexdigest()
    with db:
        inserted = db.execute(
            """INSERT INTO channel_batches(request_id, fingerprint, source_note) VALUES (?, ?, ?)
               ON CONFLICT(request_id) DO NOTHING""",
            (request_id, fingerprint, note),
        ).rowcount
        if not inserted:
            old = db.execute(
                "SELECT fingerprint FROM channel_batches WHERE request_id = ?", (request_id,)
            ).fetchone()
            if old["fingerprint"] != fingerprint:
                raise BatchConflict("같은 요청 번호에 다른 초안이 들어왔습니다. 새 요청 번호를 사용하세요.")
        else:
            for channel, draft in drafts.items():
                post = db.execute(
                    "INSERT INTO posts(channel, title, body, image_url) VALUES (?, ?, ?, ?)",
                    (channel, draft["title"], draft["body"], draft["image_url"]),
                )
                db.execute(
                    """INSERT INTO batch_posts(request_id, post_id, channel, source_url, video_url)
                       VALUES (?, ?, ?, ?, ?)""",
                    (request_id, post.lastrowid, channel, draft["source_url"], draft["video_url"]),
                )
        return {**batch_status(db, request_id), "created": bool(inserted)}


class DraftServer(ThreadingHTTPServer):
    def __init__(self, port, db_path, token):
        self.db_path = db_path
        self.auth_header = f"Bearer {token}".encode()
        super().__init__(("127.0.0.1", port), DraftHandler)


class DraftHandler(BaseHTTPRequestHandler):
    def respond(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        if self.path != "/drafts":
            return self.respond(404, {"error": "지원하지 않는 경로"})
        supplied = self.headers.get("Authorization", "").encode()
        if not compare_digest(supplied, self.server.auth_header):
            return self.respond(401, {"error": "워크플로 인증이 필요합니다."})
        length = self.headers.get("Content-Length", "")
        if len(length) > 6 or not length.isascii() or not length.isdecimal() or not 0 < int(length) <= MAX_PAYLOAD:
            return self.respond(413, {"error": "요청 크기가 허용 범위를 벗어났습니다."})
        try:
            self.connection.settimeout(15)
            payload = json.loads(self.rfile.read(int(length)))
            with closing(open_db(self.server.db_path)) as db:
                result = create_batch(db, payload)
        except BatchConflict as exc:
            return self.respond(409, {"error": str(exc)})
        except (ValueError, TimeoutError):
            return self.respond(400, {"error": "JSON 또는 초안 형식이 올바르지 않습니다."})
        except sqlite3.Error:
            return self.respond(503, {"error": "잠시 후 같은 요청 번호로 다시 시도하세요."})
        return self.respond(201 if result["created"] else 200, result)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, default=os.getenv("JOYTI_DB", ".local/joyti.sqlite3"))
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("draft").add_argument("payload", type=Path)
    sub.add_parser("status").add_argument("request_id")
    sub.add_parser("serve").add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    try:
        if args.command == "serve":
            token = os.getenv("JOYTI_WORKFLOW_TOKEN", "")
            if not re.fullmatch(r"[a-zA-Z0-9._-]{24,}", token):
                raise ValueError("JOYTI_WORKFLOW_TOKEN에는 24자 이상의 임의 문자열이 필요합니다.")
            with closing(open_db(args.db)), DraftServer(args.port, args.db, token) as server:
                print(f"Draft API listening on 127.0.0.1:{server.server_port}", flush=True)
                server.serve_forever()
        else:
            with closing(open_db(args.db)) as db:
                result = (create_batch(db, json.loads(args.payload.read_text(encoding="utf-8")))
                          if args.command == "draft" else batch_status(db, args.request_id))
            print(json.dumps(result, ensure_ascii=False, indent=2))
    except KeyboardInterrupt:
        return 0
    except (ValueError, OSError, sqlite3.Error) as exc:
        print(f"오류: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
