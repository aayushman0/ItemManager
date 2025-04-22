from datetime import date
from db.models import session
from db.models import Product, Batch
from variables import ROW_COUNT


def get(code: str | None = None, batch_no: str | None = None, batch_id: str | None = None) -> Batch | None:
    if batch_id:
        batch = session.query(Batch).filter(Batch.id == batch_id).scalar()
        return batch
    if not (code and batch_no):
        return None
    product: Product | None = session.query(Product).filter(Product.code == code).scalar()
    if not product:
        return None
    batch: Batch | None = session.query(Batch).filter(Batch.product_id == product.id, Batch.batch_no == batch_no, Batch.quantity > 0).first()
    return batch


def get_from_product(code: int) -> list[Batch]:
    batches: list[Batch] = session.query(Batch).join(Product).filter(Product.code == code, Batch.quantity > 0).order_by(Batch.exp_date).all()
    return batches


def get_paginated(page: int, name: str, shelf: str, distributor: str) -> tuple[list[Batch], int]:
    batches = session.query(Batch).join(Product)
    if name:
        batches = batches.filter(Product.code.icontains(name))
    if shelf:
        batches = batches.filter(Product.shelf.icontains(shelf))
    if distributor:
        batches = batches.filter(Batch.distributor.icontains(distributor))
    batches = batches.order_by(Batch.exp_date)
    count: int = batches.count()
    paginated_batches: list[Batch] = batches.slice((page-1) * ROW_COUNT, page * ROW_COUNT)
    return paginated_batches, count


def get_total_amount() -> float:
    batches = session.query(Batch).filter(Batch.quantity > 0)
    total = sum(batch.quantity * batch.price for batch in batches)
    return total


def create(product_id: str, batch_no: str, price: float, quantity: int, mfg_date: date, exp_date: date, distributor: str) -> Batch | None:
    product: Product | None = session.query(Product).filter(Product.id == product_id).scalar()
    if not product:
        return None
    product.price = price

    batch: Batch | None = session.query(Batch).filter(Batch.product_id == product_id, Batch.batch_no == batch_no).scalar()
    if not batch:
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


def edit(batch_id: str, product_id: str, batch_no: str, price: float, quantity: int, mfg_date: date, exp_date: date, distributor: str) -> Batch | None:
    batch: Batch | None = session.query(Batch).filter(Batch.id == batch_id).scalar()
    if not batch:
        return None
    batch.product_id = product_id
    batch.batch_no = batch_no
    batch.price = price
    batch.quantity = quantity
    batch.mfg_date = mfg_date
    batch.exp_date = exp_date
    batch.distributor = distributor
    session.commit()

    return batch
