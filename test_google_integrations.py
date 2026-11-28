"""Offline checks for Joyti's Google API workflows."""

from contextlib import redirect_stderr
import io
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch
from urllib.parse import parse_qs, urlsplit

import gemini_video
import google_sheets


class VideoTests(unittest.TestCase):
    @patch("gemini_video.api_json", return_value={
        "candidates": [{"content": {"parts": [{"text": "장면 구성"}]}}],
    })
    def test_storyboard(self, api):
        self.assertEqual(gemini_video.storyboard("농구 유니폼", "gemini-flash-latest"), "장면 구성")
        path, payload = api.call_args.args
        self.assertEqual(path, "models/gemini-flash-latest:generateContent")
        self.assertIn("처음 3초", payload["systemInstruction"]["parts"][0]["text"])
        self.assertEqual(payload["contents"][0]["parts"][0]["text"], "농구 유니폼")

    @patch("gemini_video.api_json")
    def test_explicit_single_generation(self, api):
        with TemporaryDirectory() as directory:
            prompt = Path(directory) / "scene.txt"
            prompt.write_text("스포츠 콘셉트", encoding="utf-8")
            argv = ["gemini_video.py", "veo-start", str(prompt), "--model", "veo-test"]
            with patch("sys.argv", argv), redirect_stderr(io.StringIO()):
                self.assertEqual(gemini_video.main(), 1)
            api.assert_not_called()
            api.return_value = {"name": "models/veo-test/operations/123"}
            with patch("sys.argv", [*argv, "--generate"]), patch("builtins.print"):
                self.assertEqual(gemini_video.main(), 0)
        api.assert_called_once_with(
            "models/veo-test:predictLongRunning",
            {"instances": [{"prompt": "스포츠 콘셉트"}],
             "parameters": {"aspectRatio": "9:16", "sampleCount": 1}},
        )

    @patch("gemini_video.open_api")
    def test_download_path_and_file(self, api):
        valid_uri = f"https://{gemini_video.HOST}/v1beta/files/abc:download?alt=media"
        mp4 = b"\x00\x00\x00\x10ftypmp42\x00\x00\x00\x00"
        with TemporaryDirectory() as directory:
            output = Path(directory) / "clip.mp4"
            with self.assertRaises(gemini_video.GeminiError):
                gemini_video.save_video("https://example.com/v1beta/files/abc:download", output)
            api.assert_not_called()
            api.return_value = io.BytesIO(mp4)
            gemini_video.save_video(valid_uri, output)
            api.assert_called_once_with("files/abc:download?alt=media")
            self.assertEqual(output.read_bytes(), mp4)
            api.return_value = io.BytesIO(mp4 + b"another clip")
            with self.assertRaises(FileExistsError):
                gemini_video.save_video(valid_uri, output)
            self.assertEqual(output.read_bytes(), mp4)


class SheetsTests(unittest.TestCase):
    @patch("google_sheets.call_api")
    def test_create_and_verify_native_sheet(self, api):
        template = google_sheets.sheet_template()
        api.side_effect = [
            {"spreadsheetId": "test_sheet"},
            {"valueRanges": [
                {"values": [template[0]["values"][3]]},
                {"values": [row[:4] for row in template[1]["values"][3:]]},
            ]},
        ]
        result = google_sheets.create_kin_sheet()
        self.assertEqual(result["keywords"], 29)
        self.assertEqual(result["url"], "https://docs.google.com/spreadsheets/d/test_sheet/edit")
        self.assertEqual(api.call_count, 2)
        created, checked = api.call_args_list
        question, keyword = created.kwargs["payload"]["sheets"]
        self.assertEqual(question["properties"]["title"], "질문·답변 관리")
        self.assertEqual(question["properties"]["gridProperties"]["frozenRowCount"], 4)
        self.assertEqual(keyword["basicFilter"]["range"]["startRowIndex"], 3)
        row = question["data"][0]["rowData"][4]["values"]
        self.assertEqual(row[7]["dataValidation"]["condition"]["type"], "ONE_OF_LIST")
        read = urlsplit(checked.args[0])
        self.assertEqual(read.path, "/test_sheet/values:batchGet")
        self.assertEqual(parse_qs(read.query)["ranges"], ["'질문·답변 관리'!A4:K4", "'검색 키워드'!A4:D33"])

    @patch("google_sheets.call_api", side_effect=[{"spreadsheetId": "test_sheet"}, {}])
    def test_failed_readback_preserves_created_link(self, api):
        with self.assertRaisesRegex(google_sheets.SheetsError, "/test_sheet/edit"):
            google_sheets.create_kin_sheet()
        self.assertEqual(api.call_count, 2)


if __name__ == "__main__":
    unittest.main()
