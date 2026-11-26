import json
import os
import tempfile
import unittest
from contextlib import closing
from pathlib import Path
from unittest.mock import patch
from urllib.parse import unquote_plus

import joyti
import publishers


class WorkflowTest(unittest.TestCase):
    def setUp(self):
        directory = self.enterContext(tempfile.TemporaryDirectory())
        self.root = Path(directory)
        self.db = self.enterContext(closing(joyti.open_db(self.root / "test.sqlite3")))
        self.body = self.root / "body.txt"
        self.body.write_text("조이티 소식\n<&>", encoding="utf-8")

    def run_command(self, *args):
        return joyti.run(self.db, joyti.parser().parse_args(args))

    def draft(self, channel, *options):
        return self.run_command(
            "draft", channel, "--title", "첫 게시물", "--body-file", str(self.body), *options
        )["id"]

    def test_blog_review_and_record(self):
        post_id = str(self.draft("blog"))
        self.assertEqual(self.run_command("show", post_id)["body"], "조이티 소식\n<&>")
        self.run_command("approve", post_id)
        self.run_command("record-published", post_id, "https://blog.naver.com/joyti/123")
        self.assertEqual(self.run_command("list", "--channel", "blog")[0]["state"], "published")

    @patch("publishers.post_form", side_effect=[{"id": "10"}, {"id": "20"}])
    def test_instagram_preview_and_send(self, post_form):
        post_id = str(self.draft("instagram", "--image-url", "https://example.com/image.jpg"))
        with self.assertRaisesRegex(ValueError, "승인"):
            self.run_command("publish", post_id, "--send")
        self.run_command("approve", post_id)
        self.assertEqual(self.run_command("publish", post_id)["mode"], "preview")
        post_form.assert_not_called()
        with patch.dict(os.environ, {
            "JOYTI_IG_ACCESS_TOKEN": "test-token",
            "JOYTI_IG_USER_ID": "42",
            "JOYTI_IG_API_VERSION": "v25.0",
        }):
            self.assertEqual(self.run_command("publish", post_id, "--send")["remote_id"], "20")
        first, second = post_form.call_args_list
        self.assertEqual(first.args[0], "https://graph.instagram.com/v25.0/42/media")
        self.assertEqual(first.args[2]["image_url"], "https://example.com/image.jpg")
        self.assertEqual(second.args[0], "https://graph.instagram.com/v25.0/42/media_publish")
        self.assertEqual(second.args[2], {"creation_id": "10"})
        with self.assertRaisesRegex(ValueError, "승인"):
            self.run_command("publish", post_id, "--send")
        self.assertEqual(post_form.call_count, 2)

    @patch("publishers.post_form")
    def test_cafe_success_and_uncertain_result(self, post_form):
        with patch.dict(os.environ, {
            "JOYTI_NAVER_ACCESS_TOKEN": "test-token",
            "JOYTI_NAVER_CAFE_ID": "42",
            "JOYTI_NAVER_MENU_ID": "13",
        }):
            first, second = str(self.draft("cafe")), str(self.draft("cafe"))
            self.run_command("approve", first)
            self.run_command("approve", second)
            post_form.return_value = {"message": {"result": {"articleId": 345}}}
            self.assertEqual(self.run_command("publish", first, "--send")["remote_id"], "345")
            url, _, fields = post_form.call_args.args
            self.assertEqual(url, "https://openapi.naver.com/v1/cafe/42/menu/13/articles")
            self.assertEqual(unquote_plus(fields["subject"]), "첫 게시물")
            self.assertEqual(unquote_plus(fields["content"]), "조이티 소식<br>&lt;&amp;&gt;")
            self.assertEqual(fields["openyn"], "false")

            post_form.side_effect = publishers.ApiError("테스트 오류")
            with self.assertRaises(publishers.ApiError):
                self.run_command("publish", second, "--send")
            self.assertEqual(self.run_command("show", second)["state"], "needs_review")
            with self.assertRaisesRegex(ValueError, "승인"):
                self.run_command("publish", second, "--send")
            self.assertEqual(post_form.call_count, 2)

    def test_knowledge_import_updates_and_rejects_invalid_batch(self):
        path = self.root / "knowledge.jsonl"
        entry = {"url": "https://kin.naver.com/qna/detail.naver?docId=123",
                 "question": "운영 시간은?", "answer": "오전 운영"}
        path.write_text(json.dumps(entry), encoding="utf-8")
        self.run_command("kin-import", str(path))
        entry["answer"] = "오후 운영"
        path.write_text(json.dumps(entry) + "\n{}", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "2행"):
            self.run_command("kin-import", str(path))
        self.assertEqual(self.run_command("kin-search", "오전")[0]["source_id"], "123")
        path.write_text(json.dumps(entry), encoding="utf-8")
        self.run_command("kin-import", str(path))
        self.run_command("kin-import", str(path))
        self.assertEqual(len(self.run_command("kin-search", "운영")), 1)
        self.assertEqual(self.run_command("kin-search", "오전"), [])
