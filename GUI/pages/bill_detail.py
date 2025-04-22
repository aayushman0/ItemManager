import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askyesno
from db.orm import product_bill
from GUI import classes
from variables import BILL_ROW_COUNT


class Frame(classes.Frame):
    def __init__(self, master) -> None:
        super().__init__(master)
        self.columnconfigure(0, weight=1)
        self.table_columns = ["Name", "Batch No.", "Exp Date", "Price/Unit", "Quantity", "Total"]
        self.table_columns_width = [300, 200, 100, 150, 100, 100]
        self.table_columns_align = ["w", "w", "e", "e", "e", "e"]
        self.tk_vars()
        self.main()
        self.events()

    def tk_vars(self) -> None:
        self.bill_no = tk.StringVar()
        self.bill_date = tk.StringVar()
        self.customer_name = tk.StringVar()
        self.sum_total = tk.StringVar()
        self.discount = tk.StringVar()
        self.net_total = tk.StringVar()

    def main(self) -> None:
        entry_frame = ttk.Frame(self)
        entry_frame.columnconfigure(1, weight=1)
        entry_frame.grid(row=0, sticky="ew")
        self.string_entry(entry_frame, "Bill No.: ", 0, 0, self.bill_no).config(state="disabled")
        self.string_entry(entry_frame, "Bill Date: ", 0, 4, self.bill_date).config(state="disabled")
        self.string_entry(entry_frame, "Customer's Name: ", 1, 0, self.customer_name, 5).config(state="disabled")
        self.string_entry(entry_frame, "Sum Total: ", 2, 0, self.sum_total).config(state="disabled")
        self.string_entry(entry_frame, "Discount: ", 2, 2, self.discount).config(state="disabled")
        self.string_entry(entry_frame, "Net Total: ", 2, 4, self.net_total).config(state="disabled")

        table_frame = ttk.Frame(self)
        table_frame.columnconfigure(0, weight=1)
        table_frame.grid(row=1, sticky="ew")
        self.create_table(table_frame, 0, 0)
        self.table.config(height=BILL_ROW_COUNT)

        edit_frame = ttk.Frame(self)
        edit_frame.grid(row=2, sticky="e")
        self.create_button(edit_frame, "Delete Bill", 0, 0, 30, "#ffd0d0", self.delete_bill)

    def events(self) -> None:
        pass

    def delete_bill(self) -> None:
        bill_no = self.bill_no.get()
        if not bill_no:
            return None
        confirmation = askyesno(title="Delete Bill", message=f"Delete Bill no. {bill_no}?")
        if not confirmation:
            return None
        b = product_bill.delete(bill_no)
        if not b:
            return None
        if b.is_enabled:
            print("Bill not deleted!!!")
            return None

    def refresh(self) -> None:
        bill_no = self.bill_no.get()
        if not bill_no:
            return None
        bill, batches_and_qty = product_bill.get(bill_no)
        if not bill:
            print("Bill not found!!!")
            return None
        self.bill_date.set(bill.bill_date)
        self.customer_name.set(bill.customer_name)
        self.sum_total.set(bill.total_amount)
        self.discount.set(bill.discount)
        self.net_total.set(bill.net_amount)
        self.table.delete(*self.table.get_children())
        for b, qty, total in batches_and_qty:
            self.table.insert(
                '', tk.END,
                values=(
                    b.product.name,
                    b.batch_no,
                    b.exp_date,
                    f"{b.price:.2f}/{b.product.min_unit:02d}",
                    qty,
                    total
                )
            )
