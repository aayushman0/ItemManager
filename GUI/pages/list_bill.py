import tkinter as tk
from tkinter import ttk
from datetime import date, timedelta
from db.orm import product_bill
from GUI import classes
from variables import ENTRY_FONT


class Frame(classes.Frame):
    def __init__(self, master) -> None:
        super().__init__(master)
        self.columnconfigure(0, weight=1)
        self.table_columns = ["Bill No.", "Customer's Name", "Sum Total", "Discount", "Net Total", "Bill Date"]
        self.table_columns_width = [30, 400, 100, 100, 100, 70]
        self.table_columns_align = ["e", "w", "e", "e", "e", "e"]
        self.current_date = date.today()
        self.tk_vars()
        self.main()
        self.events()

    def tk_vars(self) -> None:
        self.current_total = tk.StringVar()

    def main(self) -> None:
        filter_frame = ttk.Frame(self)
        filter_frame.columnconfigure(1, weight=1)
        filter_frame.grid(row=0, sticky="ew")
        self.first_entry = tk.Button(
                filter_frame, text="<<", width=35, height=1, font=ENTRY_FONT, command=lambda: self.change_date(-1)
            )
        self.first_entry.grid(row=0, column=0, padx=self.PADX, sticky="w")
        self.date_label = tk.Label(filter_frame, text=self.current_date, justify='center', font=ENTRY_FONT)
        self.date_label.grid(row=0, column=1, padx=self.PADX)
        self.last_entry = tk.Button(
                filter_frame, text=">>", width=35, height=1, font=ENTRY_FONT, command=lambda: self.change_date(1)
            )
        self.last_entry.grid(row=0, column=2, padx=self.PADX, sticky="e")

        table_frame = ttk.Frame(self)
        table_frame.columnconfigure(0, weight=1)
        table_frame.grid(row=1, sticky="ew")
        self.create_table(table_frame, 0, 0)

    def events(self) -> None:
        self.tab_sequencing()
        self.table.bind("<Double-Button-1>", self.select_bill)

    def update_table(self) -> None:
        bills = product_bill.get_by_date(self.current_date)
        self.table.delete(*self.table.get_children())
        current_total = 0
        for bill in bills:
            self.table.insert(
                '', tk.END,
                values=[
                    bill.id,
                    bill.customer_name,
                    bill.total_amount,
                    bill.discount,
                    bill.net_amount,
                    bill.bill_date
                ]
            )
            current_total += bill.net_amount
        self.current_total.set(f"{current_total:.2f}")

    def change_date(self, delta: int) -> None:
        self.current_date += timedelta(days=delta)
        self.date_label["text"] = self.current_date
        self.update_table()

    def select_bill(self, *args):
        selected_bill = self.table.selection()
        if not selected_bill:
            print("No Bill Selected!!!")
            return None
        bill_id = self.table.item(selected_bill[0]).get("values", [None])[0]
        if bill_id is None:
            print("Bill ID not found!!!")
            return None
        bill = product_bill.get(bill_id)
        if not bill:
            print("Bill not found!!!")
            return None
        # Send bill to bill window

    def refresh(self) -> None:
        self.change_date(0)
        self.first_entry.focus_set()
