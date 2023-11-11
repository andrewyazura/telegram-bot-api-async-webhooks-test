from typing import Any
from urllib.parse import urljoin

import httpx


class TelegramApi:
    def __init__(self, token: str) -> None:
        self._async_client = httpx.AsyncClient(
            headers={"Content-Type": "application/json"}
        )
        self._base_url = f"https://api.telegram.org/bot{token}/"

    async def send_message(self, chat_id: int, text: str):  # -> dict:
        return await self._send_telegram_request(
            "sendMessage", {"chat_id": chat_id, "text": text}
        )

    def _make_url(self, method: str) -> str:
        return urljoin(self._base_url, method)

    async def _send_telegram_request(self, method: str, data: dict[str, Any]) -> dict:
        response = await self._async_client.post(url=self._make_url(method), json=data)

        response_data = response.json()

        if response_data["ok"] is False:
            raise Exception(response_data["description"])

        return response.json()
