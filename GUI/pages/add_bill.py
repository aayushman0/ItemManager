import tkinter as tk
from tkinter import ttk
import re
from db.models import Batch
from db.orm import product, batch, product_bill
from GUI import classes
from variables import ENTRY_FONT, PRODUCT_TYPES, BILL_ROW_COUNT


class Frame(classes.Frame):
    def __init__(self, master) -> None:
        super().__init__(master)
        self.columnconfigure(0, weight=1)
        self.table_columns = ["Name", "Batch No.", "Exp Date", "Price/Unit", "Quantity", "Total"]
        self.table_columns_width = [300, 200, 100, 150, 100, 100]
        self.table_columns_align = ["w", "w", "e", "e", "e", "e"]
        self.current_batch: Batch | None = None
        self.price: float = 0.0
        self.bill_list = list()
        self.tk_vars()
        self.main()
        self.events()

    def tk_vars(self) -> None:
        self.customer_name = tk.StringVar()
        self.product_name = tk.StringVar()
        self.batch_no = tk.StringVar()
        self.price_per_unit = tk.StringVar()
        self.quantity = tk.StringVar()
        self.item_total = tk.StringVar()
        self.sum_total = tk.StringVar()
        self.discount = tk.StringVar()
        self.net_total = tk.StringVar()

    def main(self) -> None:
        entry_frame = ttk.Frame(self)
        entry_frame.columnconfigure(1, weight=1)
        entry_frame.grid(row=0, sticky="ew")
        self.first_entry = self.string_entry(entry_frame, "Customer's Name: ", 0, 0, self.customer_name, 5)
        self.product_entry = self.choice_entry(entry_frame, "Product Name: ", 1, 0, self.product_name, [], False)
        self.string_entry(entry_frame, "Price/Unit: ", 1, 2, self.price_per_unit).config(state="disabled")
        self.float_entry(entry_frame, "Total: ", 1, 4, self.item_total).config(state="disabled")
        self.batch_no_entry = self.choice_entry(entry_frame, "Batch No.: ", 2, 0, self.batch_no, [])
        self.int_entry(entry_frame, "Quantity: ", 2, 2, self.quantity)
        tk.Button(
                entry_frame, text="Add to Bill", width=20, height=1, font=ENTRY_FONT, bg="#ababdf", command=self.add_to_bill
            ).grid(
                row=2, column=5, padx=self.PADX, sticky="w"
        )

        table_frame = ttk.Frame(self)
        table_frame.columnconfigure(0, weight=1)
        table_frame.grid(row=1, sticky="ew")
        self.create_table(table_frame, 0, 0)
        self.table.config(height=BILL_ROW_COUNT)

        bottom_frame = ttk.Frame(self)
        bottom_frame.columnconfigure(4, weight=1)
        bottom_frame.grid(row=2, sticky="ew")
        self.float_entry(bottom_frame, "Sum Total: ", 0, 0, self.sum_total).config(state="disabled")
        self.float_entry(bottom_frame, "Discount: ", 0, 2, self.discount)
        self.float_entry(bottom_frame, "Net Total: ", 1, 0, self.net_total).config(state="disabled")
        self.last_entry = self.create_button(bottom_frame, "Save Bill", 0, 4, 30, "#d0ffd0", self.add_bill)
        self.last_entry.grid_configure(rowspan=2)

    def events(self) -> None:
        self.tab_sequencing()
        self.product_name.trace_add("write", self.get_filtered_names)
        self.product_entry.bind("<<ComboboxSelected>>", self.select_name)
        self.product_entry.bind("<Return>", self.select_name)
        self.product_entry.bind("<Tab>", self.select_name)
        self.batch_no.trace_add("write", self.update_price)
        self.price_per_unit.trace_add("write", self.calculate_item_total)
        self.quantity.trace_add("write", self.calculate_item_total)
        self.discount.trace_add("write", self.calculate_net_total)
        self.table.bind("<Double-Button-1>", self.remove_from_bill)

    def add_to_bill(self) -> None:
        product_name = self.product_name.get()
        batch_no = self.batch_no.get()
        quantity = int(self.quantity.get() or 0)
        if not (product_name and batch_no and quantity):
            print("Values Missing!!!")
            return None
        exp_date = f"{self.current_batch.exp_date.month:02d} / {self.current_batch.exp_date.year}"
        price_per_unit = self.price_per_unit.get()
        item_total = float(self.item_total.get() or 0)
        self.table.insert('', tk.END, values=(product_name, batch_no, exp_date, price_per_unit, quantity, item_total))
        sum_total = float(self.sum_total.get() or 0)
        self.sum_total.set(sum_total + item_total)
        self.bill_list.append(f"{self.current_batch.id}:{quantity}:{item_total}")
        self.refresh_entry()
        self.calculate_net_total()
        self.product_entry.focus_set()

    def add_bill(self) -> None:
        if not self.bill_list:
            print("Bill is Empty!!!")
            return None
        bill_string = ",".join(self.bill_list)
        customer_name = self.customer_name.get()
        total_amount = float(self.sum_total.get() or 0)
        discount = float(self.discount.get() or 0)
        net_amount = float(self.net_total.get() or 0)
        product_bill.create(
            customer_name=customer_name,
            bill_string=bill_string,
            total_amount=total_amount,
            discount=discount,
            net_amount=net_amount
        )
        self.refresh()

    def get_filtered_names(self, *args) -> None:
        name = re.sub('[^A-Za-z0-9]+', '', self.product_name.get()).lower()
        if len(name) < 3:
            return None
        products = product.get_filtered(name)
        names = [f"{PRODUCT_TYPES.get(p.type.lower(), 'oth').capitalize()}. {p.name}" for p in products]
        self.product_entry["values"] = names

    def select_name(self, *args) -> None:
        if not self.product_entry["values"]:
            self.product_entry.delete(0, tk.END)
            return None
        self.product_entry.current(0)
        name = re.sub('[^A-Za-z0-9]+', '', self.product_name.get()).lower()
        batches = batch.get_from_product(name)
        self.batch_no_entry["values"] = [b.batch_no for b in batches]
        if not batches:
            self.batch_no.set("")
            return None
        self.batch_no_entry.current(0)

    def update_price(self, *args) -> None:
        product_name = re.sub('[^A-Za-z0-9]+', '', self.product_name.get()).lower()
        batch_no = self.batch_no.get()
        if not (product_name and batch_no):
            return None
        self.current_batch = batch.get(product_name, batch_no)
        if not self.current_batch:
            return None
        self.price = self.current_batch.price
        self.price_per_unit.set(f"{self.current_batch.price:.2f}/{self.current_batch.product.min_unit:02d}")

    def calculate_item_total(self, *args) -> None:
        quantity = int(self.quantity.get() or 0)
        total = quantity * self.price
        self.item_total.set(f"{total:.2f}")

    def calculate_net_total(self, *args) -> None:
        sum_total = float(self.sum_total.get() or 0)
        discount = float(self.discount.get() or 0)
        total = max(sum_total - discount, 0)
        self.net_total.set(f"{total:.2f}")

    def remove_from_bill(self, *args) -> None:
        cur_item = self.table.focus()
        if not cur_item:
            print("No Item Selected!!!")
            return None
        i = self.table.index(cur_item)
        self.table.delete(cur_item)
        removed_item: str = self.bill_list.pop(i)
        item_total = float(removed_item.split(":")[2] or 0)
        sum_total = float(self.sum_total.get() or 0)
        self.sum_total.set(sum_total - item_total)
        self.calculate_net_total()

    def refresh_entry(self) -> None:
        self.product_entry["values"] = []
        self.product_name.set("")
        self.batch_no_entry["values"] = []
        self.batch_no.set("")
        self.current_batch = None
        self.price_per_unit.set("")
        self.price = 0.0
        self.quantity.set("")
        self.item_total.set("")

    def refresh(self) -> None:
        self.customer_name.set("")
        self.refresh_entry()
        self.bill_list = []
        self.table.delete(*self.table.get_children())
        self.sum_total.set("")
        self.discount.set("")
        self.net_total.set("")
        self.first_entry.focus_set()
