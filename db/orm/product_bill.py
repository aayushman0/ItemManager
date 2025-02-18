from sqlalchemy import func
from db.models import session
from db.models import Batch, ProductBill

from datetime import date


def get_by_date(date: date) -> list[ProductBill]:
    bills: list[ProductBill] = session.query(ProductBill).filter(func.DATE(ProductBill.bill_date) == date).order_by(ProductBill.bill_date.desc())
    return bills


def get(id: int) -> tuple[ProductBill, list[tuple[Batch, int]]] | None:
    bill: ProductBill | None = session.query(ProductBill).filter(ProductBill.id == id).scalar()
    if not bill:
        return None
    
    return bill, get_batch_list(bill.bill)


def get_batch_list(bill_string: str) -> list[tuple[Batch, int]]:
    batch_and_qty = [row.split(".") for row in bill_string.split(",")]
    return [
        (session.query(Batch).filter(Batch.id == batch_id).scalar(), qty)
        for batch_id, qty in batch_and_qty
    ]


def create(customer_name: str, bill_string: str, total_amount: float, discount: float, net_amount: float) -> ProductBill:
    bill = ProductBill(customer_name, bill_string, total_amount, discount, net_amount)
    session.add(bill)

    for batch, qty in get_batch_list(bill_string):
        if not batch:
            continue
        batch.quantity -= qty
    session.commit()

    return bill
