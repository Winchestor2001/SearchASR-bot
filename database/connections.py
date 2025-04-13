from .models import Sellers, Shops, Users, db
from peewee import DoesNotExist
from datetime import datetime


async def add_user(user_id, full_name, username=None):
    with db.atomic():
        if not Users.select().where(Users.user_id == user_id).exists():
            Users.create(user_id=user_id, username=username, full_name=full_name)


def add_seller(username: str, status: str = "trusted"):
    username = username.lower()
    existing = Sellers.select().where(Sellers.username == username).first()
    if existing:
        return existing  # already exists

    count = Sellers.select().where(Sellers.status == status).count()
    seller = Sellers.create(
        username=username,
        status=status,
        index=count + 1,
    )
    return seller


def get_seller(username: str):
    try:
        return Sellers.get(Sellers.username == username.lower())
    except DoesNotExist:
        return None


def update_seller_status(username: str, status: str):
    seller = get_seller(username)
    if seller:
        seller.status = status
        seller.save()
        return seller
    return None


def delete_seller_by_index(status: str, username: str):
    seller = Sellers.select().where(
        (Sellers.username == username) & (Sellers.status == status)
    ).first()
    if seller:
        seller.delete_instance()
        _reorder_indexes(Sellers, status)
        return True
    return False


def add_shop(name: str, username: str, status: str = "trusted", description: str = None):
    username = username.lower()
    existing = Shops.select().where(Shops.username == username).first()
    if existing:
        return existing

    count = Shops.select().where(Shops.status == status).count()
    shop = Shops.create(
        name=name,
        username=username,
        status=status,
        description=description,
        index=count + 1
    )
    return shop


def get_shop_by_username(username: str):
    try:
        return Shops.get(Shops.username == username.lower())
    except DoesNotExist:
        return None


def update_shop_status(username: str, status: str):
    shop = get_shop_by_username(username)
    if shop:
        shop.status = status
        shop.save()
        return shop
    return None


def delete_shop_by_index(status: str, index: int):
    shop = Shops.select().where(
        (Shops.status == status) & (Shops.index == index)
    ).first()
    if shop:
        shop.delete_instance()
        _reorder_indexes(Shops, status)
        return True
    return False


def _reorder_indexes(model, status: str):
    # Reorders the index field after deletion for consistency
    entries = model.select().where(model.status == status).order_by(model.date)
    for i, entry in enumerate(entries, start=1):
        entry.index = i
        entry.save()