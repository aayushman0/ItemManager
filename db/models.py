from datetime import date, datetime
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, String, Integer, Float, Date, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, DeclarativeBase, relationship
from variables import PRODUCT_TYPES


BaseModel: DeclarativeBase = declarative_base()


class Product(BaseModel):
    __tablename__ = "product"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String(64), index=True, nullable=False)
    type = Column("type", String(64), index=True, nullable=False)
    code = Column("code", String(64), index=True, unique=True)
    price = Column("price", Float)
    min_unit = Column("min_unit", Integer)
    best_before = Column("best_before", Integer)
    shelf = Column("shelf", String(16), index=True)

    def __init__(self, name: str, type: str, code: str, price: float, min_unit: int, best_before: int, shelf: str):
        self.name = name
        self.type = type
        self.code = code
        self.price = price
        self.min_unit = min_unit
        self.best_before = best_before
        self.shelf = shelf

    def __repr__(self):
        return f"{PRODUCT_TYPES.get(self.type.lower(), "oth").capitalize()}. {self.name}"


class Batch(BaseModel):
    __tablename__ = "batch"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    batch_no = Column("batch_no", String(100), index=True)
    quantity = Column("quantity", Integer)
    price = Column("price", Float)
    mfg_date = Column("mfg_date", Date)
    exp_date = Column("exp_date", Date, index=True)
    distributor = Column("distributor", String(64), index=True)
    created_at = Column("created_at", DateTime)

    product_id = Column(Integer, ForeignKey("product.id", ondelete="CASCADE"), nullable=False)
    product = relationship("Product", backref="batches")

    def __init__(self, product_id: int, batch_no: str, quantity: int, price: float, mfg_date: date, exp_date: date, distributor: str):
        self.batch_no = batch_no
        self.quantity = quantity
        self.price = price
        self.mfg_date = mfg_date
        self.exp_date = exp_date
        self.distributor = distributor
        self.product_id = product_id
        self.created_at = datetime.now()

    def __repr__(self):
        return f"{self.product.name} Batch: {self.batch_no}"


class ProductBill(BaseModel):
    __tablename__ = "product_bill"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    customer_name = Column("name", String(64))
    bill = Column("bill", String)
    total_amount = Column("total_amount", Float)
    discount = Column("discount", Float)
    net_amount = Column("net_amount", Float)
    bill_date = Column("bill_date", DateTime, index=True)

    def __init__(self, customer_name: str, bill: str, total_amount: float, discount: float, net_amount: float):
        self.customer_name = customer_name
        self.bill = bill
        self.total_amount = total_amount
        self.discount = discount
        self.net_amount = net_amount
        self.bill_date = datetime.now()

    def __repr__(self):
        return f"{self.id}. {self.customer_name}"


engine = create_engine("sqlite:///database.db", echo=False)
BaseModel.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()
