"""Local publishing queue and Knowledge iN archive for Joyti."""

import argparse
import json
import os
import re
import sqlite3
import sys
from contextlib import closing
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

from publishers import prepare

CHANNELS = ("instagram", "blog", "cafe")
SCHEMA = """
CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY,
    channel TEXT NOT NULL,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    image_url TEXT,
    state TEXT NOT NULL DEFAULT 'draft'
        CHECK (state IN ('draft', 'approved', 'sending', 'published', 'needs_review')),
    remote_id TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS knowledge (
    source_id TEXT PRIMARY KEY,
    url TEXT NOT NULL,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""


def open_db(path):
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    db = sqlite3.connect(path)
    db.row_factory = sqlite3.Row
    db.executescript(SCHEMA)
    return db


def https_url(value, expected_host=None):
    url = urlsplit(value)
    if (url.scheme != "https" or not url.hostname or url.username is not None
            or url.password is not None
            or (expected_host and url.netloc.lower() != expected_host)):
        raise ValueError("올바른 HTTPS URL이 필요합니다.")
    return url


def create_post(db, args):
    title = args.title.strip()
    body = args.body_file.read_text(encoding="utf-8").strip()
    if not title or not body:
        raise ValueError("제목과 본문을 입력하세요.")
    if args.channel == "instagram":
        if not args.image_url:
            raise ValueError("인스타그램 이미지의 공개 HTTPS URL이 필요합니다.")
        https_url(args.image_url)
    elif args.image_url:
        raise ValueError("--image-url은 인스타그램 이미지를 발행할 때 사용합니다.")
    with db:
        cursor = db.execute(
            "INSERT INTO posts(channel, title, body, image_url) VALUES (?, ?, ?, ?)",
            (args.channel, title, body, args.image_url),
        )
    return {"id": cursor.lastrowid, "state": "draft"}


def get_post(db, post_id):
    row = db.execute("SELECT * FROM posts WHERE id = ?", (post_id,)).fetchone()
    if row is None:
        raise ValueError("해당 게시물이 없습니다.")
    return dict(row)


def transition(db, post_id, before, after, remote_id=None):
    with db:
        cursor = db.execute(
            "UPDATE posts SET state = ?, remote_id = ? WHERE id = ? AND state = ?",
            (after, remote_id, post_id, before),
        )
        if cursor.rowcount != 1:
            raise ValueError(f"게시물 {post_id}의 상태가 {before}일 때만 실행할 수 있습니다.")


def publish(db, args):
    post = get_post(db, args.id)
    if post["channel"] == "blog":
        raise ValueError("블로그에 직접 게시한 뒤 record-published를 사용하세요.")
    if post["state"] != "approved":
        raise ValueError("승인 상태인 게시물만 발행할 수 있습니다.")
    if not args.send:
        return {"mode": "preview", "post": post}

    send = prepare(post)
    transition(db, args.id, "approved", "sending")
    try:
        remote_id = send()
        transition(db, args.id, "sending", "published", remote_id)
    except Exception:
        transition(db, args.id, "sending", "needs_review")
        raise
    return {"id": args.id, "state": "published", "remote_id": remote_id}


def record_published(db, args):
    post = get_post(db, args.id)
    states = ("approved",) if post["channel"] == "blog" else ("needs_review", "sending")
    if post["state"] not in states:
        raise ValueError("현재 상태에서는 발행 결과를 기록할 수 없습니다.")
    https_url(args.url)
    transition(db, args.id, post["state"], "published", args.url)
    return {"id": args.id, "state": "published", "remote_id": args.url}


def import_knowledge(db, path):
    entries = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
        if not line.strip():
            continue
        try:
            entry = json.loads(line)
            fields = tuple(entry[key].strip() for key in ("url", "question", "answer"))
            url = https_url(fields[0], "kin.naver.com")
            doc_ids = parse_qs(url.query).get("docId", [])
            if (len(doc_ids) != 1 or not re.fullmatch(r"[0-9]+", doc_ids[0])
                    or not fields[1] or not fields[2]):
                raise ValueError("docId, 질문, 답변이 필요합니다.")
            entries.append((doc_ids[0], *fields))
        except (ValueError, TypeError, AttributeError, KeyError) as exc:
            raise ValueError(f"지식iN 입력 {line_no}행의 형식이 올바르지 않습니다.") from exc
    with db:
        db.executemany(
            """INSERT INTO knowledge(source_id, url, question, answer) VALUES (?, ?, ?, ?)
               ON CONFLICT(source_id) DO UPDATE SET url = excluded.url,
                   question = excluded.question, answer = excluded.answer,
                   updated_at = CURRENT_TIMESTAMP
               WHERE knowledge.url != excluded.url OR knowledge.question != excluded.question
                   OR knowledge.answer != excluded.answer""",
            entries,
        )
    return {"processed": len(entries)}


def parser():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--db", type=Path, default=os.getenv("JOYTI_DB", ".local/joyti.sqlite3"))
    commands = cli.add_subparsers(dest="command", required=True)
    commands.add_parser("init")
    draft = commands.add_parser("draft")
    draft.add_argument("channel", choices=CHANNELS)
    draft.add_argument("--title", required=True)
    draft.add_argument("--body-file", type=Path, required=True)
    draft.add_argument("--image-url")
    listing = commands.add_parser("list")
    listing.add_argument("--channel", choices=CHANNELS)
    for name in ("show", "approve", "publish", "record-published"):
        command = commands.add_parser(name)
        command.add_argument("id", type=int)
        if name == "publish":
            command.add_argument("--send", action="store_true")
        if name == "record-published":
            command.add_argument("url")
    commands.add_parser("kin-import").add_argument("file", type=Path)
    commands.add_parser("kin-search").add_argument("query")
    return cli


def run(db, args):
    match args.command:
        case "init":
            return {"db": str(args.db)}
        case "draft":
            return create_post(db, args)
        case "list":
            return [dict(row) for row in db.execute(
                """SELECT id, channel, title, state, remote_id FROM posts
                   WHERE (? IS NULL OR channel = ?) ORDER BY id DESC""",
                (args.channel, args.channel),
            )]
        case "show":
            return get_post(db, args.id)
        case "approve":
            transition(db, args.id, "draft", "approved")
            return {"id": args.id, "state": "approved"}
        case "publish":
            return publish(db, args)
        case "record-published":
            return record_published(db, args)
        case "kin-import":
            return import_knowledge(db, args.file)
        case "kin-search":
            return [dict(row) for row in db.execute(
                """SELECT source_id, url, question, answer FROM knowledge
                   WHERE instr(question, ?) OR instr(answer, ?)
                   ORDER BY updated_at DESC, source_id LIMIT 100""",
                (args.query, args.query),
            )]


def main():
    args = parser().parse_args()
    try:
        with closing(open_db(args.db)) as db:
            result = run(db, args)
    except (ValueError, OSError, RuntimeError, sqlite3.Error) as exc:
        print(f"오류: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
