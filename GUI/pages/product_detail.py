import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from db.orm import product, batch
from GUI import classes
from GUI.pages import batch_detail
from variables import PRODUCT_TYPES_LIST, ENTRY_FONT


class Frame(classes.Frame):
    def __init__(self, master, batchDetail: batch_detail.Frame) -> None:
        super().__init__(master)
        self.columnconfigure(1, weight=1)
        self.batchDetail = batchDetail
        self.table_columns = ["ID", "Batch No.", "Mfg Date", "Exp Date", "Price", "Quantity", "Distributor"]
        self.table_columns_width = [20, 200, 100, 100, 150, 100, 150]
        self.table_columns_align = ["e", "w", "e", "e", "e", "e", "e"]
        self.tk_vars()
        self.main()
        self.events()

    def tk_vars(self) -> None:
        self.product_name = tk.StringVar()
        self.product_type = tk.StringVar()
        self.product_price = tk.StringVar()
        self.product_min_unit = tk.StringVar()
        self.product_best_before = tk.StringVar()
        self.product_shelf_id = tk.StringVar()
        self.product_id = tk.StringVar()

    def main(self) -> None:
        tk.Button(
                self, text="<", width=10, height=1, font=ENTRY_FONT, bg="#dddddd", command=self.return_prev_page
            ).grid(
                row=self.i, column=0, padx=self.PADX, sticky="w"
        )
        self.first_entry = self.string_entry(self, "Name: ", self.i, 0, self.product_name)
        self.type_entry = self.choice_entry(self, "Type: ", self.i, 0, self.product_type, PRODUCT_TYPES_LIST)
        self.float_entry(self, "Price: ", self.i, 0, self.product_price)
        self.int_entry(self, "Min. Unit: ", self.i, 0, self.product_min_unit)
        self.int_entry(self, "Best Before: ", self.i, 0, self.product_best_before)
        self.string_entry(self, "Shelf ID: ", self.i, 0, self.product_shelf_id)
        self.last_entry = self.create_button(self, "Edit Item", self.i, 1, 30, "#d0ffd0", self.edit_product)

        table_frame = ttk.Frame(self)
        table_frame.columnconfigure(0, weight=1)
        table_frame.grid(row=self.i, column=0, columnspan=2, sticky="ew")
        self.create_table(table_frame, 0, 0)
        self.table.config(height=8)

    def events(self) -> None:
        self.tab_sequencing()
        self.table.bind("<Double-Button-1>", self.select_batch)

    def edit_product(self) -> None:
        if not self.product_id.get():
            return None
        name = self.product_name.get()
        type = self.product_type.get()
        price = self.product_price.get()
        min_unit = self.product_min_unit.get()
        best_before = self.product_best_before.get()
        shelf = self.product_shelf_id.get()
        if not (name and type and price and min_unit and best_before and shelf):
            messagebox.showwarning("Missing Values", "Values are Missing!")
            return None
        p = product.edit(
            id=self.product_id.get(),
            name=name,
            type=type,
            price=price,
            min_unit=min_unit,
            best_before=best_before,
            shelf=shelf
        )
        if not p:
            messagebox.showwarning("WARNING", "Product not found!")
            return None
        self.return_prev_page()

    def select_batch(self, *args) -> None:
        selected_batch = self.table.selection()
        if not selected_batch:
            return None
        batch_id = self.table.item(selected_batch[0]).get("values", [None])[0]
        b = batch.get(batch_id=batch_id)
        self.batchDetail.batch_id.set(b.id)
        self.batchDetail.previous_page = self
        self.batchDetail.set_active()

    def update_table(self):
        self.table.delete(*self.table.get_children())
        batches = batch.get_all_from_product(self.product_id.get())
        for b in batches:
            self.table.insert(
                '', tk.END,
                values=(
                    b.id,
                    b.batch_no,
                    b.mfg_date,
                    b.exp_date,
                    b.price,
                    b.quantity,
                    b.distributor
                )
            )

    def refresh(self) -> None:
        p = product.get_by_id(self.product_id.get())
        if not p:
            self.product_name.set("")
            self.type_entry.current(0)
            self.product_price.set("")
            self.product_min_unit.set("")
            self.product_best_before.set("")
            self.product_shelf_id.set("")
            self.first_entry.focus_set()
            self.table.delete(*self.table.get_children())
            return None
        self.product_name.set(p.name)
        self.type_entry.current(PRODUCT_TYPES_LIST.index(p.type))
        self.product_price.set(p.price)
        self.product_min_unit.set(p.min_unit)
        self.product_best_before.set(p.best_before)
        self.product_shelf_id.set(p.shelf)
        self.update_table()
        self.first_entry.focus_set()
