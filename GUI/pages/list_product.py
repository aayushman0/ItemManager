import tkinter as tk
from tkinter import ttk
from db.orm import product
from GUI import classes
from variables import PRODUCT_TYPES_LIST, ROW_COUNT


class Frame(classes.Frame):
    def __init__(self, master) -> None:
        super().__init__(master)
        self.columnconfigure(0, weight=1)
        self.table_columns = ["ID", "Name", "Type", "Price/Unit", "Best Before", "Shelf"]
        self.table_columns_width = [30, 500, 150, 150, 100, 70]
        self.table_columns_align = ["e", "w", "e", "e", "e", "e"]
        self.tk_vars()
        self.main()
        self.events()

    def tk_vars(self) -> None:
        self.product_name = tk.StringVar()
        self.product_type = tk.StringVar()
        self.product_shelf_id = tk.StringVar()

    def main(self) -> None:
        filter_frame = ttk.Frame(self)
        filter_frame.columnconfigure(1, weight=1)
        filter_frame.grid(row=0, sticky="ew")
        self.first_entry = self.string_entry(filter_frame, "Name: ", 1, 0, self.product_name)
        self.type_entry = self.choice_entry(filter_frame, "Type: ", 1, 2, self.product_type, ["All"]+PRODUCT_TYPES_LIST)
        self.last_entry = self.string_entry(filter_frame, "Shelf: ", 1, 4, self.product_shelf_id)

        table_frame = ttk.Frame(self)
        table_frame.columnconfigure(0, weight=1)
        table_frame.grid(row=1, sticky="ew")
        self.create_table(table_frame, 0, 0)

    def events(self) -> None:
        self.tab_sequencing()
        self.product_name.trace_add("write", self.filter_callback)
        self.product_type.trace_add("write", self.filter_callback)
        self.product_shelf_id.trace_add("write", self.filter_callback)

    def update_table(self) -> None:
        name = self.product_name.get()
        type = self.product_type.get()
        shelf = self.product_shelf_id.get()
        products, product_count = product.get_paginated(
            page=self.page_no,
            name=name,
            type=type,
            shelf=shelf
        )
        self.total_pages = product_count // ROW_COUNT + 1
        self.table.delete(*self.table.get_children())
        for row in products:
            self.table.insert(
                '', tk.END,
                values=[
                    row.id,
                    row.name,
                    row.type,
                    f"{row.price:.2f}/{row.min_unit:02d}",
                    row.best_before,
                    row.shelf
                ]
            )

    def filter_callback(self, *args) -> None:
        self.page_no = 1
        self.update_table()

    def refresh(self) -> None:
        self.product_name.set("")
        self.type_entry.current(0)
        self.product_shelf_id.set("")
        self.page_no = 1
        self.update_table()
        self.first_entry.focus_set()
