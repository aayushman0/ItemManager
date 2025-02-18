from db.models import session
from db.models import Product
from variables import row_count, product_types

import re


class ProductAlreadyExists(Exception):
    pass


def get_by_id(id: int) -> Product | None:
    product: Product | None = session.query(Product).filter(Product.id == id).scalar()
    return product


def get_by_code(code: str) -> Product | None:
    product: Product | None = session.query(Product).filter(Product.code == code).scalar()
    return product


def get_paginated(page: int) -> tuple[list[Product], int]:
    products: list[Product] = session.query(Product)
    count: int = products.count()
    paginated_products: list[Product] = products.slice((page - 1) * row_count, page * row_count)
    return paginated_products, count


def get_filtered(code: str) -> list[Product]:
    products: list[Product] = session.query(Product).filter(Product.code.icontains(code)).order_by(Product.name)
    return products


def create(name: str, type: str, price: float, min_unit: int, best_before: int) -> Product | ProductAlreadyExists:
    code: str = f"{product_types.get(type.lower(), 'oth')}{re.sub('[^A-Za-z0-9]+', '', name).lower()}"

    product: Product | None = session.query(Product).filter(Product.code == code).scalar()
    if product:
        return ProductAlreadyExists
    product = Product(name, type, code, price, min_unit, best_before)
    session.add(product)
    session.commit()

    return product


def edit(code: str, name: str, type: str, price: float, min_unit: int, best_before: int) -> Product | None:
    product: Product | None = session.query(Product).filter(Product.code == code).scalar()
    if not product:
        return None

    product.name = name
    product.type = type
    product.code = f"{product_types.get(type.lower(), 'oth')}{re.sub('[^A-Za-z0-9]+', '', name).lower()}"
    product.price = price
    product.min_unit = min_unit
    product.best_before = best_before
    session.commit()

    return product
