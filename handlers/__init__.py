from . import users
from . import admins


routers_list = [
    admins.start.router,
    users.users.router,
]

__all__ = [
    "routers_list",
]

