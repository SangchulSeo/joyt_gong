"""Explicit, single-post publishing through platform APIs."""

import json
from html import escape
import os
import re
from urllib.error import HTTPError, URLError
from urllib.parse import quote_plus, urlencode
from urllib.request import HTTPRedirectHandler, Request, build_opener


class ApiError(RuntimeError):
    pass


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def post_form(url, token, fields):
    request = Request(
        url,
        data=urlencode(fields).encode("ascii"),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        },
    )
    try:
        with build_opener(NoRedirect()).open(request, timeout=30) as response:
            result = json.load(response)
    except HTTPError as exc:
        code = exc.code
        exc.close()
        raise ApiError(f"플랫폼 API가 HTTP {code}을 반환했습니다. 게시 여부를 확인하세요.") from None
    except (URLError, TimeoutError, ValueError):
        raise ApiError("플랫폼 API 응답을 확인할 수 없습니다. 게시 여부를 확인하세요.") from None
    if not isinstance(result, dict):
        raise ApiError("플랫폼 API 응답 형식이 올바르지 않습니다.")
    return result


def required(name, pattern=None):
    value = os.getenv(name, "").strip()
    if not value or (pattern and not re.fullmatch(pattern, value)):
        raise ValueError(f"환경 설정에서 {name}을 올바르게 지정하세요.")
    return value


def result_id(value):
    if isinstance(value, (str, int)) and not isinstance(value, bool) and str(value).strip():
        return str(value)
    raise ApiError("플랫폼 응답에 게시물 ID가 없습니다. 게시 여부를 확인하세요.")


def prepare(post):
    if post["channel"] == "instagram":
        token = required("JOYTI_IG_ACCESS_TOKEN")
        account = required("JOYTI_IG_USER_ID", r"[0-9]+")
        version = required("JOYTI_IG_API_VERSION", r"v[0-9]+\.[0-9]+")
        base = f"https://graph.instagram.com/{version}/{account}"

        def send():
            media = post_form(f"{base}/media", token, {
                "image_url": post["image_url"], "caption": post["body"],
            })
            published = post_form(f"{base}/media_publish", token, {
                "creation_id": result_id(media.get("id")),
            })
            return result_id(published.get("id"))

        return send

    if post["channel"] == "cafe":
        token = required("JOYTI_NAVER_ACCESS_TOKEN")
        cafe = required("JOYTI_NAVER_CAFE_ID", r"[0-9]+")
        menu = required("JOYTI_NAVER_MENU_ID", r"[0-9]+")
        url = f"https://openapi.naver.com/v1/cafe/{cafe}/menu/{menu}/articles"

        def send():
            response = post_form(url, token, {
                # Naver expects UTF-8 form encoding followed by a second form encoding.
                "subject": quote_plus(post["title"]),
                "content": quote_plus(escape(post["body"]).replace("\n", "<br>")),
                "openyn": "false",
            })
            try:
                article_id = response["message"]["result"]["articleId"]
            except (KeyError, TypeError):
                raise ApiError("카페 응답에 게시물 ID가 없습니다. 카페에서 확인하세요.") from None
            return result_id(article_id)

        return send

    raise ValueError("이 채널에는 API 발행이 설정되지 않았습니다.")
