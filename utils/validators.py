async def shop_username_validate(username: str) -> str:
    if username.startswith("t.me") or username.startswith("https"):
        return "@" + username.split("/")[-1]

    return username
