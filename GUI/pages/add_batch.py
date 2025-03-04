import tkinter as tk
from tkinter import ttk
from datetime import date, datetime
import re
from db.orm import product, batch
from GUI import classes


class Frame(classes.Frame):
    def __init__(self, master) -> None:
        super().__init__(master)
        self.columnconfigure(1, weight=1)
        self.best_before = 0
        self.tk_vars()
        self.main()
        self.events()

    def tk_vars(self) -> None:
        self.product_name = tk.StringVar()
        self.batch_no = tk.StringVar()
        self.price = tk.StringVar()
        self.min_unit = tk.StringVar()
        self.quantity = tk.StringVar()
        self.mfg_month = tk.IntVar()
        self.mfg_year = tk.IntVar()
        self.exp_month = tk.IntVar()
        self.exp_year = tk.IntVar()
        self.distributor = tk.StringVar()

    def main(self) -> None:
        self.first_entry = self.string_entry(self, "Name: ", self.i, 0, self.product_name)
        self.string_entry(self, "Batch No.: ", self.i, 0, self.batch_no)
        self.float_entry(self, "Price: ", self.i, 0, self.price)
        self.min_unit_entry = self.int_entry(self, "Min Unit: ", self.i, 0, self.min_unit)
        self.min_unit_entry.config(state="disabled")
        self.int_entry(self, "Quantity: ", self.i, 0, self.quantity)

        date_frame = ttk.Frame(self)
        date_frame.grid(row=self.i, column=0, columnspan=2, padx=self.PADX, pady=self.PADY, sticky="ew")
        self.date_entry(date_frame, "Mfg Date: ", 0, 0, self.mfg_month, self.mfg_year)
        self.date_entry(date_frame, "Exp Date: ", 1, 0, self.exp_month, self.exp_year)

        self.string_entry(self, "Distributor: ", self.i, 0, self.distributor)
        self.last_entry = self.create_button(self, "Add Batch", self.i, 1, 30, "#d0ffd0", self.add_batch)

    def events(self) -> None:
        self.tab_sequencing()

    def add_batch(self) -> None:
        product_name = self.product_name.get()
        batch_no = self.batch_no.get()
        price = self.price.get()
        if not (product_name and batch_no and price):
            print("Values missing!!!")
            return None
        p = product.get_by_code(code=re.sub('[^A-Za-z0-9]+', '', product_name).lower())
        if not p:
            print("Product doesn't exist!!!")
            return None
        quantity = self.quantity.get() or 0
        mfg_date = date(self.mfg_year.get(), self.mfg_month.get(), 1)
        exp_date = date(self.exp_year.get(), self.exp_month.get(), 1)
        distributor = self.distributor.get()
        b = batch.create(
            product_id=p.id,
            batch_no=batch_no,
            price=float(price),
            quantity=int(quantity),
            mfg_date=mfg_date,
            exp_date=exp_date,
            distributor=distributor
        )
        if not b:
            print("Error!!!")
            return None
        self.refresh()

    def refresh(self) -> None:
        self.product_name.set("")
        self.batch_no.set("")
        self.price.set("")
        self.min_unit.set("")
        self.quantity.set("")
        self.distributor.set("")
        today = datetime.now()
        self.mfg_year.set(today.year)
        self.mfg_month.set(today.month)
        self.exp_year.set(today.year)
        self.exp_month.set(today.month)
        self.first_entry.focus_set()
