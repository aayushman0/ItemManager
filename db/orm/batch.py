from db.models import session
from db.models import Product, Batch
from variables import row_count

from datetime import date


def get(code: str, batch_no: str) -> Batch | None:
    product: Product | None = session.query(Product).filter(Product.code == code).scalar()
    if not product:
        return None
    batch: Batch | None = session.query(Batch).filter(Batch.product_id == product.id, Batch.batch_no == batch_no, Batch.quantity > 0).first()
    return batch


def get_from_product(product_id: int) -> list[Batch]:
    batches: list[Batch] = session.query(Batch).filter(Batch.product_id == product_id).all()
    return batches


def get_paginated(page: int, code: str | None = None) -> tuple[list[Batch], int]:
    batches: list[Batch] = session.query(Batch)
    if code:
        batches = batches.join(Product).filter(Product.code.icontains(code))
    batches = batches.order_by(Batch.exp_date)

    count: int = batches.count()
    paginated_batches: list[Batch] = batches.slice((page-1) * row_count, page * row_count)
    return paginated_batches, count


def create(product_id: str, batch_no: str, price: float, quantity: int, mfg_date: date, exp_date: date, distributor: str) -> Batch | None:
    product: Product | None = session.query(Product).filter(Product.id == product_id).scalar()
    if not product:
        return None
    product.price = price

    batch: Batch | None = session.query(Batch).filter(Batch.product_id == product_id, Batch.batch_no == batch_no).scalar()
    if not Batch:
        batch = Batch(product_id, batch_no, quantity, price, mfg_date, exp_date, distributor)
    else:
        batch.quantity += quantity
        batch.price = price
        batch.mfg_date = mfg_date
        batch.exp_date = exp_date
        batch.distributor = distributor
    session.add(batch)
    session.commit()

    return batch


def edit(code: str, batch_no: str, price: float, quantity: int, mfg_date: date, exp_date: date, distributor: str) -> Batch | None:
    batch = session.query(Batch).join(Product).filter(Product.code == code, Batch.batch_no == batch_no).first()
    if not batch:
        return None

    batch.price = price
    batch.quantity = quantity
    batch.mfg_date = mfg_date
    batch.exp_date = exp_date
    batch.distributor = distributor
    session.commit()

    return batch
