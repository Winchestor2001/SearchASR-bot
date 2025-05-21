from aiogram.types import Message


async def shop_username_validate(username: str) -> str:
    if username.startswith("t.me") or username.startswith("https"):
        return "@" + username.split("/")[-1]

    return username

MAX_LENGTH = 4096

async def send_long_text(message: Message, text: str, btn = None):
    lines = text.splitlines(keepends=True)
    current_chunk = ""
    for line in lines:
        # If adding the next line would exceed the max length, send the current chunk
        if len(current_chunk) + len(line) > MAX_LENGTH:
            await message.answer(current_chunk, disable_web_page_preview=True, reply_markup=btn)
            current_chunk = ""
        current_chunk += line

    # Send any remaining text
    if current_chunk:
        await message.answer(current_chunk, disable_web_page_preview=True, reply_markup=btn)


async def send_long_text_2(message: Message, text: str, btn=None):
    while len(text) > MAX_LENGTH:
        # Find the last newline before the max length to split cleanly
        split_pos = text.rfind('\n', 0, MAX_LENGTH)
        if split_pos == -1:
            # If no newline found, force split at max length
            split_pos = MAX_LENGTH

        chunk = text[:split_pos].strip()
        await message.answer(chunk, disable_web_page_preview=True)
        text = text[split_pos:].lstrip()  # Continue with the rest

    # Send the remaining part
    if text:
        await message.answer(text, disable_web_page_preview=True, reply_markup=btn)