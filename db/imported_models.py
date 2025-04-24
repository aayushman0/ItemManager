from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, String, Integer, Float, Date
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from datetime import date

BaseModel = declarative_base()
type_dict = {
        "tablet": "tab",
        "capsule": "cap",

        "syrup": "syp",
        "drops": "drp",

        "ointment": "ont",
        "cream": "crm",
        "gel": "gel",

        "powder": "pwd",
        "injection": "inj",
        "other": "oth"
    }


class Item(BaseModel):
    __tablename__ = "item"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String(64), index=True, nullable=False)
    type = Column("type", String(64), index=True, nullable=False)
    code = Column("code", String(64), index=True, unique=True)
    price = Column("price", Float)
    best_before = Column("best_before", Integer)

    def __init__(self, name: str, type: str, code: str, price: float, best_before: int):
        self.name = name
        self.type = type
        self.code = code
        self.price = price
        self.best_before = best_before

    def __repr__(self):
        return f"{type_dict.get(self.type.lower(), "oth").capitalize()}. {self.name}"


class Batch(BaseModel):
    __tablename__ = "batch"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    batch_no = Column("batch_no", String(100), index=True)
    quantity = Column("quantity", Integer)
    price = Column("price", Float)
    mfg_date = Column("mfg_date", Date)
    exp_date = Column("exp_date", Date, index=True)
    distributor = Column("distributor", String(64), index=True)
    item_id = Column(String(64), ForeignKey("item.id", ondelete="CASCADE"), nullable=False)
    item = relationship("Item", backref="batches")

    def __init__(self, item_id: int, batch_no: str, quantity: int, price: float, mfg_date: date, exp_date: date, distributor: str):
        self.batch_no = batch_no
        self.quantity = quantity
        self.price = price
        self.mfg_date = mfg_date
        self.exp_date = exp_date
        self.distributor = distributor
        self.item_id = item_id

    def __repr__(self):
        return f"{self.item.name} Batch: {self.batch_no}"


engine = create_engine("sqlite:///imported_database.db", echo=False)
BaseModel.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()


def yield_items():
    items = session.query(Item).all()
    for item in items:
        i_dict = {
            "name": item.name,
            "type": item.type,
            "price": item.price,
            "best_before": item.best_before,
            "min_unit": 1
        }
        batches = session.query(Batch).filter(Batch.item_id == item.id)
        b_list = [{
            "batch_no": batch.batch_no,
            "quantity": batch.quantity,
            "price": batch.price,
            "mfg_date": batch.mfg_date,
            "exp_date": batch.exp_date,
            "distributor": batch.distributor
        } for batch in batches]
        yield (i_dict, b_list)
