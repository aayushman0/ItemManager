from datetime import date
from sqlalchemy import func
from db.models import session
from db.models import ServiceBill


def get_by_date(date: date) -> list[ServiceBill]:
    bills: list[ServiceBill] = session.query(ServiceBill).filter(func.DATE(ServiceBill.bill_date) == date, ServiceBill.is_enabled.is_(True)).order_by(ServiceBill.bill_date.desc())
    return bills


def get(id: int) -> ServiceBill | None:
    bill: ServiceBill | None = session.query(ServiceBill).filter(ServiceBill.id == id).scalar()
    if not bill:
        return None
    return bill


def create(customer_name: str, bill_string: str, total_amount: float, discount: float, net_amount: float) -> ServiceBill:
    bill = ServiceBill(customer_name, bill_string, total_amount, discount, net_amount)
    session.add(bill)
    session.commit()
    return bill


def delete(bill_no: str) -> ServiceBill | None:
    bill: ServiceBill | None = session.query(ServiceBill).filter(ServiceBill.id == bill_no).scalar()
    if not bill:
        return None
    bill.is_enabled = False
    session.commit()
    return bill
