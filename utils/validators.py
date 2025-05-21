from aiogram.types import Message


async def shop_username_validate(username: str) -> str:
    if username.startswith("t.me") or username.startswith("https"):
        return "@" + username.split("/")[-1]

    return username

MAX_LENGTH = 4096

async def send_long_text(message: Message, text: str):
    lines = text.splitlines(keepends=True)
    current_chunk = ""
    for line in lines:
        # If adding the next line would exceed the max length, send the current chunk
        if len(current_chunk) + len(line) > MAX_LENGTH:
            await message.answer(current_chunk, disable_web_page_preview=True)
            current_chunk = ""
        current_chunk += line

    # Send any remaining text
    if current_chunk:
        await message.answer(current_chunk, disable_web_page_preview=True)