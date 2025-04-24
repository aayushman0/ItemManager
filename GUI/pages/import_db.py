import tkinter as tk
from tkinter import ttk, messagebox
from db.orm import product
from db.imported_models import yield_items
from GUI import classes
from variables import PRODUCT_TYPES_LIST


class Frame(classes.Frame):
    def __init__(self, master) -> None:
        super().__init__(master)
        self.columnconfigure(1, weight=1)
        self.table_columns = ["Batch No.", "Mfg Date", "Exp Date", "Price", "Quantity", "Distributor"]
        self.table_columns_width = [200, 100, 100, 150, 100, 150]
        self.table_columns_align = ["w", "e", "e", "e", "e", "e"]
        self.generator = yield_items()
        self.current_batch_list = list()
        self.iteration_started = False
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

    def main(self) -> None:
        self.first_entry = self.string_entry(self, "Name: ", self.i, 0, self.product_name)
        self.type_entry = self.choice_entry(self, "Type: ", self.i, 0, self.product_type, PRODUCT_TYPES_LIST)
        self.float_entry(self, "Price: ", self.i, 0, self.product_price)
        self.int_entry(self, "Min. Unit: ", self.i, 0, self.product_min_unit)
        self.int_entry(self, "Best Before: ", self.i, 0, self.product_best_before)
        self.string_entry(self, "Shelf ID: ", self.i, 0, self.product_shelf_id)
        self.last_entry = self.create_button(self, "Import Item", self.i, 1, 30, "#d0ffd0", self.import_product)
        self.create_button(self, "Skip Item", self.i, 1, 30, "#ffd0d0", self.change_product)

        table_frame = ttk.Frame(self)
        table_frame.columnconfigure(0, weight=1)
        table_frame.grid(row=self.i, column=0, columnspan=2)
        self.create_table(table_frame, 0, 0)
        self.table.config(height=8)

    def events(self) -> None:
        self.tab_sequencing()

    def import_product(self) -> None:
        name = self.product_name.get()
        type = self.product_type.get()
        price = self.product_price.get()
        min_unit = self.product_min_unit.get()
        best_before = self.product_best_before.get()
        shelf = self.product_shelf_id.get()

        if not (name and type and price and min_unit and best_before and shelf):
            messagebox.showwarning("Missing Values", "Values are Missing!")
            return None
        product.import_product(name, type, price, min_unit, best_before, shelf, self.current_batch_list)
        self.change_product()

    def change_product(self) -> None:
        self.table.delete(*self.table.get_children())
        self.current_batch_list = []
        try:
            i_dict, b_list = next(self.generator)
        except StopIteration:
            self.product_name.set("")
            self.type_entry.current(0)
            self.product_price.set("")
            self.product_min_unit.set("")
            self.product_best_before.set("")
            self.product_shelf_id.set("")
            self.first_entry.focus_set()
            return None
        self.product_name.set(i_dict.get("name"))
        try:
            self.type_entry.current(PRODUCT_TYPES_LIST.index(i_dict.get("type")))
        except ValueError:
            self.type_entry.current(0)
        self.product_price.set(i_dict.get("price"))
        self.product_min_unit.set(i_dict.get("min_unit"))
        self.product_best_before.set(i_dict.get("best_before"))
        self.product_shelf_id.set("")
        for b_dict in b_list:
            cur_b_list = [
                    b_dict.get("batch_no"),
                    b_dict.get("mfg_date"),
                    b_dict.get("exp_date"),
                    b_dict.get("price"),
                    b_dict.get("quantity"),
                    b_dict.get("distributor")
                ]
            self.current_batch_list.append(cur_b_list)
            self.table.insert(
                '', tk.END,
                values=cur_b_list
            )

        self.first_entry.focus_set()

    def refresh(self) -> None:
        if self.iteration_started:
            return None
        self.iteration_started = True
        self.change_product()
