import re
from db.models import session
from db.models import Product
from variables import ROW_COUNT, PRODUCT_TYPES


class ProductAlreadyExists(Exception):
    pass


def get_by_id(id: int) -> Product | None:
    product: Product | None = session.query(Product).filter(Product.id == id).scalar()
    return product


def get_by_code(code: str) -> Product | None:
    product: Product | None = session.query(Product).filter(Product.code == code).scalar()
    return product


def get_paginated(page: int, name: str, type: str, shelf: str) -> tuple[list[Product], int]:
    products = session.query(Product)
    if name:
        products = products.filter(Product.name.icontains(name))
    if type != "All":
        products = products.filter(Product.type == type)
    if shelf:
        products = products.filter(Product.shelf.contains(shelf))
    count: int = products.count()
    paginated_products: list[Product] = products.slice((page - 1) * ROW_COUNT, page * ROW_COUNT)
    return paginated_products, count


def get_filtered(code: str) -> list[Product]:
    products: list[Product] = session.query(Product).filter(Product.code.icontains(code)).order_by(Product.name)
    return products


def create(name: str, type: str, price: float, min_unit: int, best_before: int, shelf: str) -> Product | ProductAlreadyExists:
    code: str = f"{PRODUCT_TYPES.get(type.lower(), 'oth')}{re.sub('[^A-Za-z0-9]+', '', name).lower()}"

    product: Product | None = session.query(Product).filter(Product.code == code).scalar()
    if product:
        raise ProductAlreadyExists
    product = Product(name, type, code, price, min_unit, best_before, shelf)
    session.add(product)
    session.commit()

    return product


def edit(id: str, name: str, type: str, price: float, min_unit: int, best_before: int, shelf: str) -> Product | None:
    product: Product | None = session.query(Product).filter(Product.id == id).scalar()
    if not product:
        return None

    product.name = name
    product.type = type
    product.code = f"{PRODUCT_TYPES.get(type.lower(), 'oth')}{re.sub('[^A-Za-z0-9]+', '', name).lower()}"
    product.price = price
    product.min_unit = min_unit
    product.best_before = best_before
    product.shelf = shelf
    session.commit()

    return product
