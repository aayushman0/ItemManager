from datetime import date
from sqlalchemy import func
from db.models import session
from db.models import Batch, ProductBill


def get_by_date(date: date) -> list[ProductBill]:
    bills: list[ProductBill] = session.query(ProductBill).filter(func.DATE(ProductBill.bill_date) == date, ProductBill.is_enabled.is_(True)).order_by(ProductBill.bill_date.desc())
    return bills


def get(id: int) -> tuple[ProductBill, list[tuple[Batch, int, float]]] | tuple[None, None]:
    bill: ProductBill | None = session.query(ProductBill).filter(ProductBill.id == id).scalar()
    if not bill:
        return None, None

    return bill, get_batch_list(bill.bill)


def get_batch_list(bill_string: str) -> list[tuple[Batch, int, float]]:
    batch_qty_total = [row.split(":") for row in bill_string.split(",")]
    return [
        (session.query(Batch).filter(Batch.id == batch_id).scalar(), int(qty or 0), float(total or 0))
        for batch_id, qty, total in batch_qty_total
    ]


def create(customer_name: str, bill_string: str, total_amount: float, discount: float, net_amount: float) -> ProductBill:
    bill = ProductBill(customer_name, bill_string, total_amount, discount, net_amount)
    session.add(bill)

    for batch, qty, _ in get_batch_list(bill_string):
        if not batch:
            continue
        batch.quantity -= qty
    session.commit()

    return bill


def delete(bill_no: str) -> ProductBill | None:
    bill: ProductBill | None = session.query(ProductBill).filter(ProductBill.id == bill_no).scalar()
    if not bill:
        return None

    for batch, qty, _ in get_batch_list(bill.bill):
        if not batch:
            continue
        batch.quantity += qty
    bill.is_enabled = False
    session.commit()

    return bill
