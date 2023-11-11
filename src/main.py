import asyncio
from datetime import datetime
from typing import Annotated

from fastapi import FastAPI, Header, Response, status
from pydantic import BaseModel, Field

from src.settings import get_settings
from src.telegram_api import TelegramApi

settings = get_settings()

app = FastAPI()
bot = TelegramApi(settings.telegram_bot_token)


class User(BaseModel):
    id: int
    first_name: str | None = None
    last_name: str | None = None
    username: str | None = None


class Message(BaseModel):
    message_id: int
    from_user: User = Field(alias="from")


class Update(BaseModel):
    update_id: int
    message: Message | None = None


@app.get("/")
async def read_root() -> dict[str, bool]:
    return {"success": True}


@app.post("/telegram")
async def receive_update(
    update: Update,
    x_telegram_bot_api_secret_token: Annotated[str | None, Header()] = "",
) -> Response:
    if x_telegram_bot_api_secret_token != settings.secret_token:
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)

    await bot.send_message(
        update.message.from_user.id,
        datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S.%f %Z"),
    )

    await asyncio.sleep(5)

    await bot.send_message(
        update.message.from_user.id,
        datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S.%f %Z"),
    )

    return Response(status_code=status.HTTP_200_OK)
