"""Shared requests.Session: base URL, logging and Allure attachments per request/response."""

import json
import logging
from typing import Any

import allure
import requests

from src.config.settings import get_settings

logger = logging.getLogger("api")


class HttpClient:
    """Wraps requests.Session so every call is logged and attached to the Allure report."""

    def __init__(self) -> None:
        settings = get_settings()
        self.session = requests.Session()
        self.base_url = settings.base_url.rstrip("/")
        self.timeout = settings.timeout
        self.session.headers["Accept"] = "application/json"

    def request(self, method: str, path: str, **kwargs: Any) -> requests.Response:
        url = f"{self.base_url}{path}"
        kwargs.setdefault("timeout", self.timeout)

        logger.info(
            "-> %s %s params=%s json=%s",
            method.upper(),
            url,
            kwargs.get("params"),
            kwargs.get("json"),
        )
        response = self.session.request(method, url, **kwargs)
        logger.info(
            "<- %s %s (%.0f ms)",
            response.status_code,
            response.reason,
            response.elapsed.total_seconds() * 1000,
        )

        self._attach_to_allure(method, url, response)
        return response

    def get(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request("POST", path, **kwargs)

    def put(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request("PUT", path, **kwargs)

    def patch(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request("PATCH", path, **kwargs)

    def delete(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request("DELETE", path, **kwargs)

    @staticmethod
    def _attach_to_allure(method: str, url: str, response: requests.Response) -> None:
        request_body = response.request.body
        if isinstance(request_body, bytes):
            request_body = request_body.decode("utf-8", errors="replace")

        allure.attach(
            json.dumps(
                {
                    "method": method.upper(),
                    "url": url,
                    "request_body": request_body,
                },
                ensure_ascii=False,
                indent=2,
            ),
            name=f"Request: {method.upper()} {path_of(url)}",
            attachment_type=allure.attachment_type.JSON,
        )
        try:
            response_body = json.dumps(response.json(), ensure_ascii=False, indent=2)
        except ValueError:
            response_body = response.text

        response_report = json.dumps(
            {"status_code": response.status_code, "body": response_body},
            ensure_ascii=False,
            indent=2,
        )
        allure.attach(
            response_report,
            name=f"Response: {response.status_code} {path_of(url)}",
            attachment_type=allure.attachment_type.JSON,
        )


def path_of(url: str) -> str:
    from urllib.parse import urlparse

    return urlparse(url).path or "/"
