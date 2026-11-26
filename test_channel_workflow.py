from contextlib import closing
import json
from pathlib import Path
import tempfile
from threading import Thread
import unittest
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from channel_workflow import BatchConflict, DraftServer, create_batch
from joyti import get_post, open_db


class ChannelWorkflowTest(unittest.TestCase):
    def setUp(self):
        self.tmp = self.enterContext(tempfile.TemporaryDirectory())
        self.path = Path(self.tmp) / "test.sqlite3"
        self.db = self.enterContext(closing(open_db(self.path)))
        self.request = json.loads(Path(__file__).with_name("workflows").joinpath(
            "example-drafts.json").read_text())

    def test_retries_do_not_duplicate_or_change_an_existing_batch(self):
        first = create_batch(self.db, self.request)
        self.assertTrue(first["created"])
        self.assertEqual([p["channel"] for p in first["posts"]],
                         ["instagram", "blog", "kin", "youtube"])
        self.assertTrue(all(p["state"] == "draft" for p in first["posts"]))
        retry = create_batch(self.db, self.request)
        self.assertFalse(retry["created"])
        self.assertEqual(first["posts"], retry["posts"])
        post = get_post(self.db, first["posts"][2]["id"])
        self.assertIn("kin.naver.com", post["source_url"])
        self.request["drafts"]["blog"]["body"] = "다른 내용"
        with self.assertRaises(BatchConflict):
            create_batch(self.db, self.request)

    def test_invalid_channel_does_not_insert_a_partial_batch(self):
        self.request["drafts"]["kin"]["source_url"] = "https://example.com/question"
        with self.assertRaises(ValueError):
            create_batch(self.db, self.request)
        self.assertEqual(self.db.execute("SELECT count(*) FROM posts").fetchone()[0], 0)

    def test_local_http_authentication_and_idempotency(self):
        token = "workflow-test-token-only-123"
        with DraftServer(0, self.path, token) as server:
            thread = Thread(target=server.serve_forever)
            thread.start()
            try:
                endpoint = f"http://127.0.0.1:{server.server_port}/drafts"
                data = json.dumps(self.request).encode()
                with self.assertRaises(HTTPError) as error:
                    urlopen(Request(endpoint, data=data), timeout=3)
                self.assertEqual(error.exception.code, 401)
                error.exception.close()
                for expected in (201, 200):
                    request = Request(endpoint, data=data, headers={"Authorization": f"Bearer {token}"})
                    with urlopen(request, timeout=3) as response:
                        self.assertEqual(response.status, expected)
                        self.assertEqual(len(json.load(response)["posts"]), 4)
            finally:
                server.shutdown()
                thread.join()
