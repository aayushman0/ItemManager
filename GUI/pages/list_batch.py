import tkinter as tk
from tkinter import ttk
import re
from db.orm import batch
from GUI import classes
from variables import ROW_COUNT, PRODUCT_TYPES


class Frame(classes.Frame):
    def __init__(self, master) -> None:
        super().__init__(master)
        self.columnconfigure(0, weight=1)
        self.table_columns = ["Name", "Batch No.", "Price/Unit", "Quantity", "Exp Date", "Shelf", "Distributor"]
        self.table_columns_width = [400, 200, 150, 100, 100, 70, 150]
        self.table_columns_align = ["w", "w", "e", "e", "e", "e", "e"]
        self.tk_vars()
        self.main()
        self.events()

    def tk_vars(self) -> None:
        self.product_name = tk.StringVar()
        self.distributor = tk.StringVar()
        self.shelf_id = tk.StringVar()

    def main(self) -> None:
        filter_frame = ttk.Frame(self)
        filter_frame.columnconfigure(1, weight=1)
        filter_frame.grid(row=0, sticky="ew")
        self.first_entry = self.string_entry(filter_frame, "Name: ", 1, 0, self.product_name)
        self.string_entry(filter_frame, "Shelf: ", 1, 2, self.shelf_id)
        self.last_entry = self.string_entry(filter_frame, "Distributor: ", 1, 4, self.distributor)

        table_frame = ttk.Frame(self)
        table_frame.columnconfigure(0, weight=1)
        table_frame.grid(row=1, sticky="ew")
        self.create_table(table_frame, 0, 0)

    def events(self) -> None:
        self.tab_sequencing()
        self.product_name.trace_add("write", self.filter_callback)
        self.shelf_id.trace_add("write", self.filter_callback)
        self.distributor.trace_add("write", self.filter_callback)

    def update_table(self) -> None:
        name = re.sub('[^A-Za-z0-9]+', '', self.product_name.get()).lower()
        shelf = self.shelf_id.get()
        distributor = self.distributor.get()
        batches, batch_count = batch.get_paginated(
            page=self.page_no,
            name=name,
            shelf=shelf,
            distributor=distributor
        )
        self.total_pages = batch_count // ROW_COUNT + 1
        self.table.delete(*self.table.get_children())
        for row in batches:
            self.table.insert(
                '', tk.END,
                values=[
                    f"{PRODUCT_TYPES.get(row.product.type.lower(), 'oth').capitalize()}. {row.product.name}",
                    row.batch_no,
                    f"{row.price:.2f}/{row.product.min_unit:02d}",
                    row.quantity,
                    f"{row.exp_date.month:02d} / {row.exp_date.year}",
                    row.product.shelf,
                    row.distributor
                ]
            )

    def filter_callback(self, *args) -> None:
        self.page_no = 1
        self.update_table()

    def refresh(self) -> None:
        self.product_name.set("")
        self.shelf_id.set("")
        self.distributor.set("")
        self.page_no = 1
        self.update_table()
        self.first_entry.focus_set()
