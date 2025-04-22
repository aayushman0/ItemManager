import tkinter as tk
from tkinter import ttk
from db.orm import batch
from GUI import classes
from GUI.pages import product_detail, batch_detail, bill_detail
from variables import env, HEADER_FONT, SUBHEADER_FONT, ENTRY_FONT


class Frame(classes.Frame):
    def __init__(self, master, productDetail: product_detail.Frame, batchDetail: batch_detail.Frame, billDetail: bill_detail.Frame) -> None:
        super().__init__(master)
        self.columnconfigure(0, weight=1)
        self.productDetail = productDetail
        self.batchDetail = batchDetail
        self.billDetail = billDetail
        self.tk_vars()
        self.main()
        self.events()

    def tk_vars(self) -> None:
        self.item_id = tk.StringVar()
        self.batch_id = tk.StringVar()
        self.bill_id = tk.StringVar()
        self.grand_total = tk.StringVar()

    def main(self) -> None:
        top_frame = ttk.Frame(self)
        top_frame.columnconfigure(0, weight=1)
        top_frame.grid(row=0, padx=self.PADX, pady=self.PADY, sticky="ew")
        tk.Label(
                top_frame, text=env.get("COMPANY_NAME", "COMPANY NAME"), justify="center", font=HEADER_FONT
            ).grid(
                row=0, column=0, sticky="ew", columnspan=2
        )
        tk.Label(
                top_frame, text=env.get("COMPANY_ADDRESS", "Address"), justify="center", font=SUBHEADER_FONT
            ).grid(
                row=1, column=0, sticky="ew", columnspan=2
        )
        tk.Label(
                top_frame, text=f"PAN No.: {env.get('PAN_NO', 'XXXXXXXXX')}", justify="left", font=ENTRY_FONT
            ).grid(
                row=2, column=0, sticky="w"
        )
        tk.Label(
                top_frame, text=f"DDA No.: {env.get('DDA_NO', 'XXXXXXXXX/XXX')}", justify="left", font=ENTRY_FONT
            ).grid(
                row=2, column=1, sticky="e"
        )

        entry_frame = ttk.Frame(self)
        entry_frame.columnconfigure(1, weight=1)
        entry_frame.grid(row=1, padx=self.PADX, pady=self.PADY, sticky="ew")
        self.first_entry = self.int_entry(entry_frame, "Item ID: ", 0, 0, self.item_id)
        self.batch_entry = self.int_entry(entry_frame, "Batch ID: ", 1, 0, self.batch_id)
        self.last_entry = self.int_entry(entry_frame, "Bill ID: ", 2, 0, self.bill_id)

        bottom_frame = ttk.Frame(self)
        bottom_frame.columnconfigure(1, weight=1)
        bottom_frame.grid(row=2, padx=self.PADX, pady=self.PADY, sticky="ew")
        grand_total_frame = self.float_entry(bottom_frame, "Total of All Products: ", 0, 0, self.grand_total)
        grand_total_frame.config(state="disabled")

    def events(self) -> None:
        self.tab_sequencing()
        self.first_entry.bind("<Return>", self.change_to_product)
        self.batch_entry.bind("<Return>", self.change_to_batch)
        self.last_entry.bind("<Return>", self.change_to_bill)

    def change_to_product(self, *args) -> None:
        item_id = self.item_id.get()
        if not item_id:
            return None
        self.productDetail.product_id.set(item_id)
        self.productDetail.set_active()

    def change_to_batch(self, *args) -> None:
        batch_id = self.batch_id.get()
        if not batch_id:
            return None
        self.batchDetail.batch_id.set(batch_id)
        self.batchDetail.set_active()

    def change_to_bill(self, *args) -> None:
        bill_no = self.bill_id.get()
        if not bill_no:
            return None
        self.billDetail.bill_no.set(bill_no)
        self.billDetail.set_active()

    def refresh(self) -> None:
        self.item_id.set("")
        self.batch_id.set("")
        self.bill_id.set("")
        self.grand_total.set(batch.get_total_amount())
        self.first_entry.focus_set()
