import tkinter as tk
from tkinter import ttk
from datetime import date, datetime
import re
from db.orm import product, batch
from GUI.pages import add_batch
from variables import PRODUCT_TYPES


class Frame(add_batch.Frame):
    def __init__(self, master) -> None:
        super().__init__(master)
        self.batch_id = tk.StringVar()

    def main(self) -> None:
        self.first_entry = self.choice_entry(self, "Name: ", self.i, 0, self.product_name, [], False)
        self.string_entry(self, "Batch No.: ", self.i, 0, self.batch_no)
        self.float_entry(self, "Price: ", self.i, 0, self.price)
        self.int_entry(self, "Min Unit: ", self.i, 0, self.min_unit).config(state="disabled")
        self.int_entry(self, "Quantity: ", self.i, 0, self.quantity)

        date_frame = ttk.Frame(self)
        date_frame.grid(row=self.i, column=0, columnspan=2, padx=self.PADX, pady=self.PADY, sticky="ew")
        self.date_entry(date_frame, "Mfg Date: ", 0, 0, self.mfg_month, self.mfg_year)
        self.date_entry(date_frame, "Exp Date: ", 1, 0, self.exp_month, self.exp_year)

        self.string_entry(self, "Distributor: ", self.i, 0, self.distributor)
        self.last_entry = self.create_button(self, "Edit Batch", self.i, 1, 30, "#d0ffd0", self.edit_batch)

    def events(self) -> None:
        self.tab_sequencing()
        self.product_name.trace_add("write", self.get_filtered_names)
        self.first_entry.bind("<<ComboboxSelected>>", self.select_name)
        self.first_entry.bind("<Return>", self.select_name)
        self.first_entry.bind("<Tab>", self.select_name)
        self.mfg_month.trace_add("write", self.update_date)
        self.mfg_year.trace_add("write", self.update_date)

    def edit_batch(self) -> None:
        if not self.batch_id.get():
            return None
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
        b = batch.edit(
            batch_id=self.batch_id.get(),
            product_id=p.id,
            batch_no=batch_no,
            price=price,
            quantity=quantity,
            mfg_date=mfg_date,
            exp_date=exp_date,
            distributor=distributor
        )
        if not b:
            print("Error!!!")
            return None
        self.refresh()

    def refresh(self) -> None:
        self.first_entry["values"] = []
        b = batch.get(batch_id=self.batch_id.get())
        if b:
            p = b.product
            self.product_name.set(f"{PRODUCT_TYPES.get(p.type.lower(), 'oth').capitalize()}. {p.name}")
            self.batch_no.set(b.batch_no)
            self.price.set(b.price)
            self.min_unit.set(p.min_unit)
            self.quantity.set(b.quantity)
            self.distributor.set(b.distributor)
            self.mfg_year.set(b.mfg_date.year)
            self.mfg_month.set(b.mfg_date.month)
            self.exp_year.set(b.exp_date.year)
            self.exp_month.set(b.exp_date.month)
        else:
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
