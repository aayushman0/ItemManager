import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, datetime
import re
from db.orm import product, batch
from GUI import classes
from variables import PRODUCT_TYPES


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
        self.last_entry = self.create_button(self, "Add Batch", self.i, 1, 30, "#d0ffd0", self.add_batch)

    def events(self) -> None:
        self.tab_sequencing()
        self.product_name.trace_add("write", self.get_filtered_names)
        self.first_entry.bind("<<ComboboxSelected>>", self.select_name)
        self.first_entry.bind("<Return>", self.select_name)
        self.first_entry.bind("<Tab>", self.select_name)
        self.mfg_month.trace_add("write", self.update_date)
        self.mfg_year.trace_add("write", self.update_date)

    def add_batch(self) -> None:
        product_name = self.product_name.get()
        batch_no = self.batch_no.get()
        price = self.price.get()
        if not (product_name and batch_no and price):
            messagebox.showwarning("Missing Values", "Values are missing!")
            return None
        p = product.get_by_code(code=re.sub('[^A-Za-z0-9]+', '', product_name).lower())
        if not p:
            messagebox.showwarning("Missing Product", "Product doesn't exist!")
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
            messagebox.showwarning("WARNING", "Batch cannot be created!")
            return None
        self.refresh()

    def get_filtered_names(self, *args) -> None:
        name = re.sub('[^A-Za-z0-9]+', '', self.product_name.get()).lower()
        if len(name) < 3:
            return None
        products = product.get_filtered(name)
        names = [f"{PRODUCT_TYPES.get(p.type.lower(), 'oth').capitalize()}. {p.name}" for p in products]
        self.first_entry["values"] = names

    def select_name(self, *args) -> None:
        if not self.first_entry["values"]:
            self.first_entry.delete(0, tk.END)
            return None
        self.first_entry.current(0)
        name = re.sub('[^A-Za-z0-9]+', '', self.product_name.get()).lower()
        p = product.get_by_code(name)
        self.price.set(p.price)
        self.min_unit.set(p.min_unit)
        self.best_before = p.best_before
        self.update_date()

    def update_date(self, *args) -> None:
        mfg_month = self.mfg_month.get()
        mfg_year = self.mfg_year.get()
        if not (mfg_month and mfg_year):
            return None
        self.exp_month.set(((mfg_month + self.best_before) % 12) or 12)
        self.exp_year.set(mfg_year + (mfg_month + self.best_before - 1) // 12)

    def refresh(self) -> None:
        self.first_entry["values"] = []
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
